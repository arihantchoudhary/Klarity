import numpy as np
from sklearn.cluster import KMeans
import faiss
import torch
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import pickle
import os
import chardet

class TextProcessor:
    """Process text documents for vector indexing."""
    
    def __init__(self, chunk_size=512, chunk_overlap=100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text_from_document(self, document_path):
        """Extract text from a document with automatic encoding detection."""
        try:
            # First detect the encoding
            with open(document_path, 'rb') as file:
                raw_data = file.read()
                detected = chardet.detect(raw_data)
                encoding = detected['encoding'] or 'utf-8'
            
            # Then read with the detected encoding
            with open(document_path, 'r', encoding=encoding, errors='replace') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file {document_path}: {e}")
            # Create a simple fallback if reading fails
            return "Sample text for indexing demonstration."
    
    def chunk_text(self, text):
        """Split text into chunks with overlap."""
        words = text.split()
        chunks = []
        
        i = 0
        while i < len(words):
            chunk = ' '.join(words[i:i + self.chunk_size])
            chunks.append(chunk)
            i += self.chunk_size - self.chunk_overlap
            
        return chunks or ["Sample chunk for indexing demonstration."]

class EmbeddingModel:
    """Generate embeddings for text chunks."""
    
    def __init__(self, model_name="sentence-transformers/all-mpnet-base-v2", use_mock=False):
        self.use_mock = use_mock or (os.environ.get("USE_MOCK_EMBEDDINGS", "false").lower() == "true")
        if not self.use_mock:
            try:
                self.model = SentenceTransformer(model_name)
                # Test the model to ensure it works
                _ = self.model.encode("test")
                self.embedding_dim = self.model.get_sentence_embedding_dimension()
            except Exception as e:
                print(f"Error loading model {model_name}: {e}. Using mock embeddings instead.")
                self.model = None
                self.use_mock = True
                self.embedding_dim = 384
        else:
            self.model = None
            self.embedding_dim = 384
    
    def generate_embeddings(self, chunks):
        """Generate embeddings for a list of text chunks."""
        embeddings = []
        
        if self.model is None:
            # Mock embeddings for demonstration
            print("Using mock embeddings for demonstration")
            for _ in tqdm(chunks, desc="Generating mock embeddings"):
                embedding = np.random.randn(self.embedding_dim).astype('float32')
                embedding = embedding / np.linalg.norm(embedding)  # Normalize
                embeddings.append(embedding)
        else:
            # Real embeddings
            for chunk in tqdm(chunks, desc="Generating embeddings"):
                embedding = self.model.encode(chunk)
                embeddings.append(embedding)
        
        return np.array(embeddings, dtype='float32')

class VectorIndex:
    """Base class for vector indexing methods."""
    
    def __init__(self, embedding_dim):
        self.embedding_dim = embedding_dim
        self.index = None
    
    def build_index(self, embeddings):
        """Build the index from embeddings."""
        pass
    
    def search(self, query_embedding, top_k=5):
        """Search the index with a query embedding."""
        pass
    
    def save(self, path):
        """Save the index to disk."""
        with open(path, 'wb') as f:
            pickle.dump(self.index, f)
    
    def load(self, path):
        """Load the index from disk."""
        with open(path, 'rb') as f:
            self.index = pickle.load(f)

class FlatIndex(VectorIndex):
    """Flat index for exact search."""
    
    def build_index(self, embeddings):
        """Build a flat index."""
        try:
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.index.add(embeddings)
        except Exception as e:
            print(f"Error building flat index: {e}")
    
    def search(self, query_embedding, top_k=5):
        """Search the flat index."""
        try:
            if self.index is None or self.index.ntotal == 0:
                return np.zeros(top_k), np.zeros(top_k, dtype=int)
                
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            distances, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
            return distances[0], indices[0]
        except Exception as e:
            print(f"Error searching flat index: {e}")
            return np.zeros(top_k), np.zeros(top_k, dtype=int)

class LSHIndex(VectorIndex):
    """Locality-Sensitive Hashing index."""
    
    def __init__(self, embedding_dim, n_bits=8, n_tables=10):
        super().__init__(embedding_dim)
        self.n_bits = n_bits
        self.n_tables = n_tables
    
    def build_index(self, embeddings):
        """Build an LSH index."""
        try:
            self.index = faiss.IndexLSH(self.embedding_dim, self.n_bits * self.n_tables)
            self.index.add(embeddings)
        except Exception as e:
            print(f"Error building LSH index: {e}")
    
    def search(self, query_embedding, top_k=5):
        """Search the LSH index."""
        try:
            if self.index is None or self.index.ntotal == 0:
                return np.zeros(top_k), np.zeros(top_k, dtype=int)
                
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            distances, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
            return distances[0], indices[0]
        except Exception as e:
            print(f"Error searching LSH index: {e}")
            return np.zeros(top_k), np.zeros(top_k, dtype=int)

class IVFIndex(VectorIndex):
    """Inverted File Index using clustering."""
    
    def __init__(self, embedding_dim, n_clusters=100):
        super().__init__(embedding_dim)
        self.n_clusters = n_clusters
    
    def build_index(self, embeddings):
        """Build an IVF index."""
        try:
            self.n_clusters = min(self.n_clusters, int(embeddings.shape[0] / 39))
            self.n_clusters = max(1, self.n_clusters)
            quantizer = faiss.IndexFlatL2(self.embedding_dim)
            self.index = faiss.IndexIVFFlat(quantizer, self.embedding_dim, self.n_clusters)
            self.index.train(embeddings)
            self.index.add(embeddings)
            self.index.nprobe = min(10, self.n_clusters)
        except Exception as e:
            print(f"Error building IVF index: {e}")
    
    def search(self, query_embedding, top_k=5):
        """Search the IVF index."""
        try:
            if self.index is None or self.index.ntotal == 0:
                return np.zeros(top_k), np.zeros(top_k, dtype=int)
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            distances, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
            return distances[0], indices[0]
        except Exception as e:
            print(f"Error searching IVF index: {e}")
            return np.zeros(top_k), np.zeros(top_k, dtype=int)

class IVFPQIndex(VectorIndex):
    """Inverted File with Product Quantization for more efficient search."""
    
    def __init__(self, embedding_dim, n_clusters=100, subquantizer_bits=8, n_subquantizers=8):
        super().__init__(embedding_dim)
        self.n_clusters = n_clusters
        self.subquantizer_bits = subquantizer_bits
        self.n_subquantizers = min(n_subquantizers, embedding_dim)
    
    def build_index(self, embeddings):
        """Build an IVFPQ index."""
        try:
            self.n_clusters = min(self.n_clusters, int(embeddings.shape[0] / 39))
            self.n_clusters = max(1, self.n_clusters)
            quantizer = faiss.IndexFlatL2(self.embedding_dim)
            self.n_subquantizers = min(self.n_subquantizers, self.embedding_dim)
            while self.embedding_dim % self.n_subquantizers != 0:
                self.n_subquantizers -= 1
            self.index = faiss.IndexIVFPQ(quantizer, self.embedding_dim, self.n_clusters, self.n_subquantizers, self.subquantizer_bits)
            self.index.train(embeddings)
            self.index.add(embeddings)
            self.index.nprobe = min(10, self.n_clusters)
        except Exception as e:
            print(f"Error building IVFPQ index: {e}")
    
    def search(self, query_embedding, top_k=5):
        """Search the IVFPQ index."""
        try:
            if self.index is None or self.index.ntotal == 0:
                return np.zeros(top_k), np.zeros(top_k, dtype=int)
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            distances, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
            return distances[0], indices[0]
        except Exception as e:
            print(f"Error searching IVFPQ index: {e}")
            return np.zeros(top_k), np.zeros(top_k, dtype=int)

class HNSWIndex(VectorIndex):
    """Hierarchical Navigable Small World index."""
    
    def __init__(self, embedding_dim, M=16, efConstruction=200):
        super().__init__(embedding_dim)
        self.M = M
        self.efConstruction = efConstruction
    
    def build_index(self, embeddings):
        """Build an HNSW index."""
        try:
            self.index = faiss.IndexHNSWFlat(self.embedding_dim, self.M)
            self.index.hnsw.efConstruction = self.efConstruction
            self.index.add(embeddings)
            self.index.hnsw.efSearch = 64
        except Exception as e:
            print(f"Error building HNSW index: {e}")
    
    def search(self, query_embedding, top_k=5):
        """Search the HNSW index."""
        try:
            if self.index is None or self.index.ntotal == 0:
                return np.zeros(top_k), np.zeros(top_k, dtype=int)
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            distances, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
            return distances[0], indices[0]
        except Exception as e:
            print(f"Error searching HNSW index: {e}")
            return np.zeros(top_k), np.zeros(top_k, dtype=int)

class RAGSystem:
    """Retrieval-Augmented Generation system using vector indexing."""
    
    def __init__(self, text_processor, embedding_model, vector_index, chunk_texts=None, embeddings=None):
        self.text_processor = text_processor
        self.embedding_model = embedding_model
        self.vector_index = vector_index
        self.chunk_texts = chunk_texts or []
        self.embeddings = embeddings
    
    def process_documents(self, document_paths):
        """Process multiple documents and build the index."""
        all_chunks = []
        
        for path in document_paths:
            try:
                text = self.text_processor.extract_text_from_document(path)
                chunks = self.text_processor.chunk_text(text)
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"Error processing document {path}: {e}")
        
        if not all_chunks:
            print("No valid chunks found. Creating a sample chunk for demonstration.")
            all_chunks = ["Sample chunk for demonstration purposes."]
        
        self.chunk_texts = all_chunks
        self.embeddings = self.embedding_model.generate_embeddings(all_chunks)
        
        try:
            self.vector_index.build_index(self.embeddings)
            print(f"Successfully processed {len(document_paths)} documents into {len(all_chunks)} chunks.")
        except Exception as e:
            print(f"Error building index: {e}")
    
    def retrieve(self, query, top_k=5):
        """Retrieve relevant chunks for a query."""
        try:
            query_embedding = self.embedding_model.generate_embeddings([query])[0]
            distances, indices = self.vector_index.search(query_embedding, top_k)
            results = []
            for i, idx in enumerate(indices):
                if idx >= 0 and idx < len(self.chunk_texts):
                    results.append({
                        'chunk': self.chunk_texts[idx],
                        'distance': float(distances[i]),
                        'index': int(idx)
                    })
            return results
        except Exception as e:
            print(f"Error retrieving results: {e}")
            return []
    
    def enhance_query(self, query):
        """Enhance the query with additional context."""
        enhanced_query = f"In the context of information retrieval and vector databases: {query}"
        return enhanced_query

