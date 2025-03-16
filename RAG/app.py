import os
import random
import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import chromadb
from chromadb.utils import embedding_functions
import openai
from flask import Flask, request, render_template_string, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import PyPDF2

# Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")  # Set your API key as an environment variable
openai.api_key = OPENAI_API_KEY

# Flask app config
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Create directory for edited text
EDITS_FOLDER = os.path.join(app.config['UPLOAD_FOLDER'], 'edits')
os.makedirs(EDITS_FOLDER, exist_ok=True)

# File extensions we support
ALLOWED_EXTENSIONS = {'pdf'}

# Global RAG system
rag_system = None

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    text = ""
    page_texts = []
    page_htmls = []
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                # Format the text with HTML tags for better display
                # Use heuristics to identify headers and format them as bold
                lines = page_text.split('\n')
                html_lines = []
                
                for line in lines:
                    # Skip empty lines
                    if not line.strip():
                        html_lines.append('<br>')
                        continue
                    
                    # Identify potential headers (shorter lines without punctuation or specific keywords)
                    line_stripped = line.strip()
                    is_header = (
                        (len(line_stripped) < 50 and not any(p in line_stripped for p in ".,;:?!/")) or
                        any(keyword in line_stripped.lower() for keyword in ["experience", "education", "skills", "project", "work", "research", "contact", "engineering", "objective", "profile", "summary"]) or
                        line_stripped.isupper() or
                        line_stripped.endswith(':')
                    )
                    
                    if is_header:
                        html_lines.append(f"<strong>{line}</strong>")
                    else:
                        html_lines.append(line)
                
                formatted_html = "<br>".join(html_lines)
                page_htmls.append(formatted_html)
                page_texts.append(page_text)
                text += page_text + "\n\n"
                
        # Add page numbers for context
        text_with_page_numbers = ""
        for i, page_content in enumerate(page_texts):
            if page_content.strip():  # Only add non-empty pages
                text_with_page_numbers += f"--- Page {i+1} ---\n{page_content}\n\n"
                
        return text_with_page_numbers, page_texts, page_htmls
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return "", [], []

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into chunks of specified size with overlap"""
    if not text:
        return []
    
    # First split by pages
    pages = text.split("--- Page ")
    
    chunks = []
    for page in pages:
        if not page.strip():
            continue
            
        # Try to parse the page number
        try:
            page_parts = page.split("---\n", 1)
            page_num = page_parts[0].strip()
            page_content = page_parts[1] if len(page_parts) > 1 else page
        except:
            page_num = "Unknown"
            page_content = page
            
        # If the page content is short enough, use it as a chunk
        if len(page_content) <= chunk_size:
            chunks.append(f"Page {page_num}: {page_content}")
        else:
            # Otherwise, split the page into overlapping chunks
            words = page_content.split()
            words_per_chunk = chunk_size // 7  # Approx. avg word length of 7 chars
            overlap_words = overlap // 7
            
            for i in range(0, len(words), words_per_chunk - overlap_words):
                chunk = " ".join(words[i:i + words_per_chunk])
                chunks.append(f"Page {page_num} (part): {chunk}")
    
    return chunks

def get_pdf_info(pdf_path):
    """Get basic information about a PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
        return {
            "path": pdf_path,
            "filename": os.path.basename(pdf_path),
            "num_pages": num_pages,
            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        print(f"Error getting PDF info: {e}")
        return None

def get_edited_text(pdf_filename, page_num):
    """Get previously edited text for a PDF page if it exists"""
    edit_filename = f"{os.path.splitext(pdf_filename)[0]}_page{page_num}_text.txt"
    edit_path = os.path.join(EDITS_FOLDER, edit_filename)
    
    if os.path.exists(edit_path):
        with open(edit_path, 'r') as f:
            return f.read()
    return None

class PDFRagSystem:
    def __init__(self, pdf_path=None):
        """Initialize the RAG system with optional PDF path"""
        self.client = chromadb.Client()
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.reset_collection()
        
        # Process PDF if provided
        if pdf_path:
            self.process_pdf(pdf_path)
    
    def reset_collection(self):
        """Reset/initialize the vector store collection"""
        # Check if collection exists and delete it
        try:
            collections = self.client.list_collections()
            for collection in collections:
                if collection.name == "pdf_content":
                    self.client.delete_collection("pdf_content")
            print("Deleted existing collection")
        except:
            pass
            
        # Create a new collection
        self.collection = self.client.create_collection(
            name="pdf_content",
            embedding_function=self.embedding_function
        )
        print("Created new collection")
        
        # Track PDF info
        self.current_pdf = None
    
    def process_pdf(self, pdf_path):
        """Process a PDF file and add its content to the vector database"""
        if not os.path.exists(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            return False
        
        # Extract text from PDF
        pdf_text, page_texts, page_htmls = extract_text_from_pdf(pdf_path)
        if not pdf_text:
            print(f"Could not extract text from PDF: {pdf_path}")
            return False
        
        # Split text into chunks
        chunks = chunk_text(pdf_text)
        if not chunks:
            print(f"No content chunks generated from PDF: {pdf_path}")
            return False
        
        # Store PDF info
        self.current_pdf = get_pdf_info(pdf_path)
        if not self.current_pdf:
            print(f"Failed to get PDF info: {pdf_path}")
            return False
            
        self.current_pdf["num_chunks"] = len(chunks)
        self.current_pdf["page_texts"] = page_texts
        self.current_pdf["page_htmls"] = page_htmls
        
        # Add chunks to collection
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        documents = chunks
        metadatas = [{
            "chunk_index": i,
            "pdf_filename": self.current_pdf["filename"],
            "source": f"Chunk {i} from {self.current_pdf['filename']}"
        } for i in range(len(chunks))]
        
        # Add data to collection
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        
        print(f"Successfully processed PDF with {len(chunks)} chunks")
        return True
    
    def query(self, question, n_results=5):
        """Query the vector database for relevant chunks"""
        results = self.collection.query(
            query_texts=[question],
            n_results=n_results
        )
        
        return results
    
    def generate_answer(self, question, context_docs):
        """Generate an answer using OpenAI API"""
        context = "\n\n".join(context_docs)
        
        # Call OpenAI to generate a response
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided PDF content. Always cite the page number when referencing information from the document."},
                {"role": "user", "content": f"Based on the following PDF content, please answer this question: {question}\n\nPDF Content:\n{context}"}
            ],
            temperature=0.3,
        )
        
        return response.choices[0].message.content
    
    def answer_question(self, question):
        """Answer a question based on PDF content"""
        # Check if there's content in the database
        if not self.current_pdf:
            return "No PDF has been uploaded yet. Please upload a PDF document first."
        
        # Query database for relevant context
        results = self.query(question)
        
        if not results or not results["documents"] or not results["documents"][0]:
            return "I couldn't find any relevant information in the PDF to answer your question."
        
        # Generate answer using OpenAI
        context_docs = results["documents"][0]
        answer = self.generate_answer(question, context_docs)
        
        return answer
    
    def get_page_text(self, page_num):
        """Get text for a specific page"""
        if not self.current_pdf or not self.current_pdf.get("page_texts"):
            return ""
            
        if 0 <= page_num - 1 < len(self.current_pdf["page_texts"]):
            # Check if there's an edited version
            edited_text = get_edited_text(self.current_pdf["filename"], page_num)
            if edited_text:
                return edited_text
            
            # Get the original text
            original_text = self.current_pdf["page_texts"][page_num - 1]
            
            # Use GPT to improve formatting
            improved_text = self.improve_text_formatting(original_text)
            return improved_text
        
        return ""
    
    def improve_text_formatting(self, text):
        """Use GPT to improve text formatting, grammar, and readability"""
        if not text.strip():
            return text
            
        try:
            # Call OpenAI to improve the formatting
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are a document formatting assistant specializing in resumes and technical documents. Your task is to fix formatting issues that typically occur when extracting text from PDFs:
                    
