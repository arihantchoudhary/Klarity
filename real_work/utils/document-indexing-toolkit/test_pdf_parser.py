#!/usr/bin/env python3
"""
Test Script for PDF Parser

This script tests the RAGFlowPdfParser by processing a sample document 
and displaying the extracted content.

Usage:
    python test_pdf_parser.py

"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get current directory
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Try to use mock dependencies if needed
try:
    # First attempt direct import
    from pdf_parser import RAGFlowPdfParser
    logger.info("Successfully imported RAGFlowPdfParser directly")
except ImportError:
    try:
        # If that fails, try with mock dependencies
        logger.info("Direct import failed, attempting with mock dependencies")
        from mock_dependencies import patch_modules
        patch_modules()
        from pdf_parser import RAGFlowPdfParser
        logger.info("Successfully imported RAGFlowPdfParser with mock dependencies")
        USING_MOCK = True
    except ImportError:
        logger.error("Could not import RAGFlowPdfParser. Check your setup.")
        sys.exit(1)

def create_sample_pdf():
    """Create a simple PDF from the sample document for testing."""
    try:
        from fpdf import FPDF
        
        # Check if text file exists
        sample_text_path = os.path.join(current_dir, "test_data", "sample_document.txt")
        
        if not os.path.exists(sample_text_path):
            logger.error(f"Sample text file not found: {sample_text_path}")
            return None
            
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Read text file
        with open(sample_text_path, 'r') as f:
            content = f.readlines()
        
        # Write content to PDF
        for line in content:
            # Handle basic markdown for headings
            if line.startswith('# '):
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, line[2:].strip(), ln=True)
                pdf.set_font("Arial", size=12)
            elif line.startswith('- ') or line.startswith('• ') or line.startswith('* '):
                pdf.cell(10, 10, "•", ln=0)
                pdf.cell(0, 10, line[2:].strip(), ln=True)
            else:
                pdf.multi_cell(0, 10, line.strip())
                
        # Create output directory if it doesn't exist
        os.makedirs(os.path.join(current_dir, "test_data", "output"), exist_ok=True)
        
        # Save the pdf
        output_pdf = os.path.join(current_dir, "test_data", "output", "sample_document.pdf")
        pdf.output(output_pdf)
        logger.info(f"Created sample PDF at: {output_pdf}")
        return output_pdf
        
    except ImportError:
        logger.warning("FPDF not installed. Cannot create sample PDF.")
        logger.info("Install with: pip install fpdf")
        return None
    except Exception as e:
        logger.error(f"Error creating PDF: {e}")
        return None

def test_pdf_parser():
    """Test the RAGFlowPdfParser on a sample PDF."""
    # Create a sample PDF for testing
    pdf_path = create_sample_pdf()
    
    if not pdf_path:
        logger.warning("Could not create test PDF. Will look for existing test files.")
        # Try to find existing PDF files in the test directory
        test_dir = os.path.join(current_dir, "test_data")
        if os.path.exists(test_dir):
            pdf_files = [f for f in os.listdir(test_dir) if f.endswith('.pdf')]
            if pdf_files:
                pdf_path = os.path.join(test_dir, pdf_files[0])
                logger.info(f"Found existing PDF for testing: {pdf_path}")
            else:
                logger.error("No PDF files found for testing.")
                return False
        else:
            logger.error(f"Test directory not found: {test_dir}")
            return False
    
    # Initialize the PDF parser
    parser = RAGFlowPdfParser()
    
    try:
        # Process the PDF
        logger.info(f"Processing PDF: {pdf_path}")
        text, tables = parser(pdf_path, need_image=True)
        
        # Display extracted text
        print("\n" + "="*50)
        print("EXTRACTED TEXT SAMPLE:")
        print("="*50)
        print(parser.remove_tag(text[:500]) + "..." if len(text) > 500 else parser.remove_tag(text))
        
        # Display extracted tables
        if tables:
            print("\n" + "="*50)
            print(f"EXTRACTED {len(tables)} TABLES:")
            print("="*50)
            for i, (img, content) in enumerate(tables):
                print(f"Table {i+1}:")
                if isinstance(content, str):
                    print(content[:200] + "..." if len(content) > 200 else content)
                else:
                    print(str(content)[:200] + "..." if len(str(content)) > 200 else str(content))
        else:
            print("\nNo tables extracted.")
        
        print("\n" + "="*50)
        logger.info("PDF parser test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error testing PDF parser: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\nTesting RAGFlowPdfParser...")
    success = test_pdf_parser()
    
    if success:
        print("\nPDF Parser Test: SUCCESS")
        print("The RAGFlowPdfParser is working correctly.")
    else:
        print("\nPDF Parser Test: FAILED")
        print("Check the logs for details on the error.")
    
    print("\nNote: This test only verifies basic functionality.")
    print("If you need to test with custom PDFs, place them in the test_data directory.")
    
    # Installation instructions if test fails
    if not success:
        print("\nTroubleshooting tips:")
        print("1. Ensure all required packages are installed:")
        print("   pip install pdfplumber xgboost numpy pypdf Pillow fpdf")
        print("2. Check if the PDF file exists and is accessible")
        print("3. Verify that the imports in pdf_parser.py are correct")
