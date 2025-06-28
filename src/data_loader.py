"""
Data handling classes with object-oriented design and inheritance.

This module implements a robust object-oriented data handling system for the ideal
function selection project. It uses inheritance and abstract base classes to create
a clean, extensible architecture for handling different types of mathematical functions.

Key Design Principles:
    - Abstract base class (BaseFunction) defines common interface
    - Concrete implementations for specific function types (TrainingFunction, IdealFunction)
    - Encapsulation of data validation and mathematical operations
    - Type safety with comprehensive error handling
    - Separation of concerns between data reading and function operations

Class Hierarchy:
    BaseFunction (ABC)
    ├── TrainingFunction: Represents training datasets with deviation calculations
    └── IdealFunction: Represents ideal functions with test point validation

The design follows SOLID principles:
    - Single Responsibility: Each class has a specific purpose
    - Open/Closed: Extensible through inheritance, closed for modification
    - Liskov Substitution: Derived classes can replace base class
    - Interface Segregation: Focused interfaces for specific needs
    - Dependency Inversion: Depends on abstractions, not concretions

Classes:
    BaseFunction: Abstract base class for all mathematical functions
    TrainingFunction: Concrete implementation for training datasets
    IdealFunction: Concrete implementation for ideal functions with validation
    DataReader: File I/O handler for CSV data loading

Example:
    Basic usage of the data handling system:
    
    >>> reader = DataReader()
    >>> training_data = reader.read_training_data("train.csv")
    >>> ideal_data = reader.read_ideal_data("ideal.csv")
    >>> 
    >>> # Use the loaded functions
    >>> deviation = training_data[1].calculate_deviation(ideal_data[23])
    >>> is_valid, dev = ideal_data[23].is_test_point_valid(1.5, 2.3)
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Any
from exceptions import DataProcessingError, ValidationError


class BaseFunction(ABC):
    """
    Abstract base class for all mathematical functions in the system.
    
    This class defines the common interface and shared functionality for all
    function types (training and ideal functions). It implements the Template
    Method pattern where common operations are defined in the base class and
    specific implementations are delegated to derived classes.
    
    Key Features:
        - Data validation ensuring x and y arrays have consistent lengths
        - Linear interpolation capability for y-value estimation
        - Abstract method for deviation calculation (implemented by subclasses)
        - Type safety with proper error handling
    
    Attributes:
        x_values (np.ndarray): X-coordinates of the function points
        y_values (np.ndarray): Y-coordinates of the function points  
        function_id (str): Unique identifier for the function
    
    Abstract Methods:
        calculate_deviation: Must be implemented by subclasses for specific
                           deviation calculation logic
    
    Example:
        This is an abstract class, so it cannot be instantiated directly:
        
        >>> # This would raise TypeError
        >>> # func = BaseFunction(x_vals, y_vals, "test")
        
        >>> # Instead, use concrete implementations:
        >>> train_func = TrainingFunction(x_vals, y_vals, 1)
        >>> ideal_func = IdealFunction(x_vals, y_vals, 23)
    """
    
    def __init__(self, x_values: np.ndarray, y_values: np.ndarray, function_id: str):
        """
        Initialize the base function with coordinate data and identifier.
        
        Args:
            x_values (np.ndarray): Array of x-coordinates for the function
            y_values (np.ndarray): Array of y-coordinates for the function
            function_id (str): Unique identifier for this function
                             (e.g., "training_1", "ideal_23")
        
        Raises:
            ValidationError: If x_values and y_values arrays have different lengths
        
        Note:
            This constructor automatically calls validate_data() to ensure
            data consistency before the object is fully initialized.
        """
        self.x_values = x_values
        self.y_values = y_values
        self.function_id = function_id
        self.validate_data()

    def validate_data(self) -> None:
        """
        Validate that x and y coordinate arrays are consistent.
        
        This method ensures that the x and y arrays have the same length,
        which is essential for proper mathematical operations. It's called
        automatically during initialization.
        
        Raises:
            ValidationError: If the arrays have different lengths, with a
                           descriptive message including the function ID
        
        Example:
            >>> # This validation happens automatically in __init__
            >>> x = np.array([1, 2, 3])
            >>> y = np.array([4, 5])  # Different length!
            >>> # TrainingFunction(x, y, 1) would raise ValidationError
        """
        if len(self.x_values) != len(self.y_values):
            raise ValidationError(f"X and Y arrays must have the same length for function {self.function_id}")

    @abstractmethod
    def calculate_deviation(self, other_function: 'BaseFunction') -> float:
        """
        Calculate deviation between this function and another function.
        
        This abstract method must be implemented by all concrete subclasses
        to define how deviation is calculated. Different function types may
        use different deviation calculation strategies.
        
        Args:
            other_function (BaseFunction): Another function to compare against
        
        Returns:
            float: Deviation value (interpretation depends on implementation)
        
        Note:
            This method uses the Template Method pattern - the interface is
            defined here but the implementation is delegated to subclasses.
        """
        pass

    def interpolate_y(self, x: float) -> float:
        """
        Interpolate y-value for a given x-coordinate using linear interpolation.
        
        This method uses NumPy's linear interpolation to estimate y-values
        for x-coordinates that may not exist in the original data. This is
        essential for comparing functions with different x-coordinate sets.
        
        Args:
            x (float): X-coordinate for which to interpolate the y-value
        
        Returns:
            float: Interpolated y-value at the given x-coordinate
        
        Interpolation Behavior:
            - For x within the range: Linear interpolation between nearest points
            - For x outside the range: Extrapolation using nearest edge values
        
        Example:
            >>> # Function with points [(0, 0), (2, 4), (4, 8)]
            >>> y = func.interpolate_y(1.0)  # Returns 2.0 (linear interpolation)
            >>> y = func.interpolate_y(3.0)  # Returns 6.0
            >>> y = func.interpolate_y(-1.0) # Extrapolates to -2.0
        """
        return np.interp(x, self.x_values, self.y_values)

class TrainingFunction(BaseFunction):
    """
    Concrete implementation of BaseFunction for training datasets.
    
    This class represents training data functions used to find the best matching
    ideal functions. It implements least squares deviation calculation and
    maintains metadata about the training dataset.
    
    Key Features:
        - Least squares deviation calculation against other functions
        - Dataset number tracking for identification
        - Integration with the model training workflow
        - Error handling for mathematical operations
    
    Attributes:
        dataset_number (int): Number identifying this training dataset (1-4)
        x_values (np.ndarray): Inherited x-coordinates
        y_values (np.ndarray): Inherited y-coordinates
        function_id (str): Generated identifier (e.g., "training_1")
    
    Mathematical Formula:
        The deviation calculation uses least squares method:
        deviation = Σ(y_training - y_other)² for all data points
    
    Example:
        >>> x_data = np.array([1, 2, 3, 4])
        >>> y_data = np.array([2, 4, 6, 8])
        >>> train_func = TrainingFunction(x_data, y_data, dataset_number=1)
        >>> 
        >>> # Calculate deviation against an ideal function
        >>> deviation = train_func.calculate_deviation(ideal_func)
        >>> print(f"Least squares deviation: {deviation:.4f}")
    """
    
    def __init__(self, x_values: np.ndarray, y_values: np.ndarray, dataset_number: int):
        """
        Initialize a training function with dataset number.
        
        Args:
            x_values (np.ndarray): Array of x-coordinates for the training data
            y_values (np.ndarray): Array of y-coordinates for the training data
            dataset_number (int): Training dataset number (typically 1-4)
        
        Note:
            The function_id is automatically generated as "training_{dataset_number}"
            and data validation is performed by the parent class constructor.
        """
        super().__init__(x_values, y_values, f"training_{dataset_number}")
        self.dataset_number = dataset_number

    def calculate_deviation(self, other_function: BaseFunction) -> float:
        """
        Calculate least squares deviation between this training function and another function.
        
        This method implements the core mathematical operation for function comparison
        using the least squares method. For each x-coordinate in this training function,
        it interpolates the corresponding y-value from the other function and calculates
        the squared difference.
        
        Args:
            other_function (BaseFunction): Function to compare against (typically an IdealFunction)
        
        Returns:
            float: Sum of squared deviations (least squares deviation)
        
        Raises:
            DataProcessingError: If there are issues during the calculation process
        
        Mathematical Process:
            1. For each (x, y) point in this training function
            2. Interpolate corresponding y-value from other function
            3. Calculate squared difference: (y_training - y_other)²
            4. Sum all squared differences
        
        Example:
            >>> train_func = TrainingFunction(x_data, y_data, 1)
            >>> ideal_func = IdealFunction(x_ideal, y_ideal, 23)
            >>> 
            >>> deviation = train_func.calculate_deviation(ideal_func)
            >>> print(f"Training dataset 1 vs Ideal function 23: {deviation:.4f}")
        """
        try:
            squared_differences = []
            for x, y in zip(self.x_values, self.y_values):
                # Get corresponding y-value from other function via interpolation
                other_y = other_function.interpolate_y(x)
                # Calculate squared difference
                squared_differences.append((y - other_y) ** 2)
            
            # Return sum of squared differences (least squares deviation)
            return sum(squared_differences)
        except Exception as e:
            raise DataProcessingError(f"Error calculating deviation: {str(e)}", "training_function")

class IdealFunction(BaseFunction):
    """
    Concrete implementation of BaseFunction for ideal functions.
    
    This class represents ideal functions that can be selected to match training
    datasets and validate test data points. It implements sophisticated test point
    validation using the sqrt(2) * max_training_deviation threshold criterion.
    
    Key Features:
        - Bidirectional deviation calculation (delegates to other function)
        - Test point validation with configurable thresholds
        - Maximum training deviation tracking for threshold calculations
        - Integration with test data assignment workflow
    
    Attributes:
        function_number (int): Number identifying this ideal function (1-50)
        max_training_deviation (float, optional): Maximum point deviation during training
                                                 Used for test data validation threshold
        x_values (np.ndarray): Inherited x-coordinates
        y_values (np.ndarray): Inherited y-coordinates
        function_id (str): Generated identifier (e.g., "ideal_23")
    
    Validation Criteria:
        A test point (x, y) is valid for assignment if:
        |y_test - y_ideal| <= sqrt(2) * max_training_deviation
    
    Example:
        >>> x_data = np.array([1, 2, 3, 4])
        >>> y_data = np.array([1.1, 3.9, 6.1, 7.9])
        >>> ideal_func = IdealFunction(x_data, y_data, function_number=23)
        >>> 
        >>> # Set maximum training deviation (usually done during training)
        >>> ideal_func.set_max_training_deviation(0.2)
        >>> 
        >>> # Validate a test point
        >>> is_valid, deviation = ideal_func.is_test_point_valid(2.5, 5.0)
        >>> if is_valid:
        ...     print(f"Test point is valid with deviation: {deviation:.4f}")
    """
    
    def __init__(self, x_values: np.ndarray, y_values: np.ndarray, function_number: int):
        """
        Initialize an ideal function with function number.
        
        Args:
            x_values (np.ndarray): Array of x-coordinates for the ideal function
            y_values (np.ndarray): Array of y-coordinates for the ideal function
            function_number (int): Ideal function number (typically 1-50)
        
        Note:
            - The function_id is automatically generated as "ideal_{function_number}"
            - max_training_deviation is initialized as None and must be set later
            - Data validation is performed by the parent class constructor
        """
        super().__init__(x_values, y_values, f"ideal_{function_number}")
        self.function_number = function_number
        self.max_training_deviation: Optional[float] = None

    def calculate_deviation(self, other_function: BaseFunction) -> float:
        """
        Calculate deviation by delegating to the other function.
        
        This method implements a delegation pattern where the actual deviation
        calculation is performed by the other function. This design allows
        different function types to implement their own deviation calculation
        strategies while maintaining a consistent interface.
        
        Args:
            other_function (BaseFunction): Function to calculate deviation with
                                         (typically a TrainingFunction)
        
        Returns:
            float: Deviation value as calculated by the other function
        
        Design Rationale:
            This delegation ensures that training functions control how deviation
            is calculated, which is appropriate since they implement the least
            squares method specific to the training process.
        
        Example:
            >>> ideal_func = IdealFunction(x_data, y_data, 23)
            >>> train_func = TrainingFunction(x_train, y_train, 1)
            >>> 
            >>> # These two calls are equivalent due to delegation:
            >>> dev1 = train_func.calculate_deviation(ideal_func)
            >>> dev2 = ideal_func.calculate_deviation(train_func)
            >>> assert dev1 == dev2
        """
        return other_function.calculate_deviation(self)

    def set_max_training_deviation(self, deviation: float) -> None:
        """
        Set the maximum training deviation for test data validation.
        
        This method stores the maximum point deviation observed during the
        training phase, which is used to establish the threshold for test
        data point validation. The threshold is calculated as sqrt(2) times
        this maximum deviation.
        
        Args:
            deviation (float): Maximum point deviation observed during training
                             phase when this ideal function was matched to training data
        
        Note:
            This method is typically called automatically during the training
            process by the ModelTrainer class after finding the best ideal
            function for each training dataset.
        
        Example:
            >>> ideal_func = IdealFunction(x_data, y_data, 23)
            >>> # This is usually called by ModelTrainer
            >>> ideal_func.set_max_training_deviation(0.15)
            >>> 
            >>> # Now test points can be validated
            >>> is_valid, dev = ideal_func.is_test_point_valid(x_test, y_test)
        """
        self.max_training_deviation = deviation

    def is_test_point_valid(self, x: float, y: float) -> Tuple[bool, float]:
        """
        Validate whether a test point can be assigned to this ideal function.
        
        This method implements the core test data validation algorithm using the
        sqrt(2) * max_training_deviation threshold. It first interpolates the
        ideal function value at the test point's x-coordinate, calculates the
        deviation, and compares it against the threshold.
        
        Args:
            x (float): X-coordinate of the test point
            y (float): Y-coordinate of the test point
        
        Returns:
            Tuple[bool, float]: 
                - bool: True if the test point is valid for assignment, False otherwise
                - float: Actual deviation between test point and ideal function
        
        Raises:
            ValidationError: If max_training_deviation has not been set
        
        Validation Algorithm:
            1. Check that max_training_deviation is set
            2. Interpolate ideal function value at x-coordinate
            3. Calculate absolute deviation: |y_test - y_ideal|
            4. Calculate threshold: sqrt(2) * max_training_deviation
            5. Return (deviation <= threshold, deviation)
        
        Mathematical Justification:
            The sqrt(2) factor provides a reasonable tolerance for test point
            assignment while preventing over-assignment of outliers.
        
        Example:
            >>> ideal_func = IdealFunction(x_data, y_data, 23)
            >>> ideal_func.set_max_training_deviation(0.1)
            >>> 
            >>> # Test a point close to the ideal function
            >>> is_valid, dev = ideal_func.is_test_point_valid(2.0, 4.05)
            >>> print(f"Valid: {is_valid}, Deviation: {dev:.4f}")
            >>> 
            >>> # Test a point far from the ideal function
            >>> is_valid, dev = ideal_func.is_test_point_valid(2.0, 10.0)
            >>> print(f"Valid: {is_valid}, Deviation: {dev:.4f}")
        """
        if self.max_training_deviation is None:
            raise ValidationError("Max training deviation not set for ideal function")
        
        # Interpolate ideal function value at test point x-coordinate
        ideal_y = self.interpolate_y(x)
        
        # Calculate absolute deviation
        deviation = abs(y - ideal_y)
        
        # Calculate threshold using sqrt(2) factor
        threshold = np.sqrt(2) * self.max_training_deviation
        
        # Return validation result and actual deviation
        return deviation <= threshold, deviation

class DataReader:
    """
    File I/O handler for loading CSV data into function objects.
    
    This class provides a clean interface for reading different types of CSV data
    files and converting them into appropriate function objects. It handles file
    validation, error reporting, and maintains separation of concerns between
    file operations and mathematical function operations.
    
    Key Features:
        - Specialized methods for different data types (training, ideal, test)
        - Comprehensive error handling with descriptive error messages
        - Data validation and consistency checking
        - Progress reporting during data loading
        - Storage of loaded data for later access
    
    Supported File Formats:
        - Training data: CSV with columns 'x', 'y1', 'y2', 'y3', 'y4'
        - Ideal data: CSV with columns 'x', 'y1', 'y2', ..., 'y50'
        - Test data: CSV with columns 'x', 'y'
    
    Attributes:
        training_data (Dict[int, TrainingFunction]): Loaded training functions
        ideal_data (Dict[int, IdealFunction]): Loaded ideal functions
        test_data (pd.DataFrame): Loaded test data
    
    Example:
        >>> reader = DataReader()
        >>> 
        >>> # Load all data types
        >>> training_funcs = reader.read_training_data("train.csv")
        >>> ideal_funcs = reader.read_ideal_data("ideal.csv")
        >>> test_df = reader.read_test_data("test.csv")
        >>> 
        >>> # Access loaded data
        >>> print(f"Loaded {len(training_funcs)} training datasets")
        >>> print(f"Loaded {len(ideal_funcs)} ideal functions")
        >>> print(f"Loaded {len(test_df)} test points")
    """
    
    def __init__(self):
        """
        Initialize the DataReader with empty storage for loaded data.
        
        The data storage attributes are initialized as empty and will be
        populated when the respective read methods are called.
        """
        self.training_data: Dict[int, TrainingFunction] = {}
        self.ideal_data: Optional[Dict[int, IdealFunction]] = None
        self.test_data: Optional[pd.DataFrame] = None

    def read_training_data(self, file_path: str) -> Dict[int, TrainingFunction]:
        """
        Read training data from CSV file and create TrainingFunction objects.
        
        This method loads training data from a CSV file containing 4 training
        datasets. Each dataset becomes a separate TrainingFunction object with
        shared x-coordinates but different y-values.
        
        Args:
            file_path (str): Path to the CSV file containing training data
        
        Returns:
            Dict[int, TrainingFunction]: Dictionary mapping dataset numbers (1-4)
                                       to TrainingFunction objects
        
        Raises:
            DataProcessingError: If there are issues reading the file or processing the data
            FileNotFoundError: If the specified file doesn't exist
        
        Expected File Format:
            CSV file with columns: 'x', 'y1', 'y2', 'y3', 'y4'
            - 'x': X-coordinates (shared across all training datasets)
            - 'y1'-'y4': Y-values for training datasets 1-4
        
        Side Effects:
            - Updates self.training_data with loaded functions
            - Prints success message with count of loaded datasets
        
        Example:
            >>> reader = DataReader()
            >>> training_funcs = reader.read_training_data("data/train.csv")
            Successfully loaded 4 training datasets
            >>> 
            >>> # Use the loaded functions
            >>> func1 = training_funcs[1]  # First training dataset
            >>> print(f"Dataset 1 has {len(func1.x_values)} points")
        """
        try:
            training_functions = {}
            df = pd.read_csv(file_path)
            
            # Validate required columns
            if 'x' not in df.columns:
                raise DataProcessingError(f"No 'x' column found in {file_path}", "training_data")
            
            x_values = df['x'].values
            
            # Load each training dataset (y1, y2, y3, y4)
            for i in range(1, 5):
                y_col = f'y{i}'
                if y_col not in df.columns:
                    raise DataProcessingError(f"No '{y_col}' column found in {file_path}", "training_data")
                
                y_values = df[y_col].values
                training_functions[i] = TrainingFunction(x_values, y_values, i)
            
            # Store loaded data and report success
            self.training_data = training_functions
            print(f"Successfully loaded {len(training_functions)} training datasets")
            return training_functions
            
        except Exception as e:
            raise DataProcessingError(f"Error reading training data: {str(e)}", "training_data")

    def read_ideal_data(self, file_path: str) -> Dict[int, IdealFunction]:
        """
        Read ideal functions data from CSV file and create IdealFunction objects.
        
        This method loads ideal function data from a CSV file containing up to 50
        ideal functions. Each function becomes a separate IdealFunction object with
        shared x-coordinates but different y-values.
        
        Args:
            file_path (str): Path to the CSV file containing ideal functions data
        
        Returns:
            Dict[int, IdealFunction]: Dictionary mapping function numbers (1-50)
                                    to IdealFunction objects
        
        Raises:
            DataProcessingError: If there are issues reading the file or processing the data
            FileNotFoundError: If the specified file doesn't exist
        
        Expected File Format:
            CSV file with columns: 'x', 'y1', 'y2', ..., 'yN' (where N <= 50)
            - 'x': X-coordinates (shared across all ideal functions)
            - 'y1'-'yN': Y-values for ideal functions 1-N
        
        Side Effects:
            - Updates self.ideal_data with loaded functions
            - Prints success message with count of loaded functions
        
        Flexibility:
            The method automatically detects available columns, so files with
            fewer than 50 ideal functions are handled gracefully.
        
        Example:
            >>> reader = DataReader()
            >>> ideal_funcs = reader.read_ideal_data("data/ideal.csv")
            Successfully loaded 50 ideal functions
            >>> 
            >>> # Use the loaded functions
            >>> func23 = ideal_funcs[23]  # Ideal function 23
            >>> print(f"Function 23 has {len(func23.x_values)} points")
        """
        try:
            df = pd.read_csv(file_path)
            
            # Validate required x column
            if 'x' not in df.columns:
                raise DataProcessingError("No 'x' column found in ideal functions file", "ideal_data")
            
            x_values = df['x'].values
            ideal_functions = {}
            
            # Load available ideal functions (up to 50)
            for i in range(1, 51):
                y_col = f'y{i}'
                if y_col in df.columns:
                    y_values = df[y_col].values
                    ideal_functions[i] = IdealFunction(x_values, y_values, i)
            
            # Store loaded data and report success
            self.ideal_data = ideal_functions
            print(f"Successfully loaded {len(ideal_functions)} ideal functions")
            return ideal_functions
            
        except Exception as e:
            raise DataProcessingError(f"Error reading ideal data: {str(e)}", "ideal_data")

    def read_test_data(self, file_path: str) -> pd.DataFrame:
        """
        Read test data from CSV file and return as pandas DataFrame.
        
        This method loads test data that will be used for assignment to ideal
        functions. Unlike training and ideal data, test data is returned as a
        DataFrame since it doesn't need to be converted to function objects.
        
        Args:
            file_path (str): Path to the CSV file containing test data
        
        Returns:
            pd.DataFrame: DataFrame containing test data with 'x' and 'y' columns
        
        Raises:
            DataProcessingError: If there are issues reading the file or if
                               required columns are missing
            FileNotFoundError: If the specified file doesn't exist
        
        Expected File Format:
            CSV file with columns: 'x', 'y'
            - 'x': X-coordinates of test points
            - 'y': Y-coordinates of test points
        
        Side Effects:
            - Updates self.test_data with loaded DataFrame
            - Prints success message with count of loaded points
        
        Example:
            >>> reader = DataReader()
            >>> test_df = reader.read_test_data("data/test.csv")
            Successfully loaded 100 test data points
            >>> 
            >>> # Access the test data
            >>> print(f"First test point: ({test_df.iloc[0]['x']}, {test_df.iloc[0]['y']})")
            >>> print(f"Test data shape: {test_df.shape}")
        """
        try:
            df = pd.read_csv(file_path)
            
            # Validate required columns
            if 'x' not in df.columns or 'y' not in df.columns:
                raise DataProcessingError("Invalid column names in test data file", "test_data")
            
            # Store loaded data and report success
            self.test_data = df
            print(f"Successfully loaded {len(df)} test data points")
            return df
            
        except Exception as e:
            raise DataProcessingError(f"Error reading test data: {str(e)}", "test_data")
