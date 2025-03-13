#!/usr/bin/env python3
"""
File Inventory Creator

This script creates a comprehensive inventory of files in the uploads directory,
extracting metadata and preparing for vector indexing.

It scans the directory, identifies file types, and creates a CSV table with
detailed information about each file, including extraction status for
different content types.
"""

import os
import csv
import sys
import logging
from pathlib import Path
import mimetypes
import pandas as pd
from datetime import datetime

# Import the enhanced RAGFlowPdfParser for PDF processing
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from work_trial_final.pdf_parser import RAGFlowPdfParser
except ImportError:
    # Direct import as a fallback
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from pdf_parser import RAGFlowPdfParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FileInventoryCreator:
    """
    Creates and manages an inventory of files from the uploads directory.
    
    This class scans the directory, extracts metadata from files,
    and generates a comprehensive CSV inventory with details about
    each file's content and extraction status.
    """
    
    def __init__(self, uploads_dir, output_csv):
        """
        Initialize the inventory creator.
        
        Args:
            uploads_dir (str): Path to the uploads directory
            output_csv (str): Path where the output CSV should be saved
        """
        self.uploads_dir = Path(uploads_dir)
        self.output_csv = Path(output_csv)
        self.pdf_parser = RAGFlowPdfParser()
        
        # Ensure the uploads directory exists
        if not self.uploads_dir.exists():
            raise FileNotFoundError(f"Uploads directory not found: {self.uploads_dir}")
            
        # Initialize the inventory DataFrame
        self.inventory_df = pd.DataFrame(columns=[
            'file_name',
            'file_path',
            'file_type',
            'num_pages',
            'file_size',
            'file_category',
            'extracted_tables',
            'extracted_text',
            'extracted_flow_diagrams',
            'extracted_images',
            'last_updated'
        ])
    
    def guess_file_category(self, file_path, file_type):
        """
        Determine the likely category of a document based on extension and content.
        
        Args:
            file_path (Path): Path to the file
            file_type (str): MIME type of the file
            
        Returns:
            str: Category of the document (e.g., 'report', 'presentation', etc.)
        """
        # Simple categorization based on file extension
        extension = file_path.suffix.lower()
        
        if file_type.startswith('image/'):
            return 'image'
        elif extension in ['.pdf']:
            # We could implement more sophisticated categorization by
            # analyzing content, looking for patterns, etc.
            return 'document'
        elif extension in ['.pptx', '.ppt']:
            return 'presentation'
        elif extension in ['.xlsx', '.xls', '.csv']:
            return 'spreadsheet'
        elif extension in ['.docx', '.doc']:
            return 'document'
        elif extension in ['.txt', '.md']:
            return 'text'
        else:
            return 'other'
    
    def count_pdf_pages(self, file_path):
        """
        Count the number of pages in a PDF file.
        
        Args:
            file_path (Path): Path to the PDF file
            
        Returns:
            int: Number of pages, or 0 if counting fails
        """
        try:
            return RAGFlowPdfParser.total_page_number(str(file_path))
        except Exception as e:
            logger.error(f"Error counting pages in {file_path}: {e}")
            return 0
    
    def scan_directory(self):
        """
        Scan the uploads directory and collect file information.
        
        This method walks through the uploads directory, identifying files
        and collecting metadata about each one.
        """
        logger.info(f"Scanning directory: {self.uploads_dir}")
        
        for root, _, files in os.walk(self.uploads_dir):
            for filename in files:
                # Skip hidden files and system files
                if filename.startswith('.'):
                    continue
                    
                file_path = Path(root) / filename
                rel_path = file_path.relative_to(self.uploads_dir)
                
                try:
                    # Get basic file information
                    file_size = file_path.stat().st_size
                    file_type = mimetypes.guess_type(file_path)[0] or 'unknown'
                    
                    # Get number of pages for PDFs
                    num_pages = 0
                    if file_type == 'application/pdf':
                        num_pages = self.count_pdf_pages(file_path)
                    
                    # Determine file category
                    file_category = self.guess_file_category(file_path, file_type)
                    
                    # Add to inventory DataFrame
                    self.inventory_df = pd.concat([self.inventory_df, pd.DataFrame([{
                        'file_name': filename,
                        'file_path': str(rel_path),
                        'file_type': file_type,
                        'num_pages': num_pages,
                        'file_size': file_size,
                        'file_category': file_category,
                        'extracted_tables': False,
                        'extracted_text': False,
                        'extracted_flow_diagrams': False,
                        'extracted_images': False,
                        'last_updated': datetime.now().isoformat()
                    }])], ignore_index=True)
                    
                    logger.info(f"Added to inventory: {filename}")
                    
                except Exception as e:
                    logger.error(f"Error processing {filename}: {e}")
    
    def save_inventory(self):
        """
        Save the inventory to a CSV file.
        """
        logger.info(f"Saving inventory to {self.output_csv}")
        self.inventory_df.to_csv(self.output_csv, index=False)
        logger.info(f"Saved {len(self.inventory_df)} files to inventory")
    
    def create_inventory(self):
        """
        Create the complete file inventory.
        """
        logger.info("Starting inventory creation process")
        self.scan_directory()
        self.save_inventory()
        logger.info("Inventory creation complete")
        return self.inventory_df


if __name__ == "__main__":
    # Set the uploads directory and output CSV path
    UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
    OUTPUT_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "file_inventory.csv")
    
    # Create the inventory
    inventory_creator = FileInventoryCreator(UPLOADS_DIR, OUTPUT_CSV)
    inventory_df = inventory_creator.create_inventory()
    
    # Print summary
    print(f"\nInventory Creation Complete")
    print(f"=========================")
    print(f"Files processed: {len(inventory_df)}")
    print(f"Inventory saved to: {OUTPUT_CSV}")
    
    # Print category distribution
    if not inventory_df.empty:
        category_counts = inventory_df['file_category'].value_counts()
        print("\nFile Category Distribution:")
        for category, count in category_counts.items():
            print(f"  {category}: {count}")
