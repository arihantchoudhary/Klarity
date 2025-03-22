# src/document_ingestion/content_extraction/ocr/mistral_ocr.py

import os
import json
import logging
import requests
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import tempfile
import base64

# Setup logging
logger = logging.getLogger(__name__)

class MistralOCRProcessor:
    """
    Implementation of OCR processing using Mistral OCR API.
    """
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.mistral.ai/v1/ocr", self_hosted_url: Optional[str] = None):
        """
        Initialize the Mistral OCR processor.
        
        Args:
            api_key: Mistral API key
            base_url: Base URL for Mistral OCR API
            self_hosted_url: URL for self-hosted Mistral OCR, if applicable
        """
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        if not self.api_key and not self_hosted_url:
            raise ValueError("Mistral API key must be provided either directly or via MISTRAL_API_KEY environment variable")
        
        self.base_url = self_hosted_url if self_hosted_url else base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def process_file(self, file_path: str, output_format: str = "markdown") -> Dict[str, Any]:
        """
        Process a file through Mistral OCR.
        
        Args:
            file_path: Path to the file to be processed
            output_format: Desired output format (markdown, text, or json)
            
        Returns:
            Dictionary containing the OCR results
        """
        logger.info(f"Processing file with Mistral OCR: {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Get file extension
        file_ext = Path(file_path).suffix.lower()
        
        # Validate file type
        supported_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp']
        if file_ext not in supported_extensions:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: {supported_extensions}")
        
        # Read file and convert to base64
        with open(file_path, "rb") as f:
            file_data = f.read()
            base64_encoded = base64.b64encode(file_data).decode('utf-8')
        
        # Prepare payload
        payload = {
            "file": base64_encoded,
            "model": "mistral-ocr-latest",
            "output_format": output_format
        }
        
        try:
            # Make API call
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Successfully processed file with Mistral OCR: {file_path}")
            return result
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred during OCR processing: {http_err}")
            if response.status_code == 429:
                logger.warning("Rate limit exceeded. Consider implementing retry logic.")
            error_detail = response.json() if response.text else {}
            raise Exception(f"HTTP error occurred: {http_err}. Details: {error_detail}")
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request error occurred during OCR processing: {req_err}")
            raise Exception(f"Request error occurred: {req_err}")
        except Exception as e:
            logger.error(f"Unexpected error during OCR processing: {e}")
            raise Exception(f"Unexpected error: {e}")
    
    def process_batch(self, file_paths: List[str], output_format: str = "markdown") -> List[Dict[str, Any]]:
        """
        Process multiple files in batch through Mistral OCR.
        
        Args:
            file_paths: List of paths to files to be processed
            output_format: Desired output format (markdown, text, or json)
            
        Returns:
            List of dictionaries containing the OCR results
        """
        logger.info(f"Processing batch of {len(file_paths)} files with Mistral OCR")
        
        results = []
        for file_path in file_paths:
            try:
                result = self.process_file(file_path, output_format)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
                results.append({"error": str(e), "file_path": file_path})
        
        return results
    
    def process_with_prompt(self, file_path: str, prompt: str) -> Dict[str, Any]:
        """
        Process a file with a specific prompt to extract targeted information.
        
        Args:
            file_path: Path to the file to be processed
            prompt: Specific prompt for information extraction
            
        Returns:
            Dictionary containing the OCR results based on the prompt
        """
        logger.info(f"Processing file with Mistral OCR using custom prompt: {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read file and convert to base64
        with open(file_path, "rb") as f:
            file_data = f.read()
            base64_encoded = base64.b64encode(file_data).decode('utf-8')
        
        # Prepare payload
        payload = {
            "file": base64_encoded,
            "model": "mistral-ocr-latest",
            "prompt": prompt,
            "output_format": "json"  # For structured information extraction, JSON is preferred
        }
        
        try:
            # Make API call
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Successfully processed file with Mistral OCR and prompt: {file_path}")
            return result
        except Exception as e:
            logger.error(f"Error processing file with prompt: {e}")
            raise Exception(f"Error processing file with prompt: {e}")
    
    def extract_tables(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract tables from a document.
        
        Args:
            file_path: Path to the file to be processed
            
        Returns:
            List of tables extracted from the document
        """
        prompt = "Extract all tables from this document and format them as JSON data."
        result = self.process_with_prompt(file_path, prompt)
        
        # Process result to extract tables
        tables = []
        try:
            if "content" in result:
                tables = result["content"].get("tables", [])
            return tables
        except Exception as e:
            logger.error(f"Error extracting tables: {e}")
            return []
    
    def extract_math_expressions(self, file_path: str) -> List[str]:
        """
        Extract mathematical expressions from a document.
        
        Args:
            file_path: Path to the file to be processed
            
        Returns:
            List of mathematical expressions extracted from the document
        """
        prompt = "Extract all mathematical expressions from this document."
        result = self.process_with_prompt(file_path, prompt)
        
        # Process result to extract math expressions
        expressions = []
        try:
            if "content" in result:
                expressions = result["content"].get("math_expressions", [])
            return expressions
        except Exception as e:
            logger.error(f"Error extracting mathematical expressions: {e}")
            return []
    
    def summarize_document(self, file_path: str) -> str:
        """
        Generate a summary of the document.
        
        Args:
            file_path: Path to the file to be processed
            
        Returns:
            Summary of the document
        """
        prompt = "Provide a concise summary of this document."
        result = self.process_with_prompt(file_path, prompt)
        
        # Extract summary
        try:
            if "content" in result:
                return result["content"].get("summary", "")
            return ""
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return ""