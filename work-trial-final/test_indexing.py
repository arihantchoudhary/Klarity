#!/usr/bin/env python3
"""
Test Script for File Inventory and Vector Indexing

This script tests the file inventory and vector indexing functionality by:
1. Creating a sample directory structure with test files
2. Running the file inventory creation
3. Testing the vector indexing process
4. Displaying results for verification

Usage:
    python test_indexing.py [--component=all|inventory|vector]

Options:
    --component: Specifies which component to test (default: all)
"""

import os
import sys
import shutil
import argparse
import logging
from pathlib import Path
import pandas as pd
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set up paths
current_dir = Path(__file__).parent.absolute()
test_uploads_dir = current_dir / "test_data" / "uploads"
test_inventory_csv = current_dir / "test_data" / "output" / "test_inventory.csv"
test_vector_dir = current_dir / "test_data" / "output" / "vector_index"

def create_test_environment():
    """Create a test environment with sample files."""
    logger.info("Creating test environment")
    
    # Create directories
    os.makedirs(test_uploads_dir, exist_ok=True)
    os.makedirs(test_inventory_csv.parent, exist_ok=True)
    
    # Create sample text file
    with open(test_uploads_dir / "sample1.txt", "w") as f:
        f.write("This is a sample text file for testing the file inventory.")
    
    # Copy sample PDF if available
    sample_pdf = current_dir / "test_data" / "output" / "sample_document.pdf"
    if sample_pdf.exists():
        shutil.copy(sample_pdf, test_uploads_dir / "sample_document.pdf")
    else:
        # Create a dummy PDF-like file if no real PDF is available
        with open(test_uploads_dir / "sample_dummy.pdf", "w") as f:
            f.write("%PDF-1.4\nThis is a dummy PDF file for testing purposes.\n%%EOF")
    
    # Create other file types for testing
    with open(test_uploads_dir / "sample.csv", "w") as f:
        f.write("id,name,value\n1,test1,100\n2,test2,200\n")
    
    with open(test_uploads_dir / "sample.md", "w") as f:
        f.write("# Sample Markdown\nThis is a sample markdown file.\n")
    
    logger.info(f"Created test files in {test_uploads_dir}")
    return True

