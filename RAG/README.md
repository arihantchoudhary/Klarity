# PDF RAG System with Enhanced Formatting

This application allows you to upload PDF documents, extract text, and ask questions about their content using GPT-powered semantic search and retrieval. It features automatic formatting improvements and a dual-view interface for both editing and viewing formatted content.

## Features

- **PDF Text Extraction**: Upload and process PDF documents
- **AI-Powered RAG**: ChromaDB vector database with semantic search capabilities
- **Smart Text Formatting**: GPT-enhanced formatting with proper spacing and grammar
- **Dual-View Interface**: Toggle between editing and formatted viewing modes
- **Automatic Header Recognition**: Bold highlighting of headers and key information
- **Question Answering**: Ask questions about the document content

## Requirements

- Python 3.8+
- OpenAI API key

## Installation

1. Clone the repository and navigate to the project directory
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the application:
   ```
   python app.py
   ```
2. Open your browser and navigate to http://localhost:5002
3. Upload a PDF document using the form
4. Navigate through pages using the toolbar
5. Toggle between edit and formatted views with the "Toggle Formatted View" button
6. Ask questions about the document content using the sidebar form
7. Edit text as needed and save changes

## How It Works

The system uses several layers of processing:

1. **PDF Extraction**: Text is extracted from PDFs while preserving structure
2. **Formatting Enhancement**: GPT improves formatting, spacing, and grammar 
3. **Vector Indexing**: Text is chunked and stored in ChromaDB with embeddings
4. **Semantic Retrieval**: When you ask a question, relevant sections are retrieved
5. **Response Generation**: GPT generates answers based on the retrieved content

The dual-view interface lets you edit text directly or view a formatted version with automatic header recognition and styling.

## File Structure

- `app.py`: Main application file
- `requirements.txt`: Required dependencies
- `uploads/`: Directory for uploaded PDFs
- `uploads/edits/`: Directory for saved text edits
