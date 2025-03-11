#!/usr/bin/env python
# src/scripts/test_mistral_ocr.py

import os
import sys
import argparse
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from document_ingestion.content_extraction.ocr.mistral_ocr import MistralOCRProcessor
from document_ingestion.content_extraction.ocr.ocr_processor import OCRProcessor
from document_ingestion.content_extraction.ocr.ocr_utils import parse_markdown_content

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Test Mistral OCR integration')
    parser.add_argument('file_path', help='Path to the file to process with OCR')
    parser.add_argument('--api-key', help='Mistral API key (or set MISTRAL_API_KEY env var)')
    parser.add_argument('--output-format', default='markdown', choices=['markdown', 'text', 'json'],
                        help='Output format (default: markdown)')
    parser.add_argument('--save-output', action='store_true', help='Save the OCR output to a file')
    parser.add_argument('--extract-tables', action='store_true', help='Extract tables from the document')
    parser.add_argument('--extract-math', action='store_true', help='Extract mathematical expressions')
    parser.add_argument('--summarize', action='store_true', help='Generate a document summary')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.file_path):
        logger.error(f"File not found: {args.file_path}")
        return 1
    
    # Get API key
    api_key = args.api_key or os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        logger.error("Mistral API key not provided. Use --api-key or set MISTRAL_API_KEY environment variable")
        return 1
    
    try:
        # Initialize OCR processor
        ocr_config = {
            "mistral_api_key": api_key,
            "use_self_hosted_ocr": False,
            "ocr_output_format": args.output_format
        }
        ocr_processor = OCRProcessor(ocr_config)
        
        # Process file
        logger.info(f"Processing file: {args.file_path}")
        result = ocr_processor.process_file(args.file_path, args.output_format)
        
        # Extract content based on output format
        if args.output_format == 'markdown' or args.output_format == 'text':
            content = result.get('content', '')
            logger.info(f"Extracted content ({len(content)} characters)")
            print("\n--- OCR OUTPUT (first 500 chars) ---")
            print(content[:500] + "..." if len(content) > 500 else content)
            
            if args.output_format == 'markdown':
                parsed = parse_markdown_content(content)
                print(f"\nFound {len(parsed['sections'])} sections and {len(parsed['tables'])} tables")
                
        elif args.output_format == 'json':
            print("\n--- OCR OUTPUT (JSON) ---")
            print(result)
        
        # Save output if requested
        if args.save_output:
            output_file = f"{os.path.splitext(args.file_path)[0]}_ocr.{args.output_format}"
            with open(output_file, 'w') as f:
                if isinstance(result.get('content'), str):
                    f.write(result.get('content', ''))
                else:
                    import json
                    json.dump(result, f, indent=2)
            logger.info(f"Saved OCR output to: {output_file}")
        
        # Extract tables if requested
        if args.extract_tables:
            try:
                tables = ocr_processor.extract_tables(args.file_path)
                print(f"\n--- EXTRACTED TABLES ({len(tables)}) ---")
                for i, table in enumerate(tables):
                    print(f"\nTable {i+1}:")
                    print(table)
            except Exception as e:
                logger.error(f"Error extracting tables: {e}")
        
        # Extract math expressions if requested
        if args.extract_math:
            try:
                expressions = ocr_processor.extract_math_expressions(args.file_path)
                print(f"\n--- EXTRACTED MATH EXPRESSIONS ({len(expressions)}) ---")
                for i, expr in enumerate(expressions):
                    print(f"\nExpression {i+1}: {expr}")
            except Exception as e:
                logger.error(f"Error extracting math expressions: {e}")
        
        # Generate summary if requested
        if args.summarize:
            try:
                summary = ocr_processor.summarize_document(args.file_path)
                print("\n--- DOCUMENT SUMMARY ---")
                print(summary)
            except Exception as e:
                logger.error(f"Error generating summary: {e}")
        
        logger.info("OCR processing completed successfully")
        return 0
    
    except Exception as e:
        logger.error(f"Error during OCR processing: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())