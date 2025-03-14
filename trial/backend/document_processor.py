from typing import List, Any, Tuple, Dict
import os
from unstructured.partition.pdf import partition_pdf
from tqdm import tqdm

class DocumentProcessor:
    """Handles the processing of PDF documents, extracting text, tables, and images."""
    
    def __init__(self, output_path: str = "./content/"):
        """Initialize the document processor.
        
        Args:
            output_path: Directory to store temporary files and processed content
        """
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)
    
    def process_pdf(self, file_path: str, extract_images: bool = True) -> Tuple[List[Any], List[Any], List[str]]:
        """Process a PDF file and extract its contents.
        
        Args:
            file_path: Path to the PDF file
            extract_images: Whether to extract images from the PDF
            
        Returns:
            Tuple containing lists of (texts, tables, images)
        """
        print(f"Processing PDF: {file_path}")
        
        # Extract content using unstructured
        chunks = partition_pdf(
            filename=file_path,
            infer_table_structure=True,
            strategy="hi_res",
            extract_image_block_types=["Image"] if extract_images else [],
            extract_image_block_to_payload=True,
            chunking_strategy="by_title",
            max_characters=10000,
            combine_text_under_n_chars=2000,
            new_after_n_chars=6000,
        )
        
        # Separate content types
        tables = []
        texts = []
        images_b64 = []
        
        for chunk in tqdm(chunks, desc="Processing chunks"):
            if "Table" in str(type(chunk)):
                tables.append(chunk)
            elif "CompositeElement" in str(type(chunk)):
                texts.append(chunk)
                # Extract images from composite elements
                if extract_images:
                    for element in chunk.metadata.orig_elements:
                        if 'Image' in str(type(element)):
                            img_dict = element.to_dict()
                            if 'base64' in img_dict:
                                images_b64.append(img_dict['base64'])
        
        print(f"Extracted {len(texts)} text chunks, {len(tables)} tables, and {len(images_b64)} images")
        return texts, tables, images_b64
    
    def process_directory(self, directory_path: str) -> Dict[str, Tuple[List[Any], List[Any], List[str]]]:
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