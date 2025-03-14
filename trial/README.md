# Klarity Document Assistant

A powerful document processing and analysis system that combines RAG (Retrieval-Augmented Generation) capabilities with an intuitive user interface for document management, editing, and intelligent querying.

## Features

- **Document Processing**

  - Upload PDF documents individually or in bulk
  - Automatic text extraction and processing
  - Dense vector indexing for efficient retrieval
  - Document content storage and management

- **Interactive Interface**

  - Three-panel layout for optimal workflow
  - Document list and management (Left panel)
  - Document viewer and editor (Middle panel)
  - RAG-powered chatbot (Right panel)

- **RAG Chatbot**
  - Context-aware responses based on uploaded documents
  - Intelligent document retrieval
  - Conversation memory and history
  - Source attribution for responses

## Project Structure

```
trial/
├── backend/
│   ├── __init__.py           # Package initialization
│   ├── app.py               # Flask server and API endpoints
│   ├── document_processor.py # PDF processing and text extraction
│   ├── vector_store.py      # Dense vector indexing with ChromaDB
│   └── rag_chatbot.py       # RAG implementation with LangChain
├── static/
│   └── brain-icon.svg       # UI assets
├── uploads/                 # Document storage directory
├── vector_store/           # ChromaDB storage
├── content/               # Processed document content
├── index.html            # Main application interface
├── styles.css            # Application styling
├── script.js             # Frontend functionality
└── requirements.txt      # Python dependencies
```

## Technology Stack

- **Backend**

  - Flask (Web server)
  - LangChain (RAG implementation)
  - ChromaDB (Vector store)
  - OpenAI API (Language model)
  - Unstructured (Document processing)

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript (Vanilla)
  - Font Awesome (Icons)

## Setup and Installation

1. **Environment Setup**

   ```bash
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **System Dependencies**

   ```bash
   # On macOS (using Homebrew)
   brew install poppler tesseract

   # On Ubuntu/Debian
   sudo apt-get install poppler-utils tesseract-ocr
   ```

3. **Environment Variables**
   Create a `.env` file in the trial directory:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Running the Application**

   ```bash
   # Start the Flask server
   cd trial
   python -m backend.app
   ```

5. **Accessing the Application**
   - Open `http://127.0.0.1:5000` in your web browser
   - The API documentation is available at the root URL

## API Endpoints

### Document Processing

- `POST /api/process-document`: Upload and process PDF documents
- `GET /api/pfizer-files`: List available PDF files
- `GET /api/file-contents`: Retrieve document contents
- `POST /api/save-file`: Save edited document contents

### Chat Interface

- `POST /api/chat`: Send messages to the RAG chatbot
- `GET /api/chat/history`: Retrieve chat history
- `POST /api/chat/clear`: Clear chat history

## Usage Guide

1. **Document Upload**

   - Use the "Upload File" button to select PDF documents
   - Files are automatically processed and indexed
   - Processed documents appear in the left panel

2. **Document Viewing/Editing**

   - Click on a document in the left panel to view/edit
   - Use the Save button to persist changes
   - Content is automatically formatted for readability

3. **RAG Chat**
   - Type questions in the chat input
   - The system retrieves relevant context from documents
   - Responses are generated using the RAG architecture
   - Chat history is maintained for context

## Development

The application uses a modular architecture:

- `document_processor.py`: Handles PDF processing, text extraction, and content organization
- `vector_store.py`: Manages document indexing and retrieval using dense vectors
- `rag_chatbot.py`: Implements the RAG system using LangChain and OpenAI
- `app.py`: Provides the REST API interface and server functionality

## Error Handling

The application includes comprehensive error handling:

- Input validation for all API endpoints
- Graceful handling of processing errors
- Informative error messages
- Logging for debugging and monitoring

## Security Considerations

- Environment variables for sensitive data
- Input sanitization
- CORS protection
- File type validation
- Secure file handling

## Future Improvements

- [ ] Add support for more document formats
- [ ] Implement user authentication
- [ ] Add document categorization
- [ ] Enhance editor capabilities
- [ ] Add document collaboration features
- [ ] Implement real-time updates
- [ ] Add export functionality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
