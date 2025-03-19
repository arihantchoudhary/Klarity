from typing import List, Any, Tuple, Dict
import os
import pdfplumber
from pdf2image import convert_from_path
import io
import base64
from PIL import Image
from tqdm import tqdm
import streamlit as st

class DocumentProcessor:
    """Handles the processing of PDF documents, extracting text, tables, and images."""
    
    def __init__(self, output_path: str = "./content/"):
        """Initialize the document processor.
        
        Args:
            output_path: Directory to store temporary files and processed content
        """
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)
    
    def process_pdf(self, file_path: str, extract_images: bool = True) -> Tuple[List[str], List[List[List[str]]], List[str]]:
        """Process a PDF file and extract its contents.
        
        Args:
            file_path: Path to the PDF file
            extract_images: Whether to extract images from the PDF
            
        Returns:
            Tuple containing lists of (texts, tables, images)
        """
        print(f"Processing PDF: {file_path}")
        
        texts = []
        tables = []
        images_b64 = []
        
        # Extract text and tables using pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in tqdm(pdf.pages, desc="Processing pages"):
                # Extract text
                text = page.extract_text()
                if text and text.strip():
                    texts.append(text.strip())
                
                # Extract tables
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)
        
        # Extract images using pdf2image if requested
        if extract_images:
            try:
                # Convert PDF pages to images
                pages = convert_from_path(file_path)
                
                for i, page in enumerate(pages):
                    # Save image to bytes
                    img_byte_arr = io.BytesIO()
                    page.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    # Convert to base64
                    img_b64 = base64.b64encode(img_byte_arr).decode('utf-8')
                    images_b64.append(img_b64)
            except Exception as e:
                print(f"Warning: Failed to extract images: {str(e)}")
        
        print(f"Extracted {len(texts)} text chunks, {len(tables)} tables, and {len(images_b64)} images")
        return texts, tables, images_b64
    
    def process_directory(self, directory_path: str) -> Dict[str, Tuple[List[str], List[List[List[str]]], List[str]]]:
        """Process all PDF files in a directory.
        
        Args:
            directory_path: Path to directory containing PDF files
            
        Returns:
            Dictionary mapping filenames to their processed contents
        """
        results = {}
        for filename in os.listdir(directory_path):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(directory_path, filename)
                try:
                    results[filename] = self.process_pdf(file_path)
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
                    continue
        return results

def main():
    """Streamlit frontend for PDF processing"""
    st.title("PDF Document Processor")
    
    # Initialize processor
    processor = DocumentProcessor()
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    extract_images = st.checkbox("Extract images", value=True)
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Process the file
        with st.spinner('Processing PDF...'):
            texts, tables, images = processor.process_pdf("temp.pdf", extract_images)
        
        # Display results
        st.success("Processing complete!")
        
        # Show text content
        if texts:
            st.subheader("Extracted Text")
            for i, text in enumerate(texts):
                with st.expander(f"Text chunk {i+1}"):
                    st.write(text)
        
        # Show tables
        if tables:
            st.subheader("Extracted Tables")
            for i, table in enumerate(tables):
                with st.expander(f"Table {i+1}"):
                    st.write(table)
        
        # Show images
        if images:
            st.subheader("Extracted Images")
            for i, img_b64 in enumerate(images):
                st.image(img_b64, caption=f"Image {i+1}")
        
        # Cleanup
        os.remove("temp.pdf")
    
    # Directory processing
    st.subheader("Process Directory")
    dir_path = st.text_input("Enter directory path containing PDFs")
    if st.button("Process Directory") and dir_path:
        if os.path.exists(dir_path):
            with st.spinner('Processing directory...'):
                results = processor.process_directory(dir_path)
            
            st.success("Directory processing complete!")
            for filename, (texts, tables, images) in results.items():
                with st.expander(f"File: {filename}"):
                    st.write(f"Number of text chunks: {len(texts)}")
                    st.write(f"Number of tables: {len(tables)}")
                    st.write(f"Number of images: {len(images)}")
        else:
            st.error("Directory not found!")

if __name__ == "__main__":
    main()