def test_file_inventory():
    """Test the file inventory creation functionality."""
    logger.info("Testing file inventory creation")
    
    try:
        # Import the mock dependencies if needed
        sys.path.insert(0, str(current_dir))
        try:
            # First try direct import
            from create_file_inventory import FileInventoryCreator
        except ImportError:
            # If direct import fails, try using mock dependencies
            logger.info("Using mock dependencies for file inventory test")
            from mock_dependencies import patch_modules
            patch_modules()
            from create_file_inventory import FileInventoryCreator
        
        # Create inventory
        inventory_creator = FileInventoryCreator(
            uploads_dir=test_uploads_dir, 
            output_csv=test_inventory_csv
        )
        
        # Create the inventory
        inventory_df = inventory_creator.create_inventory()
        
        # Display results
        print("\n" + "="*50)
        print("FILE INVENTORY TEST RESULTS:")
        print("="*50)
        print(f"Files processed: {len(inventory_df)}")
        print(f"Inventory saved to: {test_inventory_csv}")
        
        if not inventory_df.empty:
            print("\nFile Category Distribution:")
            category_counts = inventory_df['file_category'].value_counts()
            for category, count in category_counts.items():
                print(f"  {category}: {count}")
                
            print("\nSample inventory entries:")
            pd.set_option('display.max_columns', None)
            print(inventory_df.head().to_string())
            
        return inventory_df
        
    except ImportError:
        logger.error("Could not import FileInventoryCreator. Check your setup.")
        print("\nError: Could not import FileInventoryCreator.")
        print("Make sure create_file_inventory.py is in the same directory.")
        return None
        
    except Exception as e:
        logger.error(f"Error testing file inventory: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_vector_indexing(inventory_df=None):
    """Test the vector indexing functionality."""
    logger.info("Testing vector indexing")
    
    if inventory_df is None:
        # Try to load inventory if not provided
        if test_inventory_csv.exists():
            inventory_df = pd.read_csv(test_inventory_csv)
        else:
            logger.error("No inventory file found and none provided.")
            print("\nError: No inventory file found.")
            print("Run test_file_inventory first or provide an inventory DataFrame.")
            return False
    
    try:
        # Import the ChunkExtractor directly for testing document processing
        sys.path.insert(0, str(current_dir))
        try:
            # First try direct import
            from create_vector_index import ChunkExtractor, VectorIndexer
        except ImportError:
            # If direct import fails, try using mock dependencies
            logger.info("Using mock dependencies for vector indexing test")
            try:
                from mock_dependencies import patch_modules, is_patched
                if not is_patched():
                    patch_modules()
            except ImportError:
                pass
            from create_vector_index import ChunkExtractor, VectorIndexer
        
        # Create chunk extractor for testing
        chunk_extractor = ChunkExtractor(chunk_size=200, chunk_overlap=20)
        
        # Find PDF files to test
        pdf_files = []
        for file in os.listdir(test_uploads_dir):
            if file.endswith('.pdf'):
                pdf_files.append(str(test_uploads_dir / file))
        
        if not pdf_files:
            logger.warning("No PDF files found for testing vector indexing")
            print("\nWarning: No PDF files found for testing vector indexing.")
            print("The test will continue with simulated results.")
            
            # Create a sample text chunk for testing
            sample_chunks = [{
                'text': 'This is a sample text chunk for testing vector indexing.',
                'source': 'simulated_source.pdf',
                'chunk_type': 'text',
                'section_idx': 1,
                'created_at': datetime.now().isoformat()
            }]
        else:
            # Process PDF files
            all_chunks = []
            for pdf_file in pdf_files:
                logger.info(f"Processing {pdf_file} for chunks")
                chunks = chunk_extractor.process_pdf(pdf_file)
                all_chunks.extend(chunks)
                
            sample_chunks = all_chunks
        
        # Create vector indexer
        indexer = VectorIndexer(output_dir=test_vector_dir)
        
        # Add chunks and generate embeddings
        indexer.add_chunks(sample_chunks)
        indexer.generate_embeddings()
        indexer.build_index()
        indexer.save_index()
        
        # Display results
        print("\n" + "="*50)
        print("VECTOR INDEXING TEST RESULTS:")
        print("="*50)
        total_chunks = len(indexer.chunks)
        text_chunks = len([c for c in indexer.chunks if c['chunk_type'] == 'text'])
        table_chunks = len([c for c in indexer.chunks if c['chunk_type'] == 'table'])
        
        print(f"Total chunks created: {total_chunks}")
        print(f"  - Text chunks: {text_chunks}")
        print(f"  - Table chunks: {table_chunks}")
        print(f"Vector dimension: {indexer.vector_dim}")
        print(f"Index saved to: {test_vector_dir}")
        
        # Display sample chunks
        if total_chunks > 0:
            print("\nSample chunk:")
            sample_chunk = indexer.chunks[0]
            print(f"  Type: {sample_chunk['chunk_type']}")
            print(f"  Source: {sample_chunk['source']}")
            print(f"  Text sample: {sample_chunk['text'][:100]}...")
            
        return True
        
    except ImportError:
        logger.error("Could not import vector indexing modules. Check your setup.")
        print("\nError: Could not import vector indexing modules.")
        print("Make sure create_vector_index.py is in the same directory.")
        return False
        
    except Exception as e:
        logger.error(f"Error testing vector indexing: {e}")
        import traceback
        traceback.print_exc()
        return False

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Test file inventory and vector indexing')
    parser.add_argument('--component', choices=['all', 'inventory', 'vector'], default='all',
                        help='Component to test (default: all)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    print("\nSetting up Test Environment...")
    if not create_test_environment():
        print("Failed to set up test environment. Exiting.")
        sys.exit(1)
    
    if args.component in ['all', 'inventory']:
        print("\nTesting File Inventory Creation...")
        inventory_df = test_file_inventory()
        if inventory_df is None:
            print("\nFile Inventory Test: FAILED")
        else:
            print("\nFile Inventory Test: SUCCESS")
    
    if args.component in ['all', 'vector']:
        print("\nTesting Vector Indexing...")
        inventory_df = None
        if args.component == 'all':
            # Use inventory from previous test if available
            # Otherwise, inventory will be loaded from file if it exists
            pass
        
        if test_vector_indexing(inventory_df):
            print("\nVector Indexing Test: SUCCESS")
        else:
            print("\nVector Indexing Test: FAILED")
    
    print("\nTesting completed.")
    print("\nTroubleshooting tips:")
    print("1. Ensure all required packages are installed:")
    print("   pip install pandas numpy tqdm sentence-transformers faiss-cpu")
    print("2. Check logs for detailed error information")
    print("3. Verify that test files were created properly")
