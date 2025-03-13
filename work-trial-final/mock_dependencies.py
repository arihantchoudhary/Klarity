"""
Mock Dependencies for PDF Parser

This module provides mock implementations of custom dependencies required by the pdf_parser.py
that might not be available in all environments. This allows for testing the basic functionality
without needing the actual dependencies installed.

Usage:
    import mock_dependencies

    # This will patch the required modules with mock implementations
    mock_dependencies.patch_modules()
"""

import sys
import logging
import os
import numpy as np
from io import BytesIO
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Dictionary to track patched modules
_patched_modules = {}

class MockSettings:
    """Mock implementation of api.settings"""
    LIGHTEN = False

class MockFileUtils:
    """Mock implementation of api.utils.file_utils"""
    
    @staticmethod
    def get_project_base_directory():
        """Mock implementation that returns the current directory"""
        return os.path.dirname(os.path.abspath(__file__))

class MockOCR:
    """Mock implementation of deepdoc.vision.OCR"""
    
    def __init__(self):
        logger.info("Initialized Mock OCR")
    
    def detect(self, image_array):
        """Mock detect method that returns a simple bounding box"""
        logger.info("Mock OCR detection")
        h, w = image_array.shape[:2] if len(image_array.shape) > 2 else (100, 100)
        # Return a mock detection result with one text line
        return [([(0, 0), (w, h)], "Mock OCR Text")]
    
    def get_rotate_crop_image(self, img_np, points):
        """Mock method to get cropped image"""
        return np.zeros((50, 200, 3), dtype=np.uint8)
    
    def recognize_batch(self, box_images):
        """Mock method to recognize text in batch"""
        return ["Mock OCR Text" for _ in box_images]

class MockRecognizer:
    """Mock implementation of deepdoc.vision.Recognizer"""
    
    @staticmethod
    def sort_Y_firstly(boxes, threshold=0):
        """Mock sort method that returns the input boxes"""
        return boxes
    
    @staticmethod
    def layouts_cleanup(boxes, layouts, gap, portion):
        """Mock cleanup method that returns the input layouts"""
        return layouts
    
    @staticmethod
    def find_overlapped_with_threashold(box, boxes, thr=0.5, naive=False):
        """Mock method to find overlapped boxes"""
        return 0 if boxes else None
    
    @staticmethod
    def find_horizontally_tightest_fit(box, boxes):
        """Mock method to find horizontally tight fit"""
        return 0 if boxes else None
    
    @staticmethod
    def find_overlapped(box, boxes, naive=False):
        """Mock method to find overlapped boxes"""
        return 0 if boxes else None

class MockLayoutRecognizer:
    """Mock implementation of deepdoc.vision.LayoutRecognizer"""
    
    def __init__(self, layout_type="layout"):
        self.layout_type = layout_type
        logger.info(f"Initialized Mock LayoutRecognizer with type: {layout_type}")
    
    def __call__(self, images, boxes, zoom, drop=True):
        """Mock call method that adds layout_type to boxes"""
        for i, box_list in enumerate(boxes):
            for box in box_list:
                box["layout_type"] = "text"
                box["layoutno"] = 0
        
        # Create simple layout structure
        layouts = []
        for i, img in enumerate(images):
            layouts.append([{
                "type": "text",
                "x0": 10,
                "x1": 50,
                "top": 10,
                "bottom": 50
            }])
        
        # Flattened boxes list
        flat_boxes = [box for box_list in boxes for box in box_list]
        return flat_boxes, layouts

class MockTableStructureRecognizer:
    """Mock implementation of deepdoc.vision.TableStructureRecognizer"""
    
    def __init__(self):
        logger.info("Initialized Mock TableStructureRecognizer")
    
    def __call__(self, images):
        """Mock call method that returns a simple table structure"""
        return [[{
            "label": "table",
            "x0": 10,
            "x1": 50,
            "top": 10,
            "bottom": 50,
            "pn": 0,
            "layoutno": 0
        }] for _ in images]
    
    @staticmethod
    def is_caption(text_box):
        """Mock method to check if a box is a caption"""
        return "caption" in text_box.get("text", "").lower()
    
    def construct_table(self, boxes, html=False, is_english=True):
        """Mock method to construct a table"""
        if html:
            return "<table><tr><td>Mock</td><td>Table</td></tr></table>"
        else:
            return ["Mock Table Row 1", "Mock Table Row 2"]

