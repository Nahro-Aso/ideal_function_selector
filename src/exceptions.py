"""
Custom exceptions for the ideal function selection system.

This module defines specialized exception classes used throughout the ideal function
selection system to provide more specific error handling and better debugging information.
These exceptions inherit from Python's built-in Exception class and add domain-specific
context to error conditions.

Exception Hierarchy:
    Exception (built-in)
    ├── DataProcessingError: Issues with data processing or validation
    ├── DatabaseError: Database-related issues  
    └── ValidationError: Data validation failures

Example:
    Catching specific exceptions:
    
    >>> try:
    ...     data_reader.read_training_data("invalid_file.csv")
    ... except DataProcessingError as e:
    ...     print(f"Data processing failed: {e}")
    ... except DatabaseError as e:
    ...     print(f"Database issue: {e}")
"""


class DataProcessingError(Exception):
    """
    Raised when there are issues with data processing or validation.
    
    This exception is used when problems occur during data loading, processing,
    or mathematical operations on the data. It provides additional context
    about the type of data that caused the error.
    
    Attributes:
        data_type (str, optional): Type of data that caused the error.
                                 (e.g., 'training_data', 'ideal_data', 'test_data')
        message (str): The error message describing the issue
    
    Example:
        >>> # Raising a DataProcessingError with data type context
        >>> if len(x_values) != len(y_values):
        ...     raise DataProcessingError(
        ...         "X and Y arrays must have the same length", 
        ...         data_type="training_data"
        ...     )
        
        >>> # Catching and handling the error
        >>> try:
        ...     process_data()
        ... except DataProcessingError as e:
        ...     if e.data_type == "training_data":
        ...         print("Issue with training data:", str(e))
    """
    
    def __init__(self, message: str, data_type: str = None):
        """
        Initialize the DataProcessingError.
        
        Args:
            message (str): Error message describing the issue in detail
            data_type (str, optional): Type of data that caused the error.
                                     Common values include:
                                     - 'training_data': Issues with training dataset
                                     - 'ideal_data': Issues with ideal functions  
                                     - 'test_data': Issues with test dataset
                                     - 'model_training': Issues during model training
                                     - 'test_assignment': Issues during test data assignment
        """
        self.data_type = data_type
        super().__init__(message)
    
    def __str__(self) -> str:
        """
        Return a formatted string representation of the error.
        
        Returns:
            str: Formatted error message including data type if available
            
        Example:
            >>> error = DataProcessingError("Invalid data format", "training_data")
            >>> str(error)
            'DataProcessingError in training_data: Invalid data format'
        """
        if self.data_type:
            return f"DataProcessingError in {self.data_type}: {super().__str__()}"
        return f"DataProcessingError: {super().__str__()}"


class DatabaseError(Exception):
    """
    Raised when there are database-related issues.
    
    This exception is used for problems with database operations including:
    - Connection failures
    - Table creation issues  
    - Data insertion/update/deletion problems
    - Transaction rollback scenarios
    - SQLite-specific errors
    
    Example:
        >>> try:
        ...     db_manager.create_database()
        ... except DatabaseError as e:
        ...     print(f"Failed to initialize database: {e}")
        ...     # Implement fallback or recovery logic
        
        >>> # Common usage in database operations
        >>> try:
        ...     session.commit()
        ... except Exception as e:
        ...     session.rollback()
        ...     raise DatabaseError(f"Failed to commit transaction: {str(e)}")
    """
    pass


class ValidationError(Exception):
    """
    Raised when data validation fails.
    
    This exception is used when data doesn't meet expected criteria or constraints:
    - Array length mismatches
    - Missing required values
    - Data type inconsistencies
    - Range or boundary violations
    - Format validation failures
    
    Example:
        >>> def validate_arrays(x_values, y_values):
        ...     if len(x_values) != len(y_values):
        ...         raise ValidationError("X and Y arrays must have the same length")
        ...     if len(x_values) == 0:
        ...         raise ValidationError("Arrays cannot be empty")
        
        >>> # Usage in data validation
        >>> try:
        ...     validate_arrays(x_data, y_data)
        ... except ValidationError as e:
        ...     print(f"Data validation failed: {e}")
        ...     # Handle invalid data appropriately
    """
    pass
