# src/document_ingestion/content_extraction/ocr/ocr_utils.py

import os
import logging
import tempfile
import base64
from typing import Dict, Any, Optional, Tuple, List, BinaryIO
from pathlib import Path

# Setup logging
logger = logging.getLogger(__name__)

def save_temp_file(content: bytes, filename: Optional[str] = None, suffix: Optional[str] = None) -> str:
    """
    Save binary content to a temporary file.
    
    Args:
        content: Binary content to save
        filename: Optional filename to use for the temp file
        suffix: Optional file suffix if filename not provided
        
    Returns:
        Path to the temporary file
    """
    if filename:
        suffix = Path(filename).suffix
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(content)
        return temp_file.name

def process_file_stream(file_stream: BinaryIO, processor, filename: Optional[str] = None, output_format: str = "markdown") -> Dict[str, Any]:
    """
    Process a file stream through OCR.
    
    Args:
        file_stream: File-like object containing the file data
        processor: OCR processor instance
        filename: Optional filename for mime type detection
        output_format: Desired output format
        
    Returns:
        Dictionary containing the OCR results
    """
    try:
        # Read the content
        content = file_stream.read()
        
        # Save to temp file
        temp_file_path = save_temp_file(content, filename)
        
        try:
            # Process the temp file
            result = processor.process_file(temp_file_path, output_format)
            return result
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.warning(f"Failed to delete temp file {temp_file_path}: {e}")
    except Exception as e:
        logger.error(f"Error processing file stream: {e}")
        raise

def extract_content_from_ocr_result(result: Dict[str, Any], content_type: str = "text") -> str:
    """
    Extract specific content type from OCR result.
    
    Args:
        result: OCR result dictionary
        content_type: Type of content to extract (text, tables, etc.)
        
    Returns:
        Extracted content as string
    """
    try:
        if "content" in result:
            content = result["content"]
            
            if content_type == "text" and isinstance(content, str):
                return content
            elif isinstance(content, dict) and content_type in content:
                return content[content_type]
            
        return ""
    except Exception as e:
        logger.error(f"Error extracting content from OCR result: {e}")
        return ""

def get_mime_type(file_path: str) -> str:
    """
    Get the MIME type for a file based on its extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        MIME type string
    """
    extension_to_mime = {
        '.pdf': 'application/pdf',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.tif': 'image/tiff',
        '.tiff': 'image/tiff',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
        '.md': 'text/markdown',
        '.html': 'text/html',
        '.htm': 'text/html',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    }
    
    file_ext = os.path.splitext(file_path)[1].lower()
    return extension_to_mime.get(file_ext, 'application/octet-stream')

def parse_markdown_content(markdown_content: str) -> Dict[str, Any]:
    """
    Parse structured content from Markdown output of OCR.
    
    Args:
        markdown_content: Markdown content from OCR
        
    Returns:
        Dictionary with parsed content sections
    """
    result = {
        "text": markdown_content,
        "sections": [],
        "tables": [],
        "images": []
    }
    
    # This is a simple parser and would need to be enhanced for production use
    current_section = {"title": "Main", "content": ""}
    in_table = False
    table_content = ""
    
    lines = markdown_content.split("\n")
    for line in lines:
        # Check for headers
        if line.startswith("# "):
            if current_section["content"]:
                result["sections"].append(current_section)
            current_section = {"title": line[2:], "content": ""}
        
        # Check for tables
        elif line.startswith("|") and "-|-" in line:
            in_table = True
            table_content = line + "\n"
        elif in_table and line.startswith("|"):
            table_content += line + "\n"
        elif in_table:
            in_table = False
            result["tables"].append(table_content)
            table_content = ""
        
        # Regular content
        elif not in_table:
            current_section["content"] += line + "\n"
    
    # Add the last section
    if current_section["content"]:
        result["sections"].append(current_section)
    
    return result

def base64_to_temp_file(base64_string: str, suffix: Optional[str] = ".pdf") -> str:
    """
    Convert a base64 string to a temporary file.
    
    Args:
        base64_string: Base64 encoded string
        suffix: File suffix
        
    Returns:
        Path to the temporary file
    """
    try:
        # Decode the base64 string
        file_data = base64.b64decode(base64_string)
        
        # Save to temp file
        return save_temp_file(file_data, suffix=suffix)
    except Exception as e:
        logger.error(f"Error converting base64 to temp file: {e}")
        raise