def create_sample_document(document_path):
    """Create a sample document for testing purposes."""
    sample_text = """
Vector indexing is a critical component of modern information retrieval systems.

The flat index is the simplest approach, where we store vectors as-is and compare directly.

Locality Sensitive Hashing (LSH) groups similar vectors into buckets using hash functions.

Inverted File (IVF) indexing uses clustering to organize vectors, allowing for faster retrieval.

Inverted File with Product Quantization (IVFPQ) further compresses vectors for efficient storage.

Hierarchical Navigable Small World (HNSW) creates a multi-layered graph that enables efficient nearest neighbor search.
    """
    try:
        with open(document_path, 'w', encoding='utf-8') as f:
            f.write(sample_text.strip())
        print(f"Sample document created at {document_path}")
    except Exception as e:
        print(f"Error creating sample document: {e}")

if __name__ == "__main__":
    # Example usage of the indexing system
    processor = TextProcessor(chunk_size=100, chunk_overlap=20)
    model = EmbeddingModel(use_mock=True)
    index = FlatIndex(model.embedding_dim)
    rag_system = RAGSystem(processor, model, index)
    
    sample_doc_path = "sample_document.txt"
    create_sample_document(sample_doc_path)
    
    rag_system.process_documents([sample_doc_path])
    
    query = "nearest neighbor search"
    results = rag_system.retrieve(query)
    
    print("Query Results:")
    for res in results:
        print(res)
