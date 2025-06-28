#!/bin/bash

# =============================================================================
# Ideal Function Selector Project Runner
# =============================================================================
# This script runs the ideal function selection analysis project
# Author: Generated for ideal_function_selector project
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a file exists
check_file() {
    if [ ! -f "$1" ]; then
        print_error "Required file '$1' not found!"
        return 1
    fi
    return 0
}

# Header
echo "============================================================================="
echo -e "${BLUE}                  IDEAL FUNCTION SELECTOR PROJECT${NC}"
echo "============================================================================="
echo ""

# Check if Python is installed
print_status "Checking Python installation..."
if command_exists python3; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_success "Found $PYTHON_VERSION"
elif command_exists python; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version 2>&1)
    print_success "Found $PYTHON_VERSION"
else
    print_error "Python is not installed or not in PATH!"
    print_error "Please install Python 3.7+ to run this project."
    exit 1
fi

# Check if pip is available
print_status "Checking pip installation..."
if command_exists pip3; then
    PIP_CMD="pip3"
elif command_exists pip; then
    PIP_CMD="pip"
else
    print_warning "pip not found. You may need to install dependencies manually."
    PIP_CMD=""
fi

# Get the project root directory (parent of scripts directory)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check for required Python files in src directory
print_status "Checking required project files in src/..."
required_files=(
    "src/ideal_function_selector.py"
    "src/data_loader.py"
    "src/database_handler.py"
    "src/function_matcher.py"
    "src/visualizer.py"
    "src/exceptions.py"
    "src/main.py"
)

for file in "${required_files[@]}"; do
    if check_file "$file"; then
        print_success "Found $file"
    else
        exit 1
    fi
done

# Check for required data files in data directory
print_status "Checking required data files in data/..."
data_files=("data/train.csv" "data/ideal.csv" "data/test.csv")
missing_data_files=()

for file in "${data_files[@]}"; do
    if check_file "$file"; then
        print_success "Found $file"
    else
        missing_data_files+=("$file")
    fi
done

if [ ${#missing_data_files[@]} -ne 0 ]; then
    print_error "Missing required data files: ${missing_data_files[*]}"
    print_error "Please ensure all CSV data files are in the data/ directory."
    exit 1
fi

# Create output directory if it doesn't exist
print_status "Creating output directory..."
mkdir -p output
print_success "Output directory ready"

# Check if virtual environment should be activated
if [ -d "venv" ] || [ -d ".venv" ]; then
    print_status "Virtual environment detected..."
    if [ -d "venv" ]; then
        VENV_PATH="venv"
    else
        VENV_PATH=".venv"
    fi
    
    print_status "Activating virtual environment..."
    source "$VENV_PATH/bin/activate"
    print_success "Virtual environment activated"
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ] && [ -n "$PIP_CMD" ]; then
    print_status "Installing/updating dependencies from requirements.txt..."
    $PIP_CMD install -r requirements.txt
    print_success "Dependencies installed"
fi

# Clean up any previous output files
print_status "Cleaning up previous output files..."
if [ -d "output" ]; then
    rm -f output/*.html output/*.png output/*.db
    print_status "Cleaned output directory"
fi

# Run the main application
echo ""
echo "============================================================================="
print_status "Starting Ideal Function Selection Analysis..."
echo "============================================================================="
echo ""

# Execute the main Python script using module syntax
if $PYTHON_CMD -m src.main; then
    echo ""
    echo "============================================================================="
    print_success "Analysis completed successfully!"
    echo "============================================================================="
    echo ""
    
    # Check for generated output files
    print_status "Checking generated output files..."
    if [ -f "output/results_visualization.html" ]; then
        print_success "Generated: output/results_visualization.html"
    fi
    if [ -f "output/deviation_analysis.html" ]; then
        print_success "Generated: output/deviation_analysis.html"
    fi
    if [ -f "output/ideal_functions.db" ]; then
        print_success "Generated: output/ideal_functions.db"
    fi
    if [ -f "output/matplotlib_visualization.png" ]; then
        print_success "Generated: output/matplotlib_visualization.png"
    fi
    
    echo ""
    print_status "You can now open the HTML files in the output/ directory with your web browser to view the results."
    
else
    echo ""
    echo "============================================================================="
    print_error "Analysis failed!"
    echo "============================================================================="
    print_error "Please check the error messages above and fix any issues."
    exit 1
fi

echo ""
print_success "Project execution completed successfully!"
echo "=============================================================================" 