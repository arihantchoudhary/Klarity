# PDF Processing and Vector Indexing System

This system extracts content from PDF files and creates a searchable vector index for dense semantic search capabilities.

## Components

- **pdf_parser.py**: Enhanced PDF parser with detailed documentation for extracting text, tables, and figures
- **create_file_inventory.py**: Creates a catalog of files in a directory with metadata
- **create_vector_index.py**: Processes files, extracts content chunks, and creates a vector index
- **vector_indexing_plan.md**: Documentation of the vector indexing approach
- **test_*.py files**: Test scripts to verify component functionality

## Installation

1. Ensure you have Python 3.7+ installed
2. Install required dependencies:

```bash
pip install pdfplumber xgboost numpy pypdf Pillow
pip install pandas tqdm

# Optional but recommended for vector indexing:
pip install sentence-transformers faiss-cpu

# For testing with sample PDF generation:
pip install fpdf
```

## Quick Start

### Basic Workflow:

1. Run inventory creation to catalog PDF files:
```bash
python create_file_inventory.py
```

2. Run vector indexing to extract content and create searchable index:
```bash
python create_vector_index.py
```

## Testing

Use the test scripts to verify each component works correctly:

1. Test the PDF parser:
```bash
python test_pdf_parser.py
```

2. Test the file inventory and vector indexing:
```bash
python test_indexing.py
```

3. Test specific components:
```bash
python test_indexing.py --component=inventory
python test_indexing.py --component=vector
```

## Debugging

### Common Issues

1. **Import Errors**: Make sure all required packages are installed and file paths are correct.
2. **PDF Parsing Issues**: Some PDFs may be protected or have complex layouts that are difficult to parse.
3. **Vector Library Errors**: If vector libraries are not installed, the system will use simulated embeddings.

### Troubleshooting

1. Check logs for detailed error messages
2. Ensure all test directories are properly created
3. Try with simpler PDF files first
4. For PDF parser issues, verify the PDF is not encrypted
5. For vector indexing issues, verify sentence-transformers and faiss-cpu are installed correctly

## Architecture

The system follows a pipeline architecture:

1. **File Inventory**: Scans and catalogs files with metadata
2. **Content Extraction**: Processes PDFs to extract text, tables, and figures
3. **Content Chunking**: Splits content into semantic chunks for embedding
4. **Vector Embedding**: Generates dense vector representations of chunks
5. **Vector Indexing**: Creates a searchable index for similarity retrieval

## Directory Structure

```
work-trial-final/
├── pdf_parser.py                 # Enhanced PDF parser
├── create_file_inventory.py      # File inventory creator
├── create_vector_index.py        # Vector indexing implementation
├── vector_indexing_plan.md       # Vector indexing documentation
├── README.md                     # This file
├── file_inventory.csv            # Generated file inventory
├── test_pdf_parser.py            # PDF parser test script
├── test_indexing.py              # Indexing test script
├── test_data/                    # Test data directory
│   ├── sample_document.txt       # Sample text for testing
│   ├── uploads/                  # Test uploads directory
│   └── output/                   # Test output directory
└── vector_index/                 # Generated vector index directory
```

## Custom Usage

You can customize the system for your specific needs:

1. Modify chunk sizes in `create_vector_index.py` for different embedding granularity
2. Use different embedding models by changing the model name in `VectorIndexer`
3. Add custom file categorization logic in `FileInventoryCreator.guess_file_category()`
4. Extend the table extraction capabilities in `ChunkExtractor.process_tables()`
