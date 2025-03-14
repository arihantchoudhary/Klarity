# Chain-of-Thought Reasoning Chat Interface

A web-based chat interface for exploring Chain-of-Thought Reasoning concepts in large language models.

## Project Overview

This project implements a responsive web interface that mimics an AI research platform focused on Chain-of-Thought Reasoning. It includes:

- A chat interface for interacting with AI about research papers
- Source selection for referencing specific papers
- Studio tools for notes and audio overview
- Python Flask backend for API requests

## Features

- Responsive layout that matches the provided design mockup
- Source selection with checkboxes
- Interactive chat with suggested questions
- Notes management in the Studio panel
- Interactive mode with beta tag
- Backend API for chat responses

## Requirements

- Python 3.7+
- Flask
- Modern web browser with JavaScript enabled

## Installation

1. Clone the repository or navigate to the project directory
2. Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask backend server:

```bash
python app.py
```

2. Open your web browser and navigate to:

```
http://localhost:5001
```

## Project Structure

- `index.html` - Main HTML structure for the chat interface
- `styles.css` - CSS styling for the interface
- `script.js` - JavaScript for client-side interactivity
- `app.py` - Python Flask backend for serving the application and handling API requests
- `requirements.txt` - Python dependencies required for the backend

## API Endpoints

- `GET /` - Serves the main HTML page
- `GET /<path>` - Serves static files (CSS, JS)
- `POST /api/chat` - Accepts chat messages and returns AI responses

### Example API Request

```json
{
  "message": "How does CoT decoding reveal reasoning abilities?",
  "sources": ["source1", "source2", "source3"]
}
```

## References

The interface is designed based on research papers about Chain-of-Thought Reasoning:
- Paper 1: 2203.14465v2.pdf - Focuses on providing rationales during language model training
- Paper 2: 2402.10200v2.pdf - Explores reasoning without explicit prompting
- Paper 3: 2402.12875v4.pdf - Examines computational expressiveness of transformers
