import os
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path

# Document loading and processing
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader, 
    UnstructuredExcelLoader,
    UnstructuredImageLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.schema import BaseRetriever

# Embeddings
from langchain_openai import OpenAIEmbeddings  # Or any other embedding model
# For locally hosted models, you might use:
# from langchain_community.embeddings import HuggingFaceEmbeddings

# LLM
from langchain_openai import ChatOpenAI  # Or any other LLM
# For locally hosted models, you might use:
# from langchain_community.llms import HuggingFaceLLM

# Advanced retrieval components
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate

# Flask imports
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename


# 1. DOCUMENT PROCESSING

class DocumentProcessor:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def load_documents(self) -> List[Document]:
        """Load documents from various file formats"""
        documents = []
        data_path = Path(self.data_dir)
        
        for file_path in data_path.glob("**/*"):
            if file_path.is_file():
                try:
                    if file_path.suffix.lower() == ".pdf":
                        loader = PyPDFLoader(str(file_path))
                        documents.extend(loader.load())
                    elif file_path.suffix.lower() == ".docx":
                        loader = Docx2txtLoader(str(file_path))
                        documents.extend(loader.load())
                    elif file_path.suffix.lower() in [".xlsx", ".xls"]:
                        loader = UnstructuredExcelLoader(str(file_path))
                        documents.extend(loader.load())
                    elif file_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                        loader = UnstructuredImageLoader(str(file_path))
                        documents.extend(loader.load())
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
        
        return documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        return self.text_splitter.split_documents(documents)


# 2. BASIC RAG IMPLEMENTATION

