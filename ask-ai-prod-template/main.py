import sys
import os
from pathlib import Path

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from trial.backend.document_processor import DocumentProcessor

def process_pfizer_files():
    """Process Pfizer files under 20 pages and extract content"""
    
    # Initialize document processor
    processor = DocumentProcessor()
    
    # Read the Pfizer files inventory CSV
    try:
        os.chdir('/Users/arihantchoudhary/GitHub/Klarity/ask-ai-framework')
        df = pd.read_csv('pfizer_files_inventory.csv')
    except FileNotFoundError:
        print("Error: pfizer_file_inventory.csv not found")
        return
        
    # Filter for files with <= 20 pages
    df_filtered = df[df['num_pages'] <= 20].copy()
    print(f"Processing {len(df_filtered)} files with <= 20 pages")
    
    # Create new dataframe for extracted content
    extractions_df = pd.DataFrame(columns=[
        'file_path',
        'num_pages', 
        'extracted_text',
        'extracted_tables',
        'extracted_images'
    ])
    
    # Process each file
    for idx, row in df_filtered.iterrows():
        file_path = row['file_path']
        print(f"\nProcessing file {idx + 1}/{len(df_filtered)}")
        print(f"Path: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"Warning: File not found - {file_path}")
            continue
            
        if not file_path.lower().endswith('.pdf'):
            print(f"Warning: Not a PDF file - {file_path}")
            continue
            
        try:
            print(f"Processing {file_path}")
            texts, tables, images = processor.process_pdf(file_path)
            
            # Add row to extractions dataframe
            new_row = pd.DataFrame([{
                'file_path': file_path,
                'num_pages': row['num_pages'],
                'extracted_text': '\n'.join(texts) if texts else '',
                'extracted_tables': str(tables) if tables else '',
                'extracted_images': str(len(images)) if images else '0'
            }])
            extractions_df = pd.concat([extractions_df, new_row], ignore_index=True)
            
            print(f"Successfully processed: {os.path.basename(file_path)}")
            print(f"- Extracted {len(texts)} text chunks")
            print(f"- Extracted {len(tables)} tables")
            print(f"- Extracted {len(images)} images")
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            continue
    
    # Save extractions to new CSV
    try:
        extractions_df.to_csv('pfizer_extractions_under_20_pages.csv', index=False)
        print("\nSuccessfully saved extractions to pfizer_extractions_under_20_pages.csv")
    except Exception as e:
        print(f"Error saving CSV: {str(e)}")




def main():
    # print("Starting Pfizer files processing...")
    # process_pfizer_files()
    # print("Processing complete!")


if __name__ == "__main__":
    main()
