from typing import List, Dict, Any, Tuple
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DenseVectorIndexer:
    """Handles document indexing and retrieval using dense vector embeddings."""
    
    def __init__(self, 
                collection_name: str = "dense_vector_index",
                embedding_model: str = "text-embedding-3-small",
                persist_directory: str = "./vector_store"):
        """Initialize the vector store.
        
        Args:
            collection_name: Name of the vector store collection
            embedding_model: Name of the embedding model to use
            persist_directory: Directory to persist the vector store
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        
        # Create or load the vector store
        if os.path.exists(persist_directory):
            self.vector_store = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=persist_directory
            )
        else:
            os.makedirs(persist_directory)
            self.vector_store = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=persist_directory
            )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]] = None) -> None:
        """Add texts to the vector store.
        
        Args:
            texts: List of text strings to add
            metadatas: Optional list of metadata dictionaries
        """
        # Split texts into chunks
        docs = []
        for i, text in enumerate(texts):
            chunks = self.text_splitter.split_text(text)
            metadata = metadatas[i] if metadatas else {}
            for j, chunk in enumerate(chunks):
                chunk_metadata = metadata.copy()
                chunk_metadata["chunk_id"] = j
                docs.append(Document(page_content=chunk, metadata=chunk_metadata))
        
        # Add to vector store
        self.vector_store.add_documents(docs)
        self.vector_store.persist()
    
    def similarity_search(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        """Search for similar documents using the query.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of (document, score) tuples
        """
        return self.vector_store.similarity_search_with_relevance_scores(query, k=k)
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add Document objects directly to the vector store.
        
        Args:
            documents: List of Document objects to add
        """
        self.vector_store.add_documents(documents)
        self.vector_store.persist()
    
    def get_relevant_documents(self, query: str, k: int = 5) -> List[Document]:
        """Get relevant documents for a query.
        
        Args:
            query: Search query
            k: Number of documents to return
            
        Returns:
            List of relevant Document objects
        """
        return self.vector_store.similarity_search(query, k=k) 