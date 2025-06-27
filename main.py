"""
Main entry point for the ideal function selection application.
"""

import os
from ideal_function_selector import IdealFunctionSelector


def main():
    """Main function to run the application."""
    # File paths
    training_file = "train.csv"
    ideal_file = "ideal.csv"
    test_file = "test.csv"
    
    # Verify files exist
    all_files = [training_file, ideal_file, test_file]
    missing_files = [f for f in all_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"Error: Missing files: {missing_files}")
        print("Please ensure all required CSV files are in the current directory.")
        return
    
    # Run the analysis
    try:
        selector = IdealFunctionSelector()
        selector.run_complete_analysis(training_file, ideal_file, test_file)
    except Exception as e:
        print(f"Application error: {str(e)}")


if __name__ == "__main__":
    main()
