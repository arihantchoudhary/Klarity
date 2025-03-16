import os
from pathlib import Path
import pandas as pd
from typing import List, Dict
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

class DenseVectorStore:
    """Handles dense vector storage and retrieval using ChromaDB."""
    
    def __init__(self, persist_dir: str = "./vector_store"):
        """Initialize the vector store.
        
        Args:
            persist_dir: Directory to persist ChromaDB
        """
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)
        
        # Initialize sentence transformer for embeddings
        self.embedding_model = SentenceTransformer('all-mpnet-base-v2')
        
        # Initialize ChromaDB with sentence transformer embeddings
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name='all-mpnet-base-v2'
        )
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="pfizer_documents",
            embedding_function=self.embedding_function,
            metadata={"description": "Pfizer document chunks with dense vector embeddings"}
        )
    
    def chunk_text(self, text: str, chunk_size: int = 800, chunk_overlap: int = 80) -> List[str]:
        """Split text into overlapping chunks.
        
        Args:
            text: Text to split
            chunk_size: Maximum chunk size in characters
            chunk_overlap: Overlap between chunks in characters
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            # Find the end of the chunk
            end = start + chunk_size
            
            # If we're not at the end of the text, try to break at a sentence
            if end < text_len:
                # Look for sentence endings (.!?) within the last 100 chars of the chunk
                look_back = min(100, chunk_size)
                last_period = text.rfind('.', end - look_back, end)
                last_exclaim = text.rfind('!', end - look_back, end)
                last_question = text.rfind('?', end - look_back, end)
                
                # Find the latest sentence ending
                sentence_end = max(last_period, last_exclaim, last_question)
                
                if sentence_end != -1 and sentence_end > start:
                    end = sentence_end + 1
            
            # Add the chunk
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move the start pointer, considering overlap
            start = end - chunk_overlap
        
        return chunks
    
    def process_extractions(self, csv_path: str, batch_size: int = 100):
        """Process extracted text from CSV and add to vector store.
        
        Args:
            csv_path: Path to CSV file with extractions
            batch_size: Number of chunks to process at once
        """
        # Read the CSV
        df = pd.read_csv(csv_path)
        print(f"Processing {len(df)} documents...")
        
        # Process each document
        current_batch = {
            'documents': [],
            'metadatas': [],
            'ids': []
        }
        
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            # Get text content
            text = row['extracted_text']
            if not isinstance(text, str) or not text.strip():
                continue
                
            # Chunk the text
            chunks = self.chunk_text(text)
            
            # Add chunks to current batch
            for i, chunk in enumerate(chunks):
                chunk_id = f"{row['file_path']}_{i}"
                metadata = {
                    'file_path': row['file_path'],
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'num_pages': row['num_pages']
                }
                
                current_batch['documents'].append(chunk)
                current_batch['metadatas'].append(metadata)
                current_batch['ids'].append(chunk_id)
                
                # If batch is full, add to collection
                if len(current_batch['documents']) >= batch_size:
                    self._add_batch(current_batch)
                    current_batch = {
                        'documents': [],
                        'metadatas': [],
                        'ids': []
                    }
        
        # Add remaining chunks
        if current_batch['documents']:
            self._add_batch(current_batch)
        
        print(f"Added {self.collection.count()} chunks to vector store")
    
    def _add_batch(self, batch: Dict):
        """Add a batch of chunks to the collection.
        
        Args:
            batch: Dictionary containing documents, metadatas, and ids
        """
        try:
            self.collection.add(
                documents=batch['documents'],
                metadatas=batch['metadatas'],
                ids=batch['ids']
            )
        except Exception as e:
            print(f"Error adding batch: {str(e)}")
            # Try adding one by one
            for i in range(len(batch['documents'])):
                try:
                    self.collection.add(
                        documents=[batch['documents'][i]],
                        metadatas=[batch['metadatas'][i]],
                        ids=[batch['ids'][i]]
                    )
                except Exception as e:
                    print(f"Error adding document {batch['ids'][i]}: {str(e)}")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for similar text chunks.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of dictionaries containing chunks and metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            result = {
                'chunk': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            }
            formatted_results.append(result)
        
        return formatted_results
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store.
        
        Returns:
            Dictionary containing statistics
        """
        return {
            'total_chunks': self.collection.count(),
            'name': self.collection.name,
            'metadata': self.collection.metadata
        } 