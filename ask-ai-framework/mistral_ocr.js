import dotenv from 'dotenv';
import axios from 'axios';

// Load environment variables from .env file
dotenv.config();

const MISTRAL_API_KEY = process.env.MISTRAL_API_KEY;

if (!MISTRAL_API_KEY) {
  console.error("MISTRAL_API_KEY not found in environment variables.");
  process.exit(1);
}

/**
 * Runs OCR on a document using the Mistral API.
 *
 * @param {string} documentUrl - The URL of the document to process.
 * @param {string} documentName - The name of the document.
 * @param {number[]|null} pages - An array indicating which pages to process (defaults to [0]).
 * @returns {Promise<any>} The OCR result data.
 */
async function runOCR(documentUrl, documentName, pages = [0]) {
  const requestBody = {
    model: "ocr-model", // specify the OCR model if needed
    id: "unique-request-id", // ideally generate a unique ID in a real scenario
    document: {
      type: "document_url",
      document_url: documentUrl,
      document_name: documentName
    },
    pages: pages,
    include_image_base64: true,
    image_limit: 5, // maximum number of images to extract
    image_min_size: 100 // minimum image size in pixels (adjust as needed)
  };

  try {
    const response = await axios.post("https://api.mistral.com/ocr", requestBody, {
      headers: {
        'Content-Type': 'application/json',
        'ApiKey': MISTRAL_API_KEY
      }
    });
    console.log("OCR Response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Error running OCR:", error.response ? error.response.data : error.message);
    throw error;
  }
}

// Example usage:
// Replace the following URL and document name with actual values as needed.
const exampleDocumentUrl = "https://example.com/document.pdf";
const exampleDocumentName = "document.pdf";

runOCR(exampleDocumentUrl, exampleDocumentName)
  .then(result => console.log("OCR Completed:", result))
  .catch(err => console.error("OCR Failed:", err));
