#!/bin/bash
# Run All Tests Script for PDF Processing and Vector Indexing System
# This script runs all the tests in sequence and checks for dependencies

# Terminal colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Display header
echo -e "\n${BLUE}==========================================${NC}"
echo -e "${BLUE}  PDF Processing & Vector Indexing Tests  ${NC}"
echo -e "${BLUE}==========================================${NC}\n"

# Check Python installation
echo -e "${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}Found Python: $(python3 --version)${NC}"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo -e "${GREEN}Found Python: $(python --version)${NC}"
else
    echo -e "${RED}Error: Python not found. Please install Python 3.7+${NC}"
    exit 1
fi

# Check for required packages
echo -e "\n${YELLOW}Checking required packages...${NC}"

# Function to check if a Python package is installed
check_package() {
    $PYTHON_CMD -c "import $1" 2> /dev/null
    if [ $? -eq 0 ]; then
        echo -e "  ${GREEN}✓ $1${NC}"
        return 0
    else
        echo -e "  ${RED}✗ $1${NC}"
        return 1
    fi
}

# Check core packages
MISSING_CORE=false
echo "Core packages:"
check_package pandas || MISSING_CORE=true
check_package numpy || MISSING_CORE=true
check_package pathlib || MISSING_CORE=true
check_package logging || MISSING_CORE=true

# Check PDF processing packages
MISSING_PDF=false
echo -e "\nPDF processing packages:"
check_package pdfplumber || MISSING_PDF=true
check_package pypdf || MISSING_PDF=true
check_package PIL || echo -e "  ${YELLOW}✓ PIL (will try Pillow)${NC}" && check_package Pillow || MISSING_PDF=true
check_package xgboost || MISSING_PDF=true

# Check for mock dependencies
MOCK_DEPS_AVAILABLE=false
if [ -f "mock_dependencies.py" ]; then
    echo -e "\n${GREEN}Mock dependencies available - will use for missing packages${NC}"
    MOCK_DEPS_AVAILABLE=true
else
    echo -e "\n${YELLOW}Warning: mock_dependencies.py not found${NC}"
    echo -e "Some tests may fail if required packages are missing"
fi

# Check vector indexing packages (optional)
MISSING_VECTOR=false
echo -e "\nVector indexing packages (optional):"
check_package sentence_transformers || MISSING_VECTOR=true
check_package faiss || echo -e "  ${YELLOW}✓ faiss (will try faiss-cpu)${NC}" && check_package faiss_cpu || MISSING_VECTOR=true

# Check testing packages
MISSING_TEST=false
echo -e "\nTesting packages:"
check_package tqdm || MISSING_TEST=true
check_package fpdf || MISSING_TEST=true

# Warn about missing packages
if [ "$MISSING_CORE" = true ]; then
    echo -e "\n${RED}Error: Missing core packages. Install with:${NC}"
    echo -e "  pip install pandas numpy"
    exit 1
fi

if [ "$MISSING_PDF" = true ]; then
    echo -e "\n${YELLOW}Warning: Missing PDF processing packages. Some tests may fail.${NC}"
    echo -e "Install with: pip install pdfplumber xgboost pypdf Pillow"
fi

if [ "$MISSING_VECTOR" = true ]; then
    echo -e "\n${YELLOW}Warning: Missing vector indexing packages. Will use simulated embeddings.${NC}"
    echo -e "Install with: pip install sentence-transformers faiss-cpu"
fi

if [ "$MISSING_TEST" = true ]; then
    echo -e "\n${YELLOW}Warning: Missing testing packages. Some tests may fail.${NC}"
    echo -e "Install with: pip install tqdm fpdf"
fi

# Create a results array
declare -a TEST_RESULTS

# Run PDF parser test
echo -e "\n${BLUE}==========================================${NC}"
echo -e "${BLUE}  Running PDF Parser Test                 ${NC}"
echo -e "${BLUE}==========================================${NC}\n"

$PYTHON_CMD test_pdf_parser.py
if [ $? -eq 0 ]; then
    TEST_RESULTS+=("PDF Parser Test: SUCCESS")
else
    TEST_RESULTS+=("PDF Parser Test: FAILED")
fi

# Run inventory test
echo -e "\n${BLUE}==========================================${NC}"
echo -e "${BLUE}  Running File Inventory Test             ${NC}"
echo -e "${BLUE}==========================================${NC}\n"

$PYTHON_CMD test_indexing.py --component=inventory
if [ $? -eq 0 ]; then
    TEST_RESULTS+=("File Inventory Test: SUCCESS")
else
    TEST_RESULTS+=("File Inventory Test: FAILED")
fi

# Run vector indexing test
echo -e "\n${BLUE}==========================================${NC}"
echo -e "${BLUE}  Running Vector Indexing Test            ${NC}"
echo -e "${BLUE}==========================================${NC}\n"

$PYTHON_CMD test_indexing.py --component=vector
if [ $? -eq 0 ]; then
    TEST_RESULTS+=("Vector Indexing Test: SUCCESS")
else
    TEST_RESULTS+=("Vector Indexing Test: FAILED")
fi

# Display results summary
echo -e "\n${BLUE}==========================================${NC}"
echo -e "${BLUE}  Test Results Summary                   ${NC}"
echo -e "${BLUE}==========================================${NC}\n"

for result in "${TEST_RESULTS[@]}"; do
    if [[ $result == *"SUCCESS"* ]]; then
        echo -e "${GREEN}✓ $result${NC}"
    else
        echo -e "${RED}✗ $result${NC}"
    fi
done

echo -e "\n${YELLOW}Note:${NC} If any tests failed, check the output above for details."
echo -e "      You can also run individual tests for more detailed output."
echo -e "      See README.md for more information.\n"
