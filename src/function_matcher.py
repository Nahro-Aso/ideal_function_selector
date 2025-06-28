"""
Model training and selection logic for finding the best ideal functions.

This module implements the core algorithm for selecting ideal functions that best match
training datasets and assigning test data points to the selected ideal functions.
The selection is based on minimizing least squares deviation between training data
and ideal functions.

Algorithm Overview:
    1. For each training dataset, calculate least squares deviation against all ideal functions
    2. Select the ideal function with minimum deviation for each training dataset
    3. For test data assignment, use sqrt(2) * max_training_deviation as threshold
    4. Assign test points to ideal functions if deviation is within threshold

Classes:
    ModelTrainer: Core class implementing the function matching algorithm

Example:
    Basic usage:
    
    >>> trainer = ModelTrainer()
    >>> best_matches = trainer.find_best_ideal_functions(training_data, ideal_data)
    >>> assignments = trainer.assign_test_data(test_data, selected_functions)
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from .data_loader import TrainingFunction, IdealFunction
from .exceptions import DataProcessingError

class ModelTrainer:
    """
    Core class for training and selection logic in the ideal function matching system.
    
    This class implements the mathematical algorithms for:
    - Finding the best ideal function for each training dataset using least squares method
    - Calculating deviation statistics for analysis
    - Assigning test data points to ideal functions based on deviation thresholds
    - Maintaining training summaries and statistics
    
    The class uses the least squares method to find the ideal function that minimizes
    the sum of squared deviations from each training dataset.
    
    Attributes:
        best_ideal_functions (Dict[int, IdealFunction]): Mapping of training dataset 
                                                        numbers to their best ideal functions
        training_deviations (Dict[int, Dict]): Detailed deviation statistics for each 
                                             training dataset including total deviation,
                                             max point deviation, and individual point deviations
    
    Example:
        >>> trainer = ModelTrainer()
        >>> 
        >>> # Find best matches for training data
        >>> best_matches = trainer.find_best_ideal_functions(
        ...     training_functions, ideal_functions
        ... )
        >>> 
        >>> # Assign test data to selected functions
        >>> selected_functions = {num: ideal_functions[ideal_num] 
        ...                      for num, ideal_num in best_matches.items()}
        >>> assignments = trainer.assign_test_data(test_data, selected_functions)
        >>> 
        >>> # Get summary statistics
        >>> summary = trainer.get_training_summary()
    """
    
    def __init__(self):
        """
        Initialize the ModelTrainer with empty storage for results.
        
        Sets up internal data structures to store the best ideal functions
        and detailed deviation statistics that will be populated during
        the training and selection process.
        """
        self.best_ideal_functions: Dict[int, Any] = {}
        self.training_deviations: Dict[int, Dict[str, Any]] = {}

    def find_best_ideal_functions(self, 
                                training_functions: Dict[int, TrainingFunction], 
                                ideal_functions: Dict[int, IdealFunction]) -> Dict[int, int]:
        """
        Find the best ideal function for each training dataset using least squares method.
        
        This method implements the core algorithm of the system. For each training dataset,
        it calculates the least squares deviation against all available ideal functions
        and selects the one with minimum deviation. The deviation is calculated as the
        sum of squared differences between training data points and ideal function values.
        
        Mathematical Formula:
            deviation = Σ(y_training - y_ideal)² for all data points
        
        Args:
            training_functions (Dict[int, TrainingFunction]): Dictionary mapping training 
                                                            dataset numbers (1-4) to 
                                                            TrainingFunction objects
            ideal_functions (Dict[int, IdealFunction]): Dictionary mapping ideal function 
                                                      numbers (1-50) to IdealFunction objects
        
        Returns:
            Dict[int, int]: Dictionary mapping training dataset numbers to the ideal 
                          function numbers that best match them
                          Example: {1: 23, 2: 7, 3: 45, 4: 12}
        
        Raises:
            DataProcessingError: If no ideal function is found for a training dataset
                               or if there are issues during the calculation process
        
        Side Effects:
            - Updates self.best_ideal_functions with the selected ideal functions
            - Updates self.training_deviations with detailed statistics
            - Sets max_training_deviation on selected ideal functions
            - Prints progress information to console
        
        Example:
            >>> training_data = {1: train_func1, 2: train_func2}
            >>> ideal_data = {1: ideal_func1, 2: ideal_func2, 3: ideal_func3}
            >>> 
            >>> best_matches = trainer.find_best_ideal_functions(training_data, ideal_data)
            >>> print(best_matches)  # {1: 2, 2: 1} - training 1 matches ideal 2, etc.
        """
        try:
            best_matches = {}
            
            for train_num, train_func in training_functions.items():
                print(f"Finding best ideal function for training dataset {train_num}...")
                
                best_ideal_num = None
                min_deviation = float('inf')
                best_deviations = []
                
                # Test each ideal function against this training dataset
                for ideal_num, ideal_func in ideal_functions.items():
                    deviation = train_func.calculate_deviation(ideal_func)
                    
                    if deviation < min_deviation:
                        min_deviation = deviation
                        best_ideal_num = ideal_num
                        best_deviations = self._calculate_point_deviations(train_func, ideal_func)
                
                if best_ideal_num is None:
                    raise DataProcessingError(f"No ideal function found for training dataset {train_num}")
                
                # Store the best match
                best_matches[train_num] = best_ideal_num
                
                # Calculate and store maximum point deviation for test data threshold
                max_dev = max(best_deviations) if best_deviations else 0
                ideal_functions[best_ideal_num].set_max_training_deviation(max_dev)
                
                # Store detailed deviation statistics
                self.training_deviations[train_num] = {
                    'total_deviation': min_deviation,
                    'max_point_deviation': max_dev,
                    'point_deviations': best_deviations
                }
                
                print(f"  Best match: Ideal function {best_ideal_num} (deviation: {min_deviation:.4f})")
            
            # Store the best ideal functions for later use
            self.best_ideal_functions = {train_num: ideal_functions[ideal_num] 
                                       for train_num, ideal_num in best_matches.items()}
            
            return best_matches
            
        except Exception as e:
            raise DataProcessingError(f"Error finding best ideal functions: {str(e)}", "model_training")

    def _calculate_point_deviations(self, 
                                  train_func: TrainingFunction, 
                                  ideal_func: IdealFunction) -> List[float]:
        """
        Calculate individual point deviations between training and ideal functions.
        
        This private method computes the absolute deviation at each x-coordinate
        between the training function and ideal function values. These point-wise
        deviations are used for statistical analysis and threshold calculations.
        
        Args:
            train_func (TrainingFunction): Training function to compare
            ideal_func (IdealFunction): Ideal function to compare against
        
        Returns:
            List[float]: List of absolute deviations at each x-coordinate
                        |y_training - y_ideal| for each point
        
        Example:
            >>> # If training has points [(1, 2), (2, 4)] and ideal has [(1, 2.1), (2, 3.9)]
            >>> deviations = trainer._calculate_point_deviations(train_func, ideal_func)
            >>> print(deviations)  # [0.1, 0.1]
        """
        deviations = []
        for x, y in zip(train_func.x_values, train_func.y_values):
            ideal_y = ideal_func.interpolate_y(x)
            deviations.append(abs(y - ideal_y))
        return deviations

    def assign_test_data(self, 
                        test_data, 
                        selected_ideal_functions: Dict[int, IdealFunction]) -> List[Dict[str, Any]]:
        """
        Assign test data points to ideal functions based on deviation thresholds.
        
        This method implements the test data assignment algorithm. For each test point,
        it calculates the deviation to each selected ideal function and assigns the
        point to the function with minimum deviation, provided the deviation is within
        the threshold of sqrt(2) * max_training_deviation.
        
        Assignment Criteria:
            - Calculate deviation from test point to each ideal function
            - Check if deviation <= sqrt(2) * max_training_deviation for that function
            - Assign to function with minimum valid deviation
            - If no function meets criteria, leave unassigned
        
        Args:
            test_data (pd.DataFrame): DataFrame containing test data with 'x' and 'y' columns
            selected_ideal_functions (Dict[int, IdealFunction]): Dictionary mapping training 
                                                               dataset numbers to their selected 
                                                               ideal functions
        
        Returns:
            List[Dict[str, Any]]: List of assignment dictionaries, each containing:
                - 'x' (float): x-coordinate of test point
                - 'y' (float): y-coordinate of test point  
                - 'assigned_ideal_function' (int or None): Number of assigned ideal function
                - 'deviation' (float or None): Deviation value for assignment
                - 'training_dataset' (int or None): Training dataset associated with assignment
        
        Raises:
            DataProcessingError: If there are issues during the assignment process
        
        Side Effects:
            - Prints assignment summary to console
        
        Example:
            >>> test_df = pd.DataFrame({'x': [1, 2, 3], 'y': [1.5, 2.5, 3.5]})
            >>> selected_funcs = {1: ideal_func_23, 2: ideal_func_7}
            >>> 
            >>> assignments = trainer.assign_test_data(test_df, selected_funcs)
            >>> 
            >>> # Example output:
            >>> for assignment in assignments:
            ...     if assignment['assigned_ideal_function']:
            ...         print(f"Point ({assignment['x']}, {assignment['y']}) "
            ...               f"assigned to function {assignment['assigned_ideal_function']}")
        """
        try:
            assignments = []
            
            for _, row in test_data.iterrows():
                x, y = row['x'], row['y']
                best_assignment = None
                min_deviation = float('inf')
                
                # Check each selected ideal function for this test point
                for train_num, ideal_func in selected_ideal_functions.items():
                    is_valid, deviation = ideal_func.is_test_point_valid(x, y)
                    
                    # Assign to function with minimum deviation if valid
                    if is_valid and deviation < min_deviation:
                        min_deviation = deviation
                        best_assignment = {
                            'x': x,
                            'y': y,
                            'assigned_ideal_function': ideal_func.function_number,
                            'deviation': deviation,
                            'training_dataset': train_num
                        }
                
                # Store assignment result (None if no valid assignment found)
                if best_assignment is None:
                    assignments.append({
                        'x': x,
                        'y': y,
                        'assigned_ideal_function': None,
                        'deviation': None,
                        'training_dataset': None
                    })
                else:
                    assignments.append(best_assignment)
            
            # Print assignment summary
            assigned_count = len([a for a in assignments if a['assigned_ideal_function'] is not None])
            print(f"Assigned {assigned_count} out of {len(assignments)} test points")
            
            return assignments
            
        except Exception as e:
            raise DataProcessingError(f"Error assigning test data: {str(e)}", "test_assignment")

    def get_training_summary(self) -> Dict[str, Any]:
        """
        Generate a comprehensive summary of the training and selection results.
        
        This method compiles all the statistics and results from the training process
        into a structured dictionary that can be used for reporting and visualization.
        
        Returns:
            Dict[str, Any]: Comprehensive summary containing:
                - 'total_training_datasets' (int): Number of training datasets processed
                - 'best_matches' (Dict[int, Dict]): For each training dataset:
                    - 'ideal_function_number' (int): Selected ideal function number
                    - 'total_deviation' (float): Total least squares deviation
                    - 'max_point_deviation' (float): Maximum single point deviation
                - 'deviations' (Dict): Complete deviation statistics from training process
        
        Example:
            >>> summary = trainer.get_training_summary()
            >>> print(f"Processed {summary['total_training_datasets']} datasets")
            >>> 
            >>> for train_num, match_info in summary['best_matches'].items():
            ...     print(f"Training {train_num} -> Ideal {match_info['ideal_function_number']}")
            ...     print(f"  Total deviation: {match_info['total_deviation']:.4f}")
            ...     print(f"  Max point deviation: {match_info['max_point_deviation']:.4f}")
        """
        summary = {
            'total_training_datasets': len(self.best_ideal_functions),
            'best_matches': {},
            'deviations': self.training_deviations
        }
        
        for train_num, ideal_func in self.best_ideal_functions.items():
            summary['best_matches'][train_num] = {
                'ideal_function_number': ideal_func.function_number,
                'total_deviation': self.training_deviations[train_num]['total_deviation'],
                'max_point_deviation': self.training_deviations[train_num]['max_point_deviation']
            }
        
        return summary
