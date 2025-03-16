import os
from pathlib import Path
from vector_store import DenseVectorStore

def main():
    """Process extracted text and create dense vectors."""
    
    # Initialize paths
    script_dir = Path(__file__).parent.absolute()
    extractions_path = script_dir / 'pfizer_extractions_under_20_pages.csv'
    vector_store_path = script_dir / 'vector_store'
    
    # Check if extractions file exists
    if not extractions_path.exists():
        print(f"Error: {extractions_path} not found")
        print("Please run main.py first to generate the extractions")
        return
    
    # Initialize vector store
    print("\nInitializing vector store...")
    vector_store = DenseVectorStore(str(vector_store_path))
    
    # Process extractions
    print("\nProcessing extractions and creating dense vectors...")
    vector_store.process_extractions(str(extractions_path))
    
    # Print vector store stats
    stats = vector_store.get_stats()
    print("\nVector Store Statistics:")
    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Collection name: {stats['name']}")
    print(f"Collection metadata: {stats['metadata']}")
    
    # Test search
    print("\nTesting search functionality...")
    test_queries = [
        "What are the side effects?",
        "What is the recommended dosage?",
        "How should the medication be stored?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = vector_store.search(query)
        
        for i, result in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"Text: {result['chunk'][:200]}...")
            print(f"Source: {result['metadata']['file_path']}")
            print(f"Chunk: {result['metadata']['chunk_index'] + 1}/{result['metadata']['total_chunks']}")
            if result['distance'] is not None:
                print(f"Distance: {result['distance']:.4f}")

if __name__ == "__main__":
    main() 