class BasicRAG:
    def __init__(self, embedding_model=None, llm=None):
        self.embedding_model = embedding_model or OpenAIEmbeddings()
        self.llm = llm or ChatOpenAI(temperature=0.2)
        self.vector_store = None
    
    def create_index(self, documents: List[Document]):
        """Create vector store index from documents"""
        self.vector_store = FAISS.from_documents(documents, self.embedding_model)
        return self.vector_store
    
    def save_index(self, path: str):
        """Save vector store index to disk"""
        self.vector_store.save_local(path)
    
    def load_index(self, path: str):
        """Load vector store index from disk"""
        self.vector_store = FAISS.load_local(path, self.embedding_model)
        return self.vector_store
    
    def retrieve(self, query: str, k: int = 4) -> List[Document]:
        """Retrieve relevant documents for a query"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call create_index or load_index first.")
        
        return self.vector_store.similarity_search(query, k=k)
    
    def query(self, query: str, k: int = 4) -> str:
        """Process a query through the RAG pipeline"""
        documents = self.retrieve(query, k)
        
        # Create prompt template
        prompt_template = """You are a helpful assistant. Use the following context to answer the question.
        If you don't know the answer based on the context, say you don't know.
        
        Context:
        {context}
        
        Question: {input}
        """
        
        # Create document chain
        prompt = PromptTemplate.from_template(prompt_template)
        document_chain = create_stuff_documents_chain(self.llm, prompt)
        
        # Create retrieval chain
        retrieval_chain = create_retrieval_chain(
            self.vector_store.as_retriever(search_kwargs={"k": k}),
            document_chain
        )
        
        # Run the chain
        response = retrieval_chain.invoke({"input": query})
        return response["answer"]


# 3. ADVANCED RAG COMPONENTS

class SubQuery(BaseModel):
    """Model for query decomposition"""
    sub_queries: List[str] = Field(description="List of sub-queries to answer the main question")
    explanation: str = Field(description="Explanation of why these sub-queries will help answer the main question")


class DocumentSourceSelection(BaseModel):
    """Model for query routing"""
    relevant_sources: List[str] = Field(description="List of relevant document sources for this query")
    source_specific_queries: Dict[str, List[str]] = Field(description="Map of document source to specific queries for that source")


class ChainOfNoteAnalysis(BaseModel):
    """Model for Chain of Note analysis"""
    relevance: int = Field(description="Relevance score from 0-10", ge=0, le=10)
    key_points: List[str] = Field(description="Key points from the document relevant to the query")
    missing_info: List[str] = Field(description="Information that's missing but would be helpful")
    conflicts: List[str] = Field(description="Any conflicts or inconsistencies in the document")
    notes: str = Field(description="Additional notes or observations about the document")


class AdvancedRAG(BasicRAG):
    def __init__(self, embedding_model=None, llm=None):
        super().__init__(embedding_model, llm)
        self.document_sources = {}  # Map of source name to vector store
    
    # Query transformation
    def transform_query(self, query: str) -> str:
        """Improve query formulation"""
        prompt = PromptTemplate.from_template(
            """You are an expert at reformulating questions to make them clearer and more specific.
            Rewrite the following query to make it more effective for information retrieval:
            
            Original query: {query}
            
            Improved query:"""
        )
        
        chain = prompt | self.llm
        response = chain.invoke({"query": query})
        return response.content
    
    # Query decomposition
    def decompose_query(self, query: str) -> List[str]:
        """Break complex query into simpler sub-queries"""
        prompt = PromptTemplate.from_template(
            """You are an expert at breaking down complex questions into simpler sub-questions.
            Break down the following complex query into 2-5 simpler sub-queries that together would help answer the original question.
            Return ONLY a JSON list of strings representing the sub-queries.
            
            Complex query: {query}
            
            Sub-queries:"""
        )
        
        parser = PydanticOutputParser(pydantic_object=SubQuery)
        chain = prompt | self.llm | parser
        response = chain.invoke({"query": query})
        return response.sub_queries
    
    # Query routing
    def add_document_source(self, name: str, description: str, documents: List[Document]):
        """Add a new document source with description"""
        vector_store = FAISS.from_documents(documents, self.embedding_model)
        self.document_sources[name] = {
            "description": description,
            "vector_store": vector_store
        }
    
    def route_query(self, query: str) -> Dict[str, List[str]]:
        """Determine which document sources to query and with what sub-queries"""
        if not self.document_sources:
            raise ValueError("No document sources added. Call add_document_source first.")
        
        # Create description of available sources
        sources_description = "\n".join([
            f"- {name}: {source['description']}" 
            for name, source in self.document_sources.items()
        ])
        
        prompt = PromptTemplate.from_template(
            """You are an expert at determining which information sources are relevant for answering a question.
            Given the following query and list of available document sources, determine which sources are relevant
            and what specific queries should be sent to each source.
            
            Available document sources:
            {sources_description}
            
            Query: {query}
            
            Provide your analysis as a JSON object with two fields:
            1. relevant_sources: A list of names of relevant document sources
            2. source_specific_queries: A dictionary mapping document source names to lists of specific queries for that source
            """
        )
        
        parser = PydanticOutputParser(pydantic_object=DocumentSourceSelection)
        chain = prompt | self.llm | parser
        response = chain.invoke({"sources_description": sources_description, "query": query})
        
        return response.source_specific_queries
    
    # Advanced retrieval with reranking
    def retrieve_and_rerank(self, query: str, k: int = 4) -> List[Document]:
        """Retrieve documents and rerank them using an LLM"""
        # Use LLM to extract relevant parts of documents
        compressor = LLMChainExtractor.from_llm(self.llm)
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=self.vector_store.as_retriever(search_kwargs={"k": k * 2})  # Retrieve more, then compress
        )
        
        return compression_retriever.get_relevant_documents(query)[:k]
    
    # Chain of Note
    def apply_chain_of_note(self, query: str, documents: List[Document]) -> List[Dict]:
        """Apply Chain of Note to analyze and annotate documents"""
        prompt = PromptTemplate.from_template(
            """You are an expert at analyzing documents for their relevance to a query.
            For the following document, analyze its relevance to the query and extract key information.
            
            Query: {query}
            
            Document: {document}
            
            Provide your analysis as a JSON object with these fields:
            1. relevance: A score from 0-10 indicating how relevant this document is
            2. key_points: List of key points from the document relevant to the query
            3. missing_info: List of information that's missing but would be helpful
            4. conflicts: List of any conflicts or inconsistencies in the document
            5. notes: Additional observations about the document
            """
        )
        
        parser = PydanticOutputParser(pydantic_object=ChainOfNoteAnalysis)
        chain = prompt | self.llm | parser
        
        results = []
        for doc in documents:
            try:
                analysis = chain.invoke({"query": query, "document": doc.page_content})
                results.append({
                    "document": doc,
                    "analysis": analysis
                })
            except Exception as e:
                print(f"Error analyzing document: {e}")
                results.append({
                    "document": doc,
                    "analysis": None
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x["analysis"].relevance if x["analysis"] else 0, reverse=True)
        return results
    
    # Complete advanced query pipeline
    def advanced_query(self, query: str) -> str:
        """Process a query through the advanced RAG pipeline"""
        # Step 1: Transform the query
        improved_query = self.transform_query(query)
        
        # Step 2: If it's a complex query, decompose it
        sub_queries = self.decompose_query(improved_query)
        
        all_responses = []
        if len(sub_queries) > 1:
            # Complex query processing
            for sub_query in sub_queries:
                # Get documents for sub-query
                documents = self.retrieve_and_rerank(sub_query)
                
                # Analyze with Chain of Note
                analyzed_docs = self.apply_chain_of_note(sub_query, documents)
                
                # Filter to relevant documents
                relevant_docs = [item["document"] for item in analyzed_docs if item["analysis"] and item["analysis"].relevance > 5]
                
                # Get response for sub-query
                if relevant_docs:
                    prompt = PromptTemplate.from_template(
                        """Answer the following question based only on the provided context:
                        
                        Question: {query}
                        
                        Context: {context}
                        """
                    )
                    chain = prompt | self.llm
                    response = chain.invoke({
                        "query": sub_query, 
                        "context": "\n\n".join([doc.page_content for doc in relevant_docs[:3]])
                    })
                    all_responses.append({"sub_query": sub_query, "answer": response.content})
                else:
                    all_responses.append({"sub_query": sub_query, "answer": "No relevant information found."})
            
            # Synthesize final answer
            synthesis_prompt = PromptTemplate.from_template(
                """Based on the answers to the following sub-questions, provide a comprehensive answer to the original question.
                
                Original question: {original_query}
                
                Sub-question answers:
                {sub_answers}
                
                Comprehensive answer to the original question:
                """
            )
            
            sub_answers = "\n\n".join([f"Sub-question: {r['sub_query']}\nAnswer: {r['answer']}" for r in all_responses])
            chain = synthesis_prompt | self.llm
            final_response = chain.invoke({
                "original_query": query,
                "sub_answers": sub_answers
            })
            return final_response.content
        else:
            # Simple query processing - use standard retrieval and Chain of Note
            documents = self.retrieve_and_rerank(improved_query)
            analyzed_docs = self.apply_chain_of_note(improved_query, documents)
            relevant_docs = [item["document"] for item in analyzed_docs if item["analysis"] and item["analysis"].relevance > 5]
            
            if not relevant_docs:
                return "I couldn't find relevant information to answer your question."
            
            # Create prompt with Chain of Note insights
            notes = "\n".join([
                f"- Document {i+1} relevance: {item['analysis'].relevance}/10\n  Key points: {', '.join(item['analysis'].key_points)}"
                for i, item in enumerate(analyzed_docs[:3]) if item["analysis"]
            ])
            
            prompt = PromptTemplate.from_template(
                """You are a helpful assistant. Use the following context to answer the question.
                If you don't know the answer based on the context, say you don't know.
                
                Context:
                {context}
                
                Document analysis notes:
                """
            )


# Flask app configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'xls', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the uploaded document
        processor = DocumentProcessor(app.config['UPLOAD_FOLDER'])
        documents = processor.load_documents()
        chunks = processor.chunk_documents(documents)
        
        # Initialize RAG system
        rag = AdvancedRAG()
        rag.create_index(chunks)
        
        return jsonify({'message': 'File uploaded and processed successfully'})
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/query', methods=['POST'])
def process_query():
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    rag = AdvancedRAG()
    try:
        response = rag.advanced_query(query)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)