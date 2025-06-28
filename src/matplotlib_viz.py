"""
Alternative visualization using matplotlib for immediate viewing.

This module provides a matplotlib-based visualization system as an alternative to the main
Bokeh-based visualizer. It creates immediate, high-quality visualizations of the ideal
function selection results that can be viewed directly or saved as image files.

The visualization includes:
- Training datasets (scatter plots with different colors)
- Selected ideal functions (smooth curves)
- Test data points (colored by assignment status)
- Statistical summaries and legends

This module is particularly useful for:
- Quick visual inspection of results
- Generating publication-ready figures
- Systems where Bokeh might not be available
- Creating static visualizations for reports

Functions:
    create_matplotlib_visualization(): Main function to create and display visualizations

Example:
    Basic usage:
    
    >>> from matplotlib_viz import create_matplotlib_visualization
    >>> create_matplotlib_visualization()
    
    This will create a comprehensive plot showing all training data, selected ideal
    functions, and test point assignments, saving it as 'matplotlib_visualization.png'
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from data_loader import DataReader, TrainingFunction, IdealFunction
from function_matcher import ModelTrainer

def create_matplotlib_visualization() -> None:
    """
    Create a comprehensive matplotlib visualization of the ideal function selection results.
    
    This function performs the complete analysis workflow and creates a detailed
    visualization showing:
    
    1. Training datasets as colored scatter points
    2. Selected ideal functions as smooth curves
    3. Test data points colored by assignment status:
       - Green squares: Successfully assigned test points
       - Red triangles: Unassigned test points
    4. Legend with detailed information
    5. Statistical summary printed to console
    
    The visualization uses a 15x10 inch figure with high DPI for publication quality.
    Color coding ensures clear distinction between different components:
    - Blue, Orange, Green, Red: Training datasets 1-4
    - Matching colors: Corresponding ideal functions
    - Dark green: Assigned test points
    - Dark red: Unassigned test points
    
    File Operations:
        - Reads 'train.csv', 'ideal.csv', and 'test.csv' from current directory
        - Saves visualization as 'matplotlib_visualization.png' (300 DPI)
        - Displays plot using matplotlib.pyplot.show()
    
    Console Output:
        - Progress information during data loading and processing
        - Summary statistics including:
            - Number of training datasets and ideal functions
            - Test point assignment counts
            - Best match mappings with deviation values
    
    Raises:
        FileNotFoundError: If required CSV files are not found
        DataProcessingError: If there are issues with data processing
        Exception: For other visualization or matplotlib-related errors
    
    Side Effects:
        - Creates 'matplotlib_visualization.png' in current directory
        - Displays plot window (if running in interactive environment)
        - Prints detailed analysis results to console
    
    Example:
        >>> # Ensure data files are in current directory
        >>> # train.csv, ideal.csv, test.csv
        >>> 
        >>> create_matplotlib_visualization()
        Creating matplotlib visualization...
        Successfully loaded 4 training datasets
        Successfully loaded 50 ideal functions
        Successfully loaded 100 test data points
        Finding best ideal function for training dataset 1...
        ...
        Matplotlib visualization saved as 'matplotlib_visualization.png'
        
        📊 VISUALIZATION SUMMARY:
        Training Datasets: 4 (shown as colored circles)
        Selected Ideal Functions: 4 (shown as colored lines)
        Test Points Assigned: 85 (green squares)
        Test Points Unassigned: 15 (red triangles)
        Total Test Points: 100
    """
    
    print("Creating matplotlib visualization...")
    
    try:
        # Load data using the data reader component
        import os
        data_reader = DataReader()
        
        # Get paths to data files in the data directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        data_dir = os.path.join(project_root, "data")
        
        training_file = os.path.join(data_dir, "train.csv")
        ideal_file = os.path.join(data_dir, "ideal.csv")
        test_file = os.path.join(data_dir, "test.csv")
        
        training_functions = data_reader.read_training_data(training_file)
        ideal_functions = data_reader.read_ideal_data(ideal_file)
        test_data = data_reader.read_test_data(test_file)
        
        # Find best matches using the model trainer
        model_trainer = ModelTrainer()
        best_matches = model_trainer.find_best_ideal_functions(training_functions, ideal_functions)
        
        # Get selected ideal functions based on best matches
        selected_ideal_functions = {train_num: ideal_functions[ideal_num] 
                                   for train_num, ideal_num in best_matches.items()}
        
        # Assign test data to selected ideal functions
        test_assignments = model_trainer.assign_test_data(test_data, selected_ideal_functions)
        
        # Create the matplotlib figure with specified size for clarity
        plt.figure(figsize=(15, 10))
        
        # Define consistent colors for training datasets and their ideal functions
        colors = ['blue', 'orange', 'green', 'red']
        
        # Plot training data as scatter points
        for i, (train_num, train_func) in enumerate(training_functions.items()):
            plt.scatter(train_func.x_values, train_func.y_values, 
                       c=colors[i], alpha=0.7, s=50, 
                       label=f'Training Dataset {train_num}')
        
        # Plot selected ideal functions as smooth curves
        for i, (train_num, ideal_func) in enumerate(selected_ideal_functions.items()):
            # Create smooth x range for ideal function curves
            x_range = np.linspace(min(ideal_func.x_values), max(ideal_func.x_values), 200)
            y_range = [ideal_func.interpolate_y(x) for x in x_range]
            plt.plot(x_range, y_range, 
                    color=colors[i], linewidth=2, alpha=0.8,
                    label=f'Ideal Function {ideal_func.function_number}')
        
        # Separate test data by assignment status for different styling
        assigned_x = [a['x'] for a in test_assignments if a['assigned_ideal_function'] is not None]
        assigned_y = [a['y'] for a in test_assignments if a['assigned_ideal_function'] is not None]
        unassigned_x = [a['x'] for a in test_assignments if a['assigned_ideal_function'] is None]
        unassigned_y = [a['y'] for a in test_assignments if a['assigned_ideal_function'] is None]
        
        # Plot assigned test points as green squares
        if assigned_x:
            plt.scatter(assigned_x, assigned_y, 
                       c='darkgreen', marker='s', s=100, alpha=0.8,
                       label=f'Assigned Test Points ({len(assigned_x)})')
        
        # Plot unassigned test points as red triangles
        if unassigned_x:
            plt.scatter(unassigned_x, unassigned_y, 
                       c='darkred', marker='^', s=100, alpha=0.8,
                       label=f'Unassigned Test Points ({len(unassigned_x)})')
        
        # Configure plot appearance and labels
        plt.xlabel('X Values', fontsize=12)
        plt.ylabel('Y Values', fontsize=12)
        plt.title('Ideal Function Selection Results', fontsize=14, fontweight='bold')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save the plot as high-resolution PNG in the output directory
        output_dir = os.path.join(project_root, "output")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'matplotlib_visualization.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Matplotlib visualization saved as '{output_path}'")
        
        # Print comprehensive summary to console
        print(f"\n📊 VISUALIZATION SUMMARY:")
        print(f"Training Datasets: 4 (shown as colored circles)")
        print(f"Selected Ideal Functions: 4 (shown as colored lines)")
        print(f"Test Points Assigned: {len(assigned_x)} (green squares)")
        print(f"Test Points Unassigned: {len(unassigned_x)} (red triangles)")
        print(f"Total Test Points: {len(test_assignments)}")
        
        # Print best matches with deviation information
        print(f"\n🎯 BEST MATCHES:")
        for train_num, ideal_num in best_matches.items():
            deviation = model_trainer.training_deviations[train_num]['total_deviation']
            print(f"Training Dataset {train_num} → Ideal Function {ideal_num} (deviation: {deviation:.2f})")
    
    except FileNotFoundError as e:
        print(f"Error: Required data files not found. Please ensure train.csv, ideal.csv, and test.csv are in the data/ directory.")
        print(f"Details: {e}")
        raise
    
    except Exception as e:
        print(f"Error creating matplotlib visualization: {str(e)}")
        raise

if __name__ == "__main__":
    """
    Execute the visualization when script is run directly.
    
    This allows the module to be used as a standalone script:
    $ python matplotlib_viz.py
    
    The visualization will be created and saved automatically.
    """
    create_matplotlib_visualization()
