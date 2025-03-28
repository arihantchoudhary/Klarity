import os
import logging
from typing import Dict, List, Any, Optional, BinaryIO

from ..utils.config import Config
from .file_processor import FileProcessor
from .content_extraction.text_extractor import TextExtractor
from .content_extraction.pdf_extractor import PDFExtractor
from .content_extraction.image_extractor import ImageExtractor
from .content_extraction.ocr.mistral_ocr import MistralOCR
from .chunking.semantic_chunker import SemanticChunker
from .chunking.hierarchical_chunker import HierarchicalChunker
from .quality.data_quality_service import DataQualityService
from ..models.document import Document, DocumentMetadata
from ..models.chunk import Chunk

logger = logging.getLogger(__name__)

class DocumentIngestPipeline:
    """
    Main pipeline for processing and ingesting documents into the system.
    """
    
    def __init__(self, config: Config):
        self.config = config
        
        # Initialize OCR service if enabled
        self.ocr_service = None
        if config.get("use_ocr", False):
            self.ocr_service = MistralOCR(
                api_key=config.get("mistral_api_key"),
                output_format=config.get("ocr_output_format", "markdown"),
                self_hosted_url=config.get("self_hosted_ocr_url")
            )
        
        # Initialize extractors based on file types
        self.extractors = {
            "text": TextExtractor(),
            "pdf": PDFExtractor(ocr_service=self.ocr_service),
            "image": ImageExtractor(ocr_service=self.ocr_service)
        }
        
        # Initialize file processor
        self.file_processor = FileProcessor(
            extractors=self.extractors,
            supported_mime_types=config.get("supported_mime_types", [])
        )
        
        # Initialize chunkers
        chunker_type = config.get("chunker_type", "semantic")
        if chunker_type == "semantic":
            self.chunker = SemanticChunker(
                chunk_size=config.get("chunk_size", 1000),
                chunk_overlap=config.get("chunk_overlap", 200)
            )
        elif chunker_type == "hierarchical":
            self.chunker = HierarchicalChunker(
                chunk_sizes=config.get("chunk_sizes", [500, 1000, 2000]),
                chunk_overlaps=config.get("chunk_overlaps", [50, 100, 200])
            )
        else:
            raise ValueError(f"Unsupported chunker type: {chunker_type}")
        
        # Initialize data quality service
        self.quality_service = DataQualityService()
    
    async def process_document(
        self, 
        file_content: BinaryIO, 
        filename: str, 
        mime_type: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Document:
        """
        Process a document through the entire ingestion pipeline.
        
        Args:
            file_content: Binary content of the file
            filename: Name of the file
            mime_type: MIME type of the file
            metadata: Additional metadata for the document
            
        Returns:
            Processed document with extracted content and chunks
        """
        logger.info(f"Processing document: {filename} ({mime_type})")
        
        # Extract content from the file
        extracted_content = await self.file_processor.process_file(
            file_content=file_content,
            filename=filename,
            mime_type=mime_type
        )
        
        # Create document metadata
        doc_metadata = DocumentMetadata(
            source=filename,
            mime_type=mime_type,
            **(metadata or {})
        )
        
        # Create document
        document = Document(
            content=extracted_content,
            metadata=doc_metadata
        )
        
        # Check document quality
        quality_issues = self.quality_service.check_document_quality(document)
        if quality_issues:
            logger.warning(f"Quality issues detected in document {filename}: {quality_issues}")
            document.quality_issues = quality_issues
        
        # Chunk document
        document.chunks = await self.chunker.chunk_document(document)
        
        logger.info(f"Document processed successfully: {filename} with {len(document.chunks)} chunks")
        return document
    
    async def process_documents_batch(
        self, 
        documents: List[Dict[str, Any]]
    ) -> List[Document]:
        """
        Process a batch of documents.
        
        Args:
            documents: List of document dictionaries containing file_content, filename, mime_type, and metadata
            
        Returns:
            List of processed documents
        """
        processed_documents = []
        
        for doc_dict in documents:
            processed_doc = await self.process_document(
                file_content=doc_dict["file_content"],
                filename=doc_dict["filename"],
                mime_type=doc_dict["mime_type"],
                metadata=doc_dict.get("metadata")
            )
            processed_documents.append(processed_doc)
            
        return processed_documents