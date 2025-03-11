import streamlit as st
import cv2
import numpy as np
import pytesseract

def process_document(uploaded_file):
    """
    Process the uploaded file and perform OCR.
    Currently supports image files (png, jpg, jpeg).
    """
    # Read the file bytes and convert to a NumPy array
    file_bytes = uploaded_file.read()
    np_array = np.frombuffer(file_bytes, np.uint8)
    # Decode the image using OpenCV
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    if img is None:
        return "Error: Unable to process the file. Please ensure it is a valid image."
    # Run OCR on the image
    text = pytesseract.image_to_string(img)
    return text

def main():
    st.title("Mistral OCR - Drag and Drop Documents")
    st.markdown("Upload an image file (png, jpg, jpeg) to extract text using OCR.")
    
    uploaded_file = st.file_uploader("Drag and drop a file here", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        st.write("Processing file...")
        ocr_result = process_document(uploaded_file)
        st.text_area("OCR Result", ocr_result, height=300)

if __name__ == "__main__":
    main()
