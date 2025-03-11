import logging
import mimetypes
from typing import Dict, Any, BinaryIO, Optional, List

logger = logging.getLogger(__name__)

class FileProcessor:
    """
    Handles processing of different file formats by routing to appropriate extractors.
    """
    
    def __init__(self, extractors: Dict[str, Any], supported_mime_types: List[str] = None):
        self.extractors = extractors
        self.supported_mime_types = supported_mime_types or [
            "text/plain",
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # docx
            "application/msword",  # doc
            "image/jpeg",
            "image/png",
            "image/tiff"
        ]
    
    async def process_file(
        self, 
        file_content: BinaryIO, 
        filename: str, 
        mime_type: Optional[str] = None
    ) -> str:
        """
        Process a file by sending it to the appropriate extractor.
        
        Args:
            file_content: Binary content of the file
            filename: Name of the file
            mime_type: MIME type of the file (optional)
            
        Returns:
            Extracted text content from the file
        """
        # Determine mime type if not provided
        if not mime_type:
            mime_type = mimetypes.guess_type(filename)[0]
            if not mime_type:
                logger.warning(f"Could not determine mime type for file: {filename}")
                mime_type = "application/octet-stream"
        
        # Check if mime type is supported
        if mime_type not in self.supported_mime_types:
            raise ValueError(f"Unsupported file type: {mime_type}")
        
        # Route to appropriate extractor
        if mime_type == "text/plain":
            return await self.extractors["text"].extract_content(file_content)
        elif mime_type == "application/pdf":
            return await self.extractors["pdf"].extract_content(file_content)
        elif mime_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            # If we have a specific Word extractor, use it, otherwise fall back to PDF extractor with conversion
            if "docx" in self.extractors:
                return await self.extractors["docx"].extract_content(file_content)
            else:
                logger.info(f"No specific extractor for {mime_type}, using PDF extractor with conversion")
                return await self.extractors["pdf"].extract_content_with_conversion(file_content, mime_type)
        elif mime_type.startswith("image/"):
            return await self.extractors["image"].extract_content(file_content, mime_type)
        else:
            # This should not happen due to the supported_mime_types check above
            raise ValueError(f"No extractor configured for mime type: {mime_type}")