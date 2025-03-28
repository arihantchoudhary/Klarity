#!/usr/bin/env python3
"""
Vector Index Creator

This script creates a dense vector index from the extracted content of PDF files.
It processes files listed in the inventory, extracts text and structural elements,
generates embeddings, and builds a searchable vector index.
"""

import os
import sys
import json
import logging
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from datetime import datetime

# Try different import paths to handle the project structure
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from pdf_parser import RAGFlowPdfParser
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from work_trial_final.pdf_parser import RAGFlowPdfParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import vector indexing libraries
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    VECTOR_LIBS_AVAILABLE = True
except ImportError:
    logger.warning("Vector libraries not found. Will simulate embedding generation.")
    VECTOR_LIBS_AVAILABLE = False


class ChunkExtractor:
    """
    Extracts and processes chunks of text from PDF documents.
    
    This class handles the extraction of text, tables, and other content
    from PDF files, and splits them into appropriate chunks for embedding
    and indexing.
    """
    
    def __init__(self, chunk_size=512, chunk_overlap=50):
        """
        Initialize the chunk extractor.
        
        Args:
            chunk_size (int): Target size of text chunks
            chunk_overlap (int): Overlap between chunks to maintain context
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.pdf_parser = RAGFlowPdfParser()
        
    def process_pdf(self, pdf_path):
        """
        Process a PDF file and extract content chunks.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            list: List of chunk dictionaries with text and metadata
        """
        logger.info(f"Processing PDF: {pdf_path}")
        try:
            # Extract text and tables from the PDF
            text, tables = self.pdf_parser(pdf_path, need_image=True)
            
            # Create chunks from the extracted text
            chunks = []
            
            # Process the main text content
            if text:
                text_chunks = self.split_text(text, pdf_path)
                chunks.extend(text_chunks)
            
            # Process tables if available
            if tables:
                table_chunks = self.process_tables(tables, pdf_path)
                chunks.extend(table_chunks)
                
            logger.info(f"Created {len(chunks)} chunks from {pdf_path}")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {e}")
            return []
    
    def split_text(self, text, source_file, min_chunk_size=100):
        """
        Split text into overlapping chunks of appropriate size.
        
        Args:
            text (str): Text to split into chunks
            source_file (str): Source file path for metadata
            min_chunk_size (int): Minimum size for a meaningful chunk
            
        Returns:
            list: List of chunk dictionaries
        """
        # Clean text by removing redundant spacing and normalizing line breaks
        clean_text = self.pdf_parser.remove_tag(text)
        
        # Split the document into logical sections based on double newlines
        sections = [s for s in clean_text.split('\n\n') if s.strip()]
        
        chunks = []
        current_chunk = ""
        current_section_idx = 0
        
        # Process each section
        for section in sections:
            # If adding this section would exceed chunk size and we already have content,
            # save the current chunk and start a new one with overlap
            if len(current_chunk) + len(section) > self.chunk_size and len(current_chunk) >= min_chunk_size:
                chunks.append({
                    'text': current_chunk,
                    'source': source_file,
                    'chunk_type': 'text',
                    'section_idx': current_section_idx,
                    'created_at': datetime.now().isoformat()
                })
                
                # Start a new chunk with overlap by including the last bit of the previous chunk
                if self.chunk_overlap > 0 and len(current_chunk) > self.chunk_overlap:
                    # Find a clean break point for the overlap
                    overlap_text = current_chunk[-self.chunk_overlap:]
                    # Try to find a sentence or paragraph break in the overlap region
                    break_points = [overlap_text.rfind('. '), overlap_text.rfind('\n')]
                    best_break = max(break_points)
                    
                    if best_break > 0:
                        current_chunk = current_chunk[-(best_break+1):]
                    else:
                        current_chunk = current_chunk[-self.chunk_overlap:]
                else:
                    current_chunk = ""
            
            # Add the current section to the chunk
            if current_chunk and not current_chunk.endswith('\n'):
                current_chunk += '\n'
            current_chunk += section
            current_section_idx += 1
        
        # Add the final chunk if it's not empty
        if current_chunk and len(current_chunk) >= min_chunk_size:
            chunks.append({
                'text': current_chunk,
                'source': source_file,
                'chunk_type': 'text',
                'section_idx': current_section_idx,
                'created_at': datetime.now().isoformat()
            })
            
        return chunks
    
    def process_tables(self, tables, source_file):
        """
        Process extracted tables into chunks.
        
        Args:
            tables (list): List of tables from the PDF parser
            source_file (str): Source file path for metadata
            
        Returns:
            list: List of chunk dictionaries for tables
        """
        table_chunks = []
        
        for i, table_data in enumerate(tables):
            # Each table is a tuple of (image, content)
            # For simple text representation, we can convert the table content to text
            table_image, table_content = table_data
            
            if isinstance(table_content, list):
                # If it's a simple list, join with newlines
                table_text = '\n'.join([str(row) for row in table_content])
            elif isinstance(table_content, str):
                # If it's already a string (e.g., HTML), use as is
                table_text = table_content
            else:
                # For other formats, attempt to convert to string
                table_text = str(table_content)
            
            table_chunks.append({
                'text': table_text,
                'source': source_file,
                'chunk_type': 'table',
                'table_idx': i,
                'created_at': datetime.now().isoformat()
            })
            
        return table_chunks


class VectorIndexer:
    """
    Creates and manages dense vector indexes for document chunks.
    
    This class handles embedding generation, vector indexing,
    and storage of the index for efficient semantic search.
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2', output_dir='vector_index'):
        """
        Initialize the vector indexer.
        
        Args:
            model_name (str): Name of the sentence transformer model to use
            output_dir (str): Directory to store the vector index
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        self.chunks = []
        self.metadata = []
        self.embeddings = None
        self.index = None
        
        # Initialize the embedding model if libraries are available
        if VECTOR_LIBS_AVAILABLE:
            logger.info(f"Loading embedding model: {model_name}")
            self.model = SentenceTransformer(model_name)
            self.vector_dim = self.model.get_sentence_embedding_dimension()
        else:
            logger.warning("Using simulated embeddings (random vectors)")
            self.model = None
            self.vector_dim = 768  # Typical embedding dimension
    
    def add_chunks(self, chunks):
        """
        Add chunks to the index.
        
        Args:
            chunks (list): List of chunk dictionaries with text and metadata
        """
        self.chunks.extend(chunks)
        # Extract metadata separately for storage
        for chunk in chunks:
            metadata = {k: v for k, v in chunk.items() if k != 'text'}
            self.metadata.append(metadata)
    
    def generate_embeddings(self):
        """
        Generate embeddings for all added chunks.
        """
        if not self.chunks:
            logger.warning("No chunks to embed")
            return
        
        logger.info(f"Generating embeddings for {len(self.chunks)} chunks")
        
        # Extract text content from chunks
        texts = [chunk['text'] for chunk in self.chunks]
        
        if VECTOR_LIBS_AVAILABLE and self.model:
            # Use actual embedding model
            self.embeddings = self.model.encode(
                texts, 
                show_progress_bar=True,
                batch_size=32,
                convert_to_numpy=True
            )
        else:
            # Generate random embeddings for simulation
            logger.info("Using simulated embeddings (random vectors)")
            self.embeddings = np.random.randn(len(texts), self.vector_dim).astype(np.float32)
            # Normalize the random vectors (as real embeddings are usually normalized)
            self.embeddings = self.embeddings / np.linalg.norm(self.embeddings, axis=1, keepdims=True)
    
    def build_index(self):
        """
        Build a FAISS index from the generated embeddings.
        """
        if self.embeddings is None:
            logger.warning("No embeddings available. Call generate_embeddings() first.")
            return
            
        logger.info("Building vector index")
        
        if VECTOR_LIBS_AVAILABLE:
            # Create a FAISS index for fast similarity search
            # Use L2 distance (squared Euclidean) for similarity
            self.index = faiss.IndexFlatL2(self.vector_dim)
            
            # Add the embeddings to the index
            self.index.add(self.embeddings.astype(np.float32))
            
            # For larger datasets, consider using an approximate neighbor index:
            # index = faiss.IndexIVFFlat(quantizer, d, n_cells, faiss.METRIC_L2)
            # Where n_cells is typically sqrt(n) for n vectors
        else:
            logger.warning("FAISS not available, skipping actual index creation")
            self.index = "SIMULATED_INDEX"
    
    def save_index(self):
        """
        Save the vector index and associated metadata to disk.
        """
        if self.index is None or self.embeddings is None:
            logger.warning("Index or embeddings not available. Nothing to save.")
            return
            
        logger.info(f"Saving index to {self.output_dir}")
        
        # Save metadata
        with open(self.output_dir / 'chunk_metadata.json', 'w') as f:
            json.dump(self.metadata, f, indent=2)
        
        # Save embeddings as numpy array
        np.save(self.output_dir / 'embeddings.npy', self.embeddings)
        
        # Save chunks for reference
        with open(self.output_dir / 'chunks.pkl', 'wb') as f:
            pickle.dump(self.chunks, f)
        
        # Save the index if FAISS is available
        if VECTOR_LIBS_AVAILABLE and isinstance(self.index, faiss.Index):
            faiss.write_index(self.index, str(self.output_dir / 'faiss_index.bin'))
        else:
            logger.warning("FAISS index not available, skipping index save")
        
        # Save indexing metadata
        with open(self.output_dir / 'index_info.json', 'w') as f:
            json.dump({
                'num_vectors': len(self.chunks),
                'vector_dim': self.vector_dim,
                'created_at': datetime.now().isoformat(),
                'vector_libs_available': VECTOR_LIBS_AVAILABLE
            }, f, indent=2)
        
        logger.info(f"Index saved successfully with {len(self.chunks)} vectors")
    
    def process_and_index_files(self, inventory_df, uploads_dir):
        """
        Process and index all PDF files in the inventory.
        
        Args:
            inventory_df (DataFrame): DataFrame containing file inventory
            uploads_dir (str): Path to the uploads directory
        """
        chunk_extractor = ChunkExtractor()
        
        # Filter for PDF files
        pdf_files = inventory_df[inventory_df['file_type'] == 'application/pdf']
        
        if len(pdf_files) == 0:
            logger.warning("No PDF files found in inventory")
            return
            
        logger.info(f"Processing {len(pdf_files)} PDF files")
        
        for _, row in tqdm(pdf_files.iterrows(), total=len(pdf_files)):
            file_path = os.path.join(uploads_dir, row['file_path'])
            
            # Extract chunks from the PDF
            chunks = chunk_extractor.process_pdf(file_path)
            
            # Add chunks to the indexer
            self.add_chunks(chunks)
            
            # Update inventory with extraction status
            inventory_df.loc[inventory_df['file_path'] == row['file_path'], 'extracted_text'] = True
            if len([c for c in chunks if c['chunk_type'] == 'table']) > 0:
                inventory_df.loc[inventory_df['file_path'] == row['file_path'], 'extracted_tables'] = True
        
        # Generate embeddings and build the index
        self.generate_embeddings()
        self.build_index()
        self.save_index()
        
        return inventory_df


if __name__ == "__main__":
    # Set the inventory file path
    INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "file_inventory.csv")
    UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
    OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vector_index")
    
    # Check if inventory exists
    if not os.path.exists(INVENTORY_FILE):
        logger.error(f"Inventory file not found: {INVENTORY_FILE}")
        logger.info("Please run create_file_inventory.py first")
        sys.exit(1)
    
    # Load inventory
    logger.info(f"Loading inventory from {INVENTORY_FILE}")
    inventory_df = pd.read_csv(INVENTORY_FILE)
    
    # Create the vector indexer
    indexer = VectorIndexer(output_dir=OUTPUT_DIR)
    
    # Process and index files
    updated_inventory = indexer.process_and_index_files(inventory_df, UPLOADS_DIR)
    
    # Save updated inventory
    updated_inventory.to_csv(INVENTORY_FILE, index=False)
    
    # Print summary
    total_chunks = len(indexer.chunks)
    text_chunks = len([c for c in indexer.chunks if c['chunk_type'] == 'text'])
    table_chunks = len([c for c in indexer.chunks if c['chunk_type'] == 'table'])
    
    print(f"\nVector Indexing Complete")
    print(f"=========================")
    print(f"Files processed: {len(inventory_df[inventory_df['extracted_text']])}")
    print(f"Total chunks created: {total_chunks}")
    print(f"  - Text chunks: {text_chunks}")
    print(f"  - Table chunks: {table_chunks}")
    print(f"Vector dimension: {indexer.vector_dim}")
    print(f"Index saved to: {OUTPUT_DIR}")
    
    # Note about vector libraries
    if not VECTOR_LIBS_AVAILABLE:
        print("\nNOTE: Vector libraries not available. Used simulated embeddings.")
        print("To use actual embeddings, install:")
        print("  pip install sentence-transformers faiss-cpu")
