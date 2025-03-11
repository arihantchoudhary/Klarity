import os
import requests
from dotenv import load_dotenv
import streamlit as st

def process_document(uploaded_file):
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("MISTRAL_API_KEY")
    endpoint = os.getenv("MISTRAL_OCR_ENDPOINT")
    model = os.getenv("MISTRAL_OCR_MODEL")
    include_images = os.getenv("INCLUDE_IMAGES", "false")
    request_timeout = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": uploaded_file.type  # e.g., "image/png" or "application/pdf"
    }
    
    # Read the uploaded file content
    file_content = uploaded_file.read()
    
    # Make the API call to the Mistral OCR API for single document processing
    response = requests.post(
        endpoint,
        headers=headers,
        data=file_content,
        params={
            "model": model,
            "include_images": include_images
        },
        timeout=request_timeout
    )
    
    # Return the parsed JSON or error message
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

def process_batch(uploaded_files):
    results = {}
    for uploaded_file in uploaded_files:
        result = process_document(uploaded_file)
        results[uploaded_file.name] = result
    return results

def main():
    st.title("Mistral OCR - Document Processing")
    st.markdown("Upload one or more files (images or PDFs) to extract text and structured output using the Mistral OCR API.")
    
    batch_processing = st.checkbox("Enable Batch Processing", value=False)
    
    if batch_processing:
        uploaded_files = st.file_uploader(
            "Drag and drop files here", 
            type=["png", "jpg", "jpeg", "pdf"], 
            accept_multiple_files=True
        )
        if uploaded_files:
            st.write("Processing files...")
            results = process_batch(uploaded_files)
            st.json(results)
    else:
        uploaded_file = st.file_uploader(
            "Drag and drop a file here", 
            type=["png", "jpg", "jpeg", "pdf"]
        )
        if uploaded_file is not None:
            st.write("Processing file...")
            result = process_document(uploaded_file)
            st.json(result)

if __name__ == "__main__":
    main()
