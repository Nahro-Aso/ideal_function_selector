"""
Main entry point for the ideal function selection application.
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from ideal_function_selector import IdealFunctionSelector


def main():
    """Main function to run the application."""
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # File paths - now pointing to data directory
    data_dir = os.path.join(project_root, "data")
    training_file = os.path.join(data_dir, "train.csv")
    ideal_file = os.path.join(data_dir, "ideal.csv")
    test_file = os.path.join(data_dir, "test.csv")
    
    # Database will be created in output directory
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)
    db_path = os.path.join(output_dir, "ideal_functions.db")
    
    # Verify files exist
    all_files = [training_file, ideal_file, test_file]
    missing_files = [f for f in all_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"Error: Missing files: {missing_files}")
        print("Please ensure all required CSV files are in the data/ directory.")
        return
    
    # Run the analysis
    try:
        selector = IdealFunctionSelector(db_path)
        selector.run_complete_analysis(training_file, ideal_file, test_file)
        print(f"\nResults saved to: {output_dir}")
    except Exception as e:
        print(f"Application error: {str(e)}")


if __name__ == "__main__":
    main()
