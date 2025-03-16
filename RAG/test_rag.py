#!/usr/bin/env python3
"""
Simple CLI test script for the PDF RAG system.
This script allows testing the RAG capabilities without running the full Flask application.
"""

import os
import argparse
from dotenv import load_dotenv
import openai
from app import PDFRagSystem, extract_text_from_pdf, chunk_text

# Load environment variables
load_dotenv()

def test_pdf_rag(pdf_path):
    """Initialize the PDF RAG system and allow interactive queries"""
    print("Initializing PDF RAG system...")
    
    # Check for API key
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("Error: OpenAI API key not found or not set properly in .env file")
        print("Please add your API key to the .env file and try again")
        return
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return
    
    openai.api_key = api_key
    
    # Initialize RAG system with the PDF
    rag_system = PDFRagSystem(pdf_path)
    
    # Get basic PDF info
    pdf_info = rag_system.current_pdf
    if not pdf_info:
        print("Error: Failed to process the PDF")
        return
    
    print(f"\nSuccessfully processed PDF: {pdf_info['filename']}")
    print(f"Created {pdf_info['num_chunks']} text chunks")
    print("You can now ask questions about this document.")
    print("Type 'exit' or 'quit' to end the session.\n")
    
    # Interactive query loop
    while True:
        query = input("\nEnter your question: ")
        
        if query.lower() in ['exit', 'quit']:
            print("Exiting test session.")
            break
        
        if not query.strip():
            continue
        
        try:
            print("\nProcessing your query...")
            result = rag_system.answer_question(query)
            print(f"\nAnswer: {result}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the PDF RAG system")
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file to process')
    
    args = parser.parse_args()
    test_pdf_rag(args.pdf_path)