1. Add proper spacing between words that are incorrectly joined (e.g., "MULTiMODALGENAIRESEARCHER" → "MULTIMODAL GENAI RESEARCHER")
2. Format bullet points properly with spaces after them
3. Fix line breaks and paragraph spacing
4. Correct special characters that appear incorrectly
5. Preserve the structure of headers, sections, and important information
6. Use bold formatting for headers, section titles, and important terms
                    
Carefully analyze the text and fix these formatting issues while preserving the original content."""},
                    {"role": "user", "content": f"This text was extracted from a PDF resume and has formatting issues. Please fix the spacing, line breaks, and special characters while maintaining the document structure. Mark headers and important sections with **bold**:\n\n{text}"}
                ],
                temperature=0.3,
                max_tokens=2000,
            )
            
            improved_text = response.choices[0].message.content
            
            # Replace markdown-style bold with proper text
            improved_text = improved_text.replace("**", "")
            
            return improved_text
        except Exception as e:
            print(f"Error improving text formatting: {e}")
            return text  # Return original text on error

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PDF RAG System</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background-color: #4285f4;
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        h1 {
            color: white;
            margin: 0;
            font-size: 1.5rem;
        }
        .main-container {
            display: flex;
            flex: 1;
            overflow: hidden;
        }
        .sidebar {
            width: 300px;
            padding: 20px;
            background-color: #f5f5f5;
            overflow-y: auto;
            border-right: 1px solid #ddd;
        }
        .pdf-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            background-color: #f9f9f9;
            overflow: hidden;
        }
        .toolbar {
            background-color: #f1f1f1;
            padding: 10px;
            border-bottom: 1px solid #ddd;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
        }
        .text-editor {
            flex: 1;
            overflow: auto;
            display: flex;
            flex-direction: column;
            background-color: #e0e0e0;
            padding: 20px;
        }
        .pdf-page {
            background-color: white;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            margin: 0 auto;
            width: 100%;
            height: 100%;
            position: relative;
            display: flex;
            flex-direction: column;
        }
        #text-content {
            width: 100%;
            flex: 1;
            padding: 40px;
            box-sizing: border-box;
            border: none;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.5;
            background-color: white;
            white-space: pre-wrap;
            overflow-wrap: break-word;
            tab-size: 4;
            -moz-tab-size: 4;
            resize: none;
            overflow: auto;
        }
        #html-content {
            width: 100%;
            flex: 1;
            padding: 40px;
            box-sizing: border-box;
            border: none;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.5;
            background-color: white;
            overflow: auto;
        }
        #html-content strong {
            font-weight: 800; /* Increase font weight from bold (700) to extra-bold (800) */
            color: #000; /* Change from blue to black for stronger contrast */
            font-size: 1.1em; /* Slightly larger text */
            display: block; /* Make headers block elements for better spacing */
            margin-top: 10px;
            margin-bottom: 5px;
        }
        .page-header {
            padding: 10px 40px;
            border-bottom: 1px solid #ddd;
            background-color: #f9f9f9;
            font-size: 12px;
            color: #666;
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"], input[type="file"] {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button, input[type="submit"] {
            background-color: #4285f4;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 15px;
            cursor: pointer;
            margin-right: 5px;
            margin-bottom: 5px;
        }
        button:hover, input[type="submit"]:hover {
            background-color: #3367d6;
        }
        .save-btn {
            background-color: #0f9d58;
        }
        .save-btn:hover {
            background-color: #0b8043;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 5px;
            white-space: pre-wrap;
            border: 1px solid #ddd;
        }
        .file-status {
            background-color: #e9f7fe;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            border: 1px solid #a8d4f5;
        }
        .error {
            color: #d32f2f;
            background-color: #ffebee;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            border: 1px solid #f5c6cb;
        }
        /* Navigation controls */
        .nav-controls {
            display: flex;
            align-items: center;
        }
        #page-num {
            margin: 0 10px;
            width: 40px;
            text-align: center;
        }
        .status-message {
            margin-left: 20px;
            color: #0b8043;
            font-weight: bold;
            opacity: 0;
            transition: opacity 0.5s ease-in-out;
        }
        .status-message.visible {
            opacity: 1;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>PDF RAG System</h1>
    </div>

    <div class="main-container">
        <div class="sidebar">
            <!-- PDF Upload Form -->
            <div class="form-group">
                <h3>Upload a PDF Document</h3>
                <form action="/upload" method="post" enctype="multipart/form-data" id="pdf-upload-form">
                    <input type="file" name="file" accept=".pdf" required>
                    <input type="submit" value="Upload PDF">
                </form>
            </div>
            
            <!-- PDF Status -->
            {% if pdf_info %}
            <div class="file-status">
                <strong>Current PDF:</strong> {{ pdf_info.filename }} 
                <br>
                <small>{{ pdf_info.num_pages }} pages processed on {{ pdf_info.processed_at }}</small>
            </div>
            {% endif %}
            
            <!-- Error Message -->
            {% if error %}
            <div class="error">
                {{ error }}
            </div>
            {% endif %}
            
            <!-- Question Form -->
            <div class="form-group">
                <h3>Ask a Question About the PDF</h3>
                <label for="query">Enter your question:</label>
                <input type="text" id="query" name="query" placeholder="What is the main topic of this document?">
                <button onclick="askQuestion()">Ask</button>
            </div>
            
            <!-- Results -->
            <div id="result" class="result" style="display: none;"></div>
            
            <!-- Document Editing with AI -->
            <div class="form-group">
                <h3>Edit Document with AI</h3>
                <label for="edit-instructions">Describe your changes:</label>
                <textarea id="edit-instructions" rows="4" placeholder="Example: Fix formatting in the second paragraph, or Organize the skills section into bullet points"></textarea>
                <button onclick="editWithAI()">Apply Changes</button>
            </div>
        </div>
        
        <div class="pdf-container">
            <div class="toolbar">
                <div class="nav-controls">
                    <button id="prev-page">Previous</button>
                    <span>Page <input id="page-num" type="number" min="1" value="1"> of <span id="page-count">0</span></span>
                    <button id="next-page">Next</button>
                </div>
                
                <button id="toggle-view-btn">Toggle Formatted View</button>
                <button id="save-text-btn" class="save-btn">Save Edits</button>
                
                <div id="save-status" class="status-message">Changes saved successfully!</div>
            </div>
            
            <div class="text-editor">
                <div class="pdf-page">
                    <div class="page-header">
                        {% if pdf_info %}
                            {{ pdf_info.filename }} - Page <span id="header-page-num">1</span>
                        {% else %}
                            No document loaded
                        {% endif %}
                    </div>
                    <div id="html-content" style="display:none;"></div>
                    <textarea id="text-content" placeholder="No content available. Please upload a PDF."></textarea>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Initialize PDF.js for PDF info only
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
        
        let pdfInfo = null;
        let currentPage = 1;
        let totalPages = {{ pdf_info.num_pages if pdf_info else 0 }};
        let textContent = document.getElementById('text-content');
        let pageNumInput = document.getElementById('page-num');
        let pageCountDisplay = document.getElementById('page-count');
        let saveStatusMessage = document.getElementById('save-status');
        
        // Set up initial state
        pageCountDisplay.textContent = totalPages;
        pageNumInput.value = currentPage;
        
        // Load text for the current page
        function loadPageText(pageNum) {
            fetch(`/page-text/${pageNum}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Set the plain text in the textarea
                        textContent.value = data.text;
                        
                        // Set the HTML content if available
                        if (data.html) {
                            const htmlContentDiv = document.getElementById('html-content');
                            htmlContentDiv.innerHTML = data.html;
                            
                            // Toggle view option for formatted view would go here
                            // For now we keep the textarea visible and html content hidden
                        }
                    } else {
                        textContent.value = "Error loading page text: " + data.error;
                    }
                })
                .catch(error => {
                    textContent.value = "Error: " + error;
                });
        }
        
        // Save current page edits
        function savePageText() {
            const text = textContent.value;
            
            fetch('/save-text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    page: currentPage, 
                    text: text,
                    filename: '{{ pdf_info.filename if pdf_info else "" }}'
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showSaveStatus();
                } else {
                    alert('Error saving text: ' + data.error);
                }
            })
            .catch(error => {
                alert('Error saving text: ' + error);
            });
        }
        
        // Show save status message
        function showSaveStatus() {
            saveStatusMessage.classList.add('visible');
            setTimeout(() => {
                saveStatusMessage.classList.remove('visible');
            }, 2000);
        }
        
        // Navigation functions
        function goToPrevPage() {
            if (currentPage <= 1) return;
            currentPage--;
            updatePageDisplay();
            loadPageText(currentPage);
        }
        
        function goToNextPage() {
            if (currentPage >= totalPages) return;
            currentPage++;
            updatePageDisplay();
            loadPageText(currentPage);
        }
        
        // Update all page number displays
        function updatePageDisplay() {
            pageNumInput.value = currentPage;
            document.getElementById('header-page-num').textContent = currentPage;
        }
        
        // Toggle view between text and formatted HTML
        function toggleView() {
            const textContent = document.getElementById('text-content');
            const htmlContent = document.getElementById('html-content');
            const toggleButton = document.getElementById('toggle-view-btn');
            
            if (textContent.style.display === 'none') {
                // Switch to text view
                textContent.style.display = 'block';
                htmlContent.style.display = 'none';
                toggleButton.textContent = 'Show Formatted View';
            } else {
                // Switch to HTML view
                textContent.style.display = 'none';
                htmlContent.style.display = 'block';
                toggleButton.textContent = 'Show Edit View';
            }
        }
        
        // Event listeners
        document.getElementById('prev-page').addEventListener('click', goToPrevPage);
        document.getElementById('next-page').addEventListener('click', goToNextPage);
        document.getElementById('save-text-btn').addEventListener('click', savePageText);
        document.getElementById('toggle-view-btn').addEventListener('click', toggleView);
        
        pageNumInput.addEventListener('change', function() {
            const newPage = parseInt(this.value);
            if (isNaN(newPage) || newPage < 1 || newPage > totalPages) {
                this.value = currentPage;
                return;
            }
            currentPage = newPage;
            updatePageDisplay();
            loadPageText(currentPage);
        });
        
        // Ask question function
        function askQuestion() {
            const query = document.getElementById('query').value;
            if (!query) return;
            
            document.getElementById('result').innerHTML = 'Processing...';
            document.getElementById('result').style.display = 'block';
            
            fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('result').innerHTML = `<div class="error">${data.error}</div>`;
                } else {
                    document.getElementById('result').innerHTML = '<h3>Answer:</h3><p>' + data.answer + '</p>';
                }
            })
            .catch(error => {
                document.getElementById('result').innerHTML = 'Error: ' + error;
            });
        }
        
        // Edit text with AI
        function editWithAI() {
            const instructions = document.getElementById('edit-instructions').value;
            if (!instructions) {
                alert('Please enter editing instructions');
                return;
            }
            
            // Show processing status
            document.getElementById('result').innerHTML = 'Processing your editing request...';
            document.getElementById('result').style.display = 'block';
            
            fetch('/edit-text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    page: currentPage, 
                    text: textContent.value,
                    instructions: instructions,
                    filename: '{{ pdf_info.filename if pdf_info else "" }}'
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the text content with the edited version
                    textContent.value = data.edited_text;
                    
                    // Update the HTML content if needed
                    if (data.html) {
                        const htmlContentDiv = document.getElementById('html-content');
                        htmlContentDiv.innerHTML = data.html;
                    }
                    
                    // Show success message
                    document.getElementById('result').innerHTML = '<h3>Changes Applied:</h3><p>' + data.message + '</p>';
                    
                    // Clear the instructions
                    document.getElementById('edit-instructions').value = '';
                } else {
                    document.getElementById('result').innerHTML = `<div class="error">${data.error}</div>`;
                }
            })
            .catch(error => {
                document.getElementById('result').innerHTML = 'Error: ' + error;
            });
        }
        
        // Load the first page on start
        {% if pdf_info %}
            loadPageText(currentPage);
        {% endif %}
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    pdf_info = rag_system.current_pdf if rag_system else None
    return render_template_string(HTML_TEMPLATE, pdf_info=pdf_info, error=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if file is in the request
    if 'file' not in request.files:
        return render_template_string(HTML_TEMPLATE, pdf_info=None, error="No file part")
    
    file = request.files['file']
    
    # Check if the user submitted an empty form
    if file.filename == '':
        return render_template_string(HTML_TEMPLATE, pdf_info=None, error="No file selected")
    
    # Check if the file has an allowed extension
    if not allowed_file(file.filename):
        return render_template_string(HTML_TEMPLATE, pdf_info=None, error="Invalid file type. Only PDF files are allowed.")
    
    # Validate and save the file
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the PDF
        success = rag_system.process_pdf(file_path)
        if not success:
            return render_template_string(HTML_TEMPLATE, pdf_info=None, error="Failed to process the PDF. Please try another file.")
        
        # Redirect to home page with success
        return redirect(url_for('home'))
    
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, pdf_info=None, error=f"Error processing file: {str(e)}")

@app.route('/ask', methods=['POST'])
def ask():
    query = request.json.get('query', '')
    
    if not rag_system:
        return jsonify({"error": "RAG system not initialized properly"}), 500
    
    try:
        result = rag_system.answer_question(query)
        return jsonify({"answer": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/page-text/<int:page_num>')
def get_page_text(page_num):
    """Get text for a specific page"""
    if not rag_system or not rag_system.current_pdf:
        return jsonify({"success": False, "error": "No PDF loaded"})
    
    try:
        text = rag_system.get_page_text(page_num)
        html = ""
        
        # Get the formatted HTML if available
        if 0 <= page_num - 1 < len(rag_system.current_pdf.get("page_htmls", [])):
            html = rag_system.current_pdf["page_htmls"][page_num - 1]
            
        return jsonify({
            "success": True, 
            "text": text,
            "html": html
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/save-text', methods=['POST'])
def save_text():
    """Save edited text for a PDF page"""
    try:
        # Get data from request
        data = request.json
        page = data.get('page', 1)
        text = data.get('text', '')
        filename = data.get('filename', '')
        
        if not filename:
            return jsonify({"success": False, "error": "No filename provided"}), 400
            
        # Create a unique filename for the edited text
        edit_filename = f"{os.path.splitext(filename)[0]}_page{page}_text.txt"
        edit_path = os.path.join(EDITS_FOLDER, edit_filename)
        
        # Save the edited text
        with open(edit_path, 'w') as f:
            f.write(text)
            
        return jsonify({"success": True, "message": f"Text saved to {edit_filename}"})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/edit-text', methods=['POST'])
def edit_text():
    """Edit text based on natural language instructions using AI"""
    try:
        # Get data from request
        data = request.json
        page = data.get('page', 1)
        text = data.get('text', '')
        instructions = data.get('instructions', '')
        filename = data.get('filename', '')
        
        if not filename:
            return jsonify({"success": False, "error": "No filename provided"}), 400
        
        if not text.strip():
            return jsonify({"success": False, "error": "No text to edit"}), 400
        
        if not instructions.strip():
            return jsonify({"success": False, "error": "No editing instructions provided"}), 400
        
        # Use GPT to edit the text based on instructions
        edited_text = edit_text_with_gpt(text, instructions)
        
        if not edited_text:
            return jsonify({"success": False, "error": "Failed to edit text"}), 500
            
        # Generate HTML version of edited text
        html = generate_html_from_text(edited_text)
        
        # Create a unique filename for the edited text
        edit_filename = f"{os.path.splitext(filename)[0]}_page{page}_text.txt"
        edit_path = os.path.join(EDITS_FOLDER, edit_filename)
        
        # Save the edited text
        with open(edit_path, 'w') as f:
            f.write(edited_text)
            
        return jsonify({
            "success": True, 
            "edited_text": edited_text,
            "html": html,
            "message": f"Successfully applied changes: {instructions}"
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def edit_text_with_gpt(text, instructions):
    """Use GPT to edit text based on instructions"""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a document editing assistant. You will be given a document and instructions for how to edit it. Your task is to return the edited version of the document according to the instructions.

Follow these guidelines:
1. Make ONLY the changes specified in the instructions
2. Preserve all other content and structure
3. Keep existing formatting conventions where possible
4. For resumes and technical documents, ensure professional formatting
5. Important headers and sections should be marked with **bold** for later formatting
                
Return only the edited document text with no additional commentary."""},
                {"role": "user", "content": f"Here is the document to edit:\n\n{text}\n\nEdit instructions: {instructions}\n\nPlease return the edited document:"}
            ],
            temperature=0.3,
            max_tokens=2500,
        )
        
        edited_text = response.choices[0].message.content
        
        # Remove any markdown-style bold - we'll handle this separately
        edited_text = edited_text.replace("**", "")
        
        return edited_text
    except Exception as e:
        print(f"Error editing text with GPT: {e}")
        return None

def generate_html_from_text(text):
    """Generate HTML from text with formatting"""
    if not text:
        return ""
        
    # Split into lines
    lines = text.split('\n')
    html_lines = []
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            html_lines.append('<br>')
            continue
        
        # Identify potential headers
        line_stripped = line.strip()
        is_header = (
            (len(line_stripped) < 50 and not any(p in line_stripped for p in ".,;:?!/")) or
            any(keyword in line_stripped.lower() for keyword in ["experience", "education", "skills", "project", "work", "research", "contact", "engineering", "objective", "profile", "summary"]) or
            line_stripped.isupper() or
            line_stripped.endswith(':')
        )
        
        if is_header:
            html_lines.append(f"<strong>{line}</strong>")
        else:
            html_lines.append(line)
    
    formatted_html = "<br>".join(html_lines)
    return formatted_html

@app.route('/uploads/<filename>')
def serve_pdf(filename):
    """Serve uploaded PDF files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Initialize the RAG system
    rag_system = PDFRagSystem()
    
    # Run the Flask app
    app.run(debug=True, port=5002)
