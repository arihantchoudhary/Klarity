import os
import sqlite3
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyPDF2 and OCR with pytesseract
    """
    try:
        reader = PdfReader(pdf_path)
        text = []
        
        for page in reader.pages:
            page_text = page.extract_text().strip()
            
            # Only do OCR if needed
            if not page_text and '/XObject' in page['/Resources']:
                xObject = page['/Resources']['/XObject'].get_object()
                
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        img = Image.open(io.BytesIO(xObject[obj].get_data()))
                        page_text = pytesseract.image_to_string(img).strip()
                        break
            
            if page_text:
                text.append(page_text)
                
        return '\n'.join(text)
        
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {str(e)}")
        return None

def init_db():
    """Initialize SQLite database"""
    db_path = os.path.join(os.path.dirname(__file__), 'documents.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS documents
                 (path TEXT PRIMARY KEY, content TEXT)''')
    conn.commit()
    return conn

def process_uploads_folder(uploads_dir="uploads"):
    """
    Process all PDFs in the uploads directory and store text in SQLite
    """
    conn = init_db()
    cursor = conn.cursor()
    
    try:
        for root, _, files in os.walk(uploads_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_path = os.path.join(root, file)
                    text = extract_text_from_pdf(pdf_path)
                    
                    if text:
                        cursor.execute('INSERT OR REPLACE INTO documents (path, content) VALUES (?, ?)',
                                     (pdf_path, text))
        conn.commit()
        
    except Exception as e:
        print(f"Error processing uploads folder: {str(e)}")
        
    finally:
        conn.close()

def main():
    """Main function to demonstrate usage"""
    pdf_path = "uploads/Pfizer/Rel_01032022/125742_S1_M1_cover.pdf"
    
    # Process single file
    conn = init_db()
    cursor = conn.cursor()
    
    try:
        text = extract_text_from_pdf(pdf_path)
        if text:
            cursor.execute('INSERT OR REPLACE INTO documents (path, content) VALUES (?, ?)',
                         (pdf_path, text))
            conn.commit()
            print(f"Successfully processed and stored: {pdf_path}")
        else:
            print("Failed to extract text from PDF")
            
    finally:
        conn.close()

if __name__ == "__main__":
    main()