class MockRagTokenizer:
    """Mock implementation of rag.nlp.rag_tokenizer"""
    
    @staticmethod
    def tokenize(text):
        """Mock tokenize method that returns the input text"""
        return text
    
    @staticmethod
    def tag(text):
        """Mock tag method that returns a simple tag"""
        return "n"
    
    @staticmethod
    def is_chinese(char):
        """Mock method to check if a character is Chinese"""
        return False

class MockHuggingfaceHub:
    """Mock implementation of huggingface_hub"""
    
    @staticmethod
    def snapshot_download(repo_id, local_dir, local_dir_use_symlinks=False):
        """Mock snapshot_download method that returns the local_dir"""
        os.makedirs(local_dir, exist_ok=True)
        return local_dir

def patch_modules():
    """
    Patch necessary modules with mock implementations
    This function should be called before importing pdf_parser
    """
    global _patched_modules
    
    # Only patch if not already patched
    if _patched_modules:
        return
    
    # Create mock modules
    try:
        # Try to create the api module and its submodules
        if 'api' not in sys.modules:
            sys.modules['api'] = type('api', (), {})
            _patched_modules['api'] = True
            
        if 'api.settings' not in sys.modules:
            sys.modules['api.settings'] = MockSettings
            _patched_modules['api.settings'] = True
            
        if 'api.utils' not in sys.modules:
            sys.modules['api.utils'] = type('utils', (), {})
            _patched_modules['api.utils'] = True
            
        if 'api.utils.file_utils' not in sys.modules:
            sys.modules['api.utils.file_utils'] = MockFileUtils
            _patched_modules['api.utils.file_utils'] = True
            
        # Create deepdoc module and its submodules
        if 'deepdoc' not in sys.modules:
            sys.modules['deepdoc'] = type('deepdoc', (), {})
            _patched_modules['deepdoc'] = True
            
        if 'deepdoc.vision' not in sys.modules:
            vision_module = type('vision', (), {
                'OCR': MockOCR,
                'Recognizer': MockRecognizer,
                'LayoutRecognizer': MockLayoutRecognizer,
                'TableStructureRecognizer': MockTableStructureRecognizer
            })
            sys.modules['deepdoc.vision'] = vision_module
            _patched_modules['deepdoc.vision'] = True
            
        # Create rag module and its submodules
        if 'rag' not in sys.modules:
            sys.modules['rag'] = type('rag', (), {})
            _patched_modules['rag'] = True
            
        if 'rag.nlp' not in sys.modules:
            nlp_module = type('nlp', (), {
                'rag_tokenizer': MockRagTokenizer
            })
            sys.modules['rag.nlp'] = nlp_module
            _patched_modules['rag.nlp'] = True
            
        # Create huggingface_hub module
        if 'huggingface_hub' not in sys.modules:
            huggingface_module = type('huggingface_hub', (), {
                'snapshot_download': MockHuggingfaceHub.snapshot_download
            })
            sys.modules['huggingface_hub'] = huggingface_module
            _patched_modules['huggingface_hub'] = True
        
        logger.info("Successfully patched mock dependencies")
    except Exception as e:
        logger.error(f"Error patching mock dependencies: {e}")
        raise

def unpatch_modules():
    """
    Remove patched modules to restore original functionality
    """
    global _patched_modules
    
    # Remove each patched module
    for module_name in _patched_modules:
        if module_name in sys.modules:
            del sys.modules[module_name]
    
    # Clear the patched modules dictionary
    _patched_modules = {}
    logger.info("Unpatched mock dependencies")

def is_patched():
    """Check if modules have been patched"""
    return bool(_patched_modules)

if __name__ == "__main__":
    # Test the mock modules
    patch_modules()
    
    # Import these to verify they work
    from api import settings
    from api.utils.file_utils import get_project_base_directory
    from deepdoc.vision import OCR, Recognizer, LayoutRecognizer, TableStructureRecognizer
    from rag.nlp import rag_tokenizer
    import huggingface_hub
    
    print("Mock dependencies test successful!")
    
    # Clean up
    unpatch_modules()
