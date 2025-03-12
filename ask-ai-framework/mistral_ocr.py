import os
import base64
import uuid
import requests
from dotenv import load_dotenv
import os
from mistralai import Mistral

# Load environment variables from .env file
load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    print("MISTRAL_API_KEY not found in environment variables.")
    exit(1)

def run_ocr(file_path, pages=[0]):
    """
    Runs OCR on a local document file using the Mistral API.

    Parameters:
        file_path (str): The local path to the document to process.
        pages (list, optional): Specific pages to process (defaults to [0]).

    Returns:
        dict: The OCR result data.
    """
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        exit(1)
    
    # Encode file data in base64
    encoded_file = base64.b64encode(file_data).decode("utf-8")
    document_name = os.path.basename(file_path)
    
    request_body = {
        "model": "ocr-model",  # specify the OCR model if needed
        "id": str(uuid.uuid4()),  # generate a unique request ID
        "document": {
            "type": "local_file",
            "file_content": encoded_file,
            "document_name": document_name
        },
        "pages": pages,
        "include_image_base64": True,
        "image_limit": 5,        # maximum number of images to extract
        "image_min_size": 100      # minimum image size in pixels (adjust as needed)
    }
    
    headers = {
        "Content-Type": "application/json",
        "ApiKey": MISTRAL_API_KEY
    }
    
    url = "https://api.mistral.com/ocr"
    
    try:
        response = requests.post(url, json=request_body, headers=headers)
        response.raise_for_status()
        print("OCR Response:", response.json())
        return response.json()
    except requests.HTTPError as http_err:
        print("HTTP error occurred:", http_err)
        print("Response:", response.text)
        raise
    except Exception as err:
        print("Other error occurred:", err)
        raise

if __name__ == "__main__":
    # Replace the following path with the actual local file path
    os.environ["MISTRAL_API_KEY"] = "your_api_key_here"

    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": "What is the best French cheese?"}]
    )

    print(response.choices[0].message.content)
    file_path = "uploads/Anlaysis_Essay.pdf"
    run_ocr(file_path)
