from typing import List, Dict, Any, Tuple, Optional
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class DenseVectorIndexer:
    """Handles document indexing and retrieval using dense vector embeddings."""
    
    def __init__(self, persist_directory: str, collection_name: str = "documents"):
        """Initialize the vector store.
        
        Args:
            persist_directory: Directory to persist the vector store
            collection_name: Name of the collection to store vectors
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        
        # Initialize sentence transformer for embeddings
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-mpnet-base-v2"
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
            metadata={"description": "Document chunks with embeddings"}
        )
        
        logger.info(f"Initialized vector store at {persist_directory}")
    
    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict]] = None) -> List[str]:
        """Add texts to the vector store.
        
        Args:
            texts: List of text chunks to add
            metadatas: Optional list of metadata dictionaries for each chunk
            
        Returns:
            List of IDs for the added chunks
        """
        if not texts:
            return []
        
        # Generate IDs for chunks
        ids = [f"chunk_{i}" for i in range(len(texts))]
        
        try:
            # Add chunks to collection
            self.collection.add(
                documents=texts,
                metadatas=metadatas if metadatas else None,
                ids=ids
            )
            logger.info(f"Added {len(texts)} chunks to vector store")
            return ids
        
        except Exception as e:
            logger.error(f"Error adding texts to vector store: {e}")
            raise
    
    def similarity_search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar texts in the vector store.
        
        Args:
            query: Query text
            k: Number of results to return
            
        Returns:
            List of dictionaries containing text and metadata
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=k
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['documents'][0])):
                result = {
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else None,
                    'distance': results['distances'][0][i] if 'distances' in results else None
                }
                formatted_results.append(result)
            
            return formatted_results
        
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            raise
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store.
        
        Returns:
            Dictionary containing vector store statistics
        """
        try:
            return {
                'total_chunks': self.collection.count(),
                'collection_name': self.collection.name,
                'metadata': self.collection.metadata
            }
        except Exception as e:
            logger.error(f"Error getting vector store stats: {e}")
            raise
    
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