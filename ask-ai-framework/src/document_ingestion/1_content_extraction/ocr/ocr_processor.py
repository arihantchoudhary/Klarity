# src/document_ingestion/content_extraction/ocr/ocr_processor.py

import os
import logging
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod

from .mistral_ocr import MistralOCRProcessor

# Setup logging
logger = logging.getLogger(__name__)

class OCRProcessorInterface(ABC):
    """Abstract interface for OCR processors."""
    
    @abstractmethod
    def process_file(self, file_path: str, output_format: str = "markdown") -> Dict[str, Any]:
        """Process a file and extract text content."""
        pass
    
    @abstractmethod
    def process_batch(self, file_paths: List[str], output_format: str = "markdown") -> List[Dict[str, Any]]:
        """Process multiple files in batch."""
        pass

class OCRProcessor:
    """
    Main OCR processor that manages different OCR implementations.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the OCR processor with configuration.
        
        Args:
            config: Configuration dictionary containing OCR settings
        """
        self.config = config or {}
        self.api_key = self.config.get("mistral_api_key") or os.environ.get("MISTRAL_API_KEY")
        self.use_self_hosted = self.config.get("use_self_hosted_ocr", False)
        self.self_hosted_url = self.config.get("self_hosted_ocr_url")
        self.default_output_format = self.config.get("ocr_output_format", "markdown")
        
        # Initialize Mistral OCR processor
        if self.use_self_hosted and self.self_hosted_url:
            self.ocr_processor = MistralOCRProcessor(self.api_key, self_hosted_url=self.self_hosted_url)
        else:
            self.ocr_processor = MistralOCRProcessor(self.api_key)
        
        logger.info("OCR Processor initialized")
    
    def should_use_ocr(self, file_path: str) -> bool:
        """
        Determine if OCR should be used for the given file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Boolean indicating whether OCR should be used
        """
        mime_types = self.config.get("ocr_mime_types", [
            "application/pdf",
            "image/jpeg",
            "image/png",
            "image/tiff",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ])
        
        # Simple mime type detection based on file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        
        ext_to_mime = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.tif': 'image/tiff',
            '.tiff': 'image/tiff',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }
        
        detected_mime = ext_to_mime.get(file_ext)
        return detected_mime in mime_types if detected_mime else False
    
    def process_file(self, file_path: str, output_format: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a file using the appropriate OCR method.
        
        Args:
            file_path: Path to the file to be processed
            output_format: Desired output format (overrides default)
            
        Returns:
            Dictionary containing the OCR results
        """
        if not self.should_use_ocr(file_path):
            logger.info(f"OCR not required for file: {file_path}")
            raise ValueError(f"OCR not supported for file: {file_path}")
        
        format_to_use = output_format or self.default_output_format
        logger.info(f"Processing file with OCR: {file_path}, format: {format_to_use}")
        
        try:
            result = self.ocr_processor.process_file(file_path, format_to_use)
            return result
        except Exception as e:
            logger.error(f"Error in OCR processing: {e}")
            raise
    
    def process_batch(self, file_paths: List[str], output_format: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Process multiple files using OCR.
        
        Args:
            file_paths: List of paths to files to be processed
            output_format: Desired output format (overrides default)
            
        Returns:
            List of dictionaries containing the OCR results
        """
        format_to_use = output_format or self.default_output_format
        logger.info(f"Processing batch of {len(file_paths)} files with OCR, format: {format_to_use}")
        
        # Filter files that should use OCR
        ocr_files = [f for f in file_paths if self.should_use_ocr(f)]
        
        if not ocr_files:
            logger.info("No files requiring OCR in batch")
            return []
        
        try:
            results = self.ocr_processor.process_batch(ocr_files, format_to_use)
            return results
        except Exception as e:
            logger.error(f"Error in batch OCR processing: {e}")
            raise
    
    def extract_tables(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract tables from a document.
        
        Args:
            file_path: Path to the file to be processed
            
        Returns:
            List of tables extracted from the document
        """
        if not self.should_use_ocr(file_path):
            logger.info(f"OCR not required for table extraction: {file_path}")
            raise ValueError(f"OCR not supported for file: {file_path}")
        
        try:
            tables = self.ocr_processor.extract_tables(file_path)
            return tables
        except Exception as e:
            logger.error(f"Error extracting tables with OCR: {e}")
            raise
    
    def extract_math_expressions(self, file_path: str) -> List[str]:
        """
        Extract mathematical expressions from a document.
        
        Args:
            file_path: Path to the file to be processed
            
        Returns:
            List of mathematical expressions extracted from the document
        """
        if not self.should_use_ocr(file_path):
            logger.info(f"OCR not required for math expression extraction: {file_path}")
            raise ValueError(f"OCR not supported for file: {file_path}")
        
        try:
            expressions = self.ocr_processor.extract_math_expressions(file_path)
            return expressions
        except Exception as e:
            logger.error(f"Error extracting math expressions with OCR: {e}")
            raise
    
    def summarize_document(self, file_path: str) -> str:
        """
        Generate a summary of the document.
        
        Args:
            file_path: Path to the file to be processed
            
        Returns:
            Summary of the document
        """
        if not self.should_use_ocr(file_path):
            logger.info(f"OCR not required for document summarization: {file_path}")
            raise ValueError(f"OCR not supported for file: {file_path}")
        
        try:
            summary = self.ocr_processor.summarize_document(file_path)
            return summary
        except Exception as e:
            logger.error(f"Error summarizing document with OCR: {e}")
            raise