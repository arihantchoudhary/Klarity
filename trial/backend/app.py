import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from .document_processor import DocumentProcessor
from .vector_store import DenseVectorIndexer
from .rag_chatbot import RAGChatbot

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Check required environment variables
required_env_vars = ['OPENAI_API_KEY']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# HTML template for the home page
HOME_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Klarity RAG API Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; margin-top: 30px; }
        .endpoint {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .method {
            font-weight: bold;
            color: #2980b9;
        }
        .path {
            color: #27ae60;
            font-family: monospace;
        }
        code {
            background: #eee;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <h1>Klarity RAG API Documentation</h1>
    
    <h2>Document Processing Endpoints</h2>
    
    <div class="endpoint">
        <p><span class="method">POST</span> <span class="path">/api/process-document</span></p>
        <p>Upload and process a PDF document.</p>
        <p>Request: Form data with 'file' field containing PDF file</p>
        <p>Response: JSON with processing statistics</p>
    </div>

    <div class="endpoint">
        <p><span class="method">GET</span> <span class="path">/api/pfizer-files</span></p>
        <p>List PDF files in a directory.</p>
        <p>Query params: <code>directory</code> - Path to directory</p>
        <p>Response: JSON array of file names</p>
    </div>

    <div class="endpoint">
        <p><span class="method">GET</span> <span class="path">/api/file-contents</span></p>
        <p>Get contents of a file.</p>
        <p>Query params: <code>path</code> - Path to file</p>
        <p>Response: JSON with file content</p>
    </div>

    <div class="endpoint">
        <p><span class="method">POST</span> <span class="path">/api/save-file</span></p>
        <p>Save edited file contents.</p>
        <p>Request body: JSON with <code>path</code> and <code>content</code> fields</p>
        <p>Response: JSON success status</p>
    </div>

    <h2>Chat Interface Endpoints</h2>

    <div class="endpoint">
        <p><span class="method">POST</span> <span class="path">/api/chat</span></p>
        <p>Send a message to the RAG chatbot.</p>
        <p>Request body: JSON with <code>message</code> field</p>
        <p>Response: JSON with chatbot response</p>
    </div>

    <div class="endpoint">
        <p><span class="method">GET</span> <span class="path">/api/chat/history</span></p>
        <p>Get chat history.</p>
        <p>Response: JSON array of chat messages</p>
    </div>

    <div class="endpoint">
        <p><span class="method">POST</span> <span class="path">/api/chat/clear</span></p>
        <p>Clear chat history.</p>
        <p>Response: JSON success status</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Render the API documentation page."""
    return render_template_string(HOME_PAGE_TEMPLATE)

# Initialize components
BASE_DIR = Path(__file__).parent.parent
UPLOAD_FOLDER = BASE_DIR / 'uploads'
VECTOR_STORE_DIR = BASE_DIR / 'vector_store'
CONTENT_DIR = BASE_DIR / 'content'

for directory in [UPLOAD_FOLDER, VECTOR_STORE_DIR, CONTENT_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

try:
    processor = DocumentProcessor(output_path=str(CONTENT_DIR))
    vector_store = DenseVectorIndexer(persist_directory=str(VECTOR_STORE_DIR))
    chatbot = RAGChatbot(vector_store=vector_store)
    logger.info("Successfully initialized all components")
except Exception as e:
    logger.error(f"Error initializing components: {str(e)}")
    raise

@app.route('/api/pfizer-files', methods=['GET'])
def list_pfizer_files():
    """List files in a Pfizer directory."""
    directory = request.args.get('directory')
    if not directory or not os.path.exists(directory):
        return jsonify({"error": "Invalid directory"}), 400
    
    try:
        files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
        logger.info(f"Found {len(files)} PDF files in {directory}")
        return jsonify({"files": files})
    except Exception as e:
        logger.error(f"Error listing files in {directory}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/file-contents', methods=['GET'])
def get_file_contents():
    """Get the contents of a file."""
    file_path = request.args.get('path')
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "Invalid file path"}), 400
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"content": content})
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/save-file', methods=['POST'])
def save_file():
    """Save file contents."""
    data = request.json
    if not data or 'path' not in data or 'content' not in data:
        return jsonify({"error": "Missing path or content"}), 400
    
    try:
        with open(data['path'], 'w', encoding='utf-8') as f:
            f.write(data['content'])
        logger.info(f"Successfully saved file {data['path']}")
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Error saving file {data.get('path')}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/process-document', methods=['POST'])
def process_document():
    """Process a document and add it to the vector store."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        file_path = str(UPLOAD_FOLDER / filename)
        file.save(file_path)
        logger.info(f"Saved uploaded file to {file_path}")
        
        # Process document
        texts, tables, images = processor.process_pdf(file_path)
        logger.info(f"Processed {filename}: {len(texts)} texts, {len(tables)} tables, {len(images)} images")
        
        # Convert texts to strings and add metadata
        text_strings = []
        metadatas = []
        for text in texts:
            text_strings.append(str(text))
            metadatas.append({
                "source": filename,
                "type": "text"
            })
        
        # Add to vector store
        vector_store.add_texts(text_strings, metadatas)
        logger.info(f"Added {len(text_strings)} text chunks to vector store")
        
        return jsonify({
            "success": True,
            "stats": {
                "texts": len(texts),
                "tables": len(tables),
                "images": len(images)
            }
        })
    except Exception as e:
        logger.error(f"Error processing document {file.filename}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process a chat message."""
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        response = chatbot.query(data['message'])
        logger.info(f"Generated response for message: {data['message'][:50]}...")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    """Get chat history."""
    try:
        history = chatbot.get_chat_history()
        return jsonify({"history": history})
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/clear', methods=['POST'])
def clear_chat_history():
    """Clear chat history."""
    try:
        chatbot.clear_memory()
        logger.info("Cleared chat history")
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Error clearing chat history: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 