"""
Main application orchestrator that coordinates the entire ideal function selection process.

This module contains the IdealFunctionSelector class which serves as the main entry point
for the ideal function selection analysis. It coordinates data loading, function matching,
database operations, and visualization generation.

Example:
    Basic usage of the IdealFunctionSelector:
    
    >>> selector = IdealFunctionSelector("my_database.db")
    >>> selector.run_complete_analysis("train.csv", "ideal.csv", "test.csv")
    
Classes:
    IdealFunctionSelector: Main orchestrator class for the analysis workflow
"""

import os
from typing import List, Dict, Any
from database_handler import DatabaseManager, TrainingData, IdealFunctions, TestDataMappings
from data_loader import DataReader
from function_matcher import ModelTrainer
from visualizer import DataVisualizer
from exceptions import DataProcessingError, DatabaseError


class IdealFunctionSelector:
    """
    Main application class that coordinates all components of the ideal function selection system.
    
    This class manages the complete workflow from data loading through analysis to visualization.
    It handles database operations, coordinates between different components, and ensures
    proper error handling throughout the process.
    
    Attributes:
        db_manager (DatabaseManager): Handles all database operations
        data_reader (DataReader): Responsible for loading data from CSV files
        model_trainer (ModelTrainer): Performs function matching and test data assignment
        visualizer (DataVisualizer): Creates visualizations and reports
        training_functions (Dict[int, TrainingFunction]): Loaded training data
        ideal_functions (Dict[int, IdealFunction]): Loaded ideal functions
        test_data (pd.DataFrame): Loaded test data
        test_assignments (List[Dict]): Results of test data assignment
        best_matches (Dict[int, int]): Mapping of training datasets to best ideal functions
        
    Example:
        >>> # Initialize the selector with a custom database path
        >>> selector = IdealFunctionSelector("analysis_results.db")
        >>> 
        >>> # Run complete analysis with your data files
        >>> selector.run_complete_analysis(
        ...     training_file="my_training_data.csv",
        ...     ideal_file="my_ideal_functions.csv", 
        ...     test_file="my_test_data.csv"
        ... )
    """
    
    def __init__(self, db_path: str = "ideal_functions.db"):
        """
        Initialize the ideal function selector with all necessary components.
        
        Args:
            db_path (str, optional): Path to the SQLite database file. 
                                   Defaults to "ideal_functions.db". If the file doesn't exist,
                                   it will be created during the analysis.
        
        Raises:
            DatabaseError: If there are issues initializing the database manager
        """
        self.db_manager = DatabaseManager(db_path)
        self.data_reader = DataReader()
        self.model_trainer = ModelTrainer()
        self.visualizer = DataVisualizer()
        
        # Data storage - initialized as empty and populated during analysis
        self.training_functions: Dict[int, Any] = {}
        self.ideal_functions: Dict[int, Any] = {}
        self.test_data = None
        self.test_assignments: List[Dict[str, Any]] = []
        self.best_matches: Dict[int, int] = {}
    
    def run_complete_analysis(self, 
                            training_file: str,
                            ideal_file: str,
                            test_file: str) -> None:
        """
        Execute the complete ideal function selection analysis workflow.
        
        This method orchestrates the entire analysis process:
        1. Database initialization
        2. Data loading from CSV files
        3. Data storage in database
        4. Finding best ideal functions for training data
        5. Assigning test data to ideal functions
        6. Storing results in database
        7. Creating visualizations
        8. Generating summary reports
        
        Args:
            training_file (str): Path to the CSV file containing training data.
                               Expected format: columns 'x', 'y1', 'y2', 'y3', 'y4'
            ideal_file (str): Path to the CSV file containing ideal functions.
                            Expected format: columns 'x', 'y1', 'y2', ..., 'y50'
            test_file (str): Path to the CSV file containing test data.
                           Expected format: columns 'x', 'y'
        
        Returns:
            None: Results are stored in database and visualization files are generated
        
        Raises:
            DataProcessingError: If there are issues with data loading or processing
            DatabaseError: If there are database-related issues
            FileNotFoundError: If any of the input files cannot be found
            
        Side Effects:
            - Creates/updates SQLite database with analysis results
            - Generates HTML visualization files
            - Prints progress and summary information to console
            
        Example:
            >>> selector = IdealFunctionSelector()
            >>> selector.run_complete_analysis(
            ...     training_file="data/train.csv",
            ...     ideal_file="data/ideal.csv",
            ...     test_file="data/test.csv"
            ... )
            Starting Ideal Function Selection Analysis...
            ==================================================
            1. Initializing database...
            2. Loading data files...
            ...
            Analysis completed successfully!
        """
        try:
            print("Starting Ideal Function Selection Analysis...")
            print("="*50)
            
            # Step 1: Initialize database
            print("1. Initializing database...")
            self.db_manager.create_database()
            
            # Step 2: Load data
            print("2. Loading data files...")
            self.training_functions = self.data_reader.read_training_data(training_file)
            self.ideal_functions = self.data_reader.read_ideal_data(ideal_file)
            self.test_data = self.data_reader.read_test_data(test_file)
            
            # Step 3: Store data in database
            print("3. Storing data in database...")
            self._store_data_in_database()
            
            # Step 4: Find best ideal functions
            print("4. Finding best ideal functions for each training dataset...")
            self.best_matches = self.model_trainer.find_best_ideal_functions(
                self.training_functions, self.ideal_functions)
            
            # Step 5: Assign test data
            print("5. Assigning test data to ideal functions...")
            selected_ideal_functions = {train_num: self.ideal_functions[ideal_num] 
                                       for train_num, ideal_num in self.best_matches.items()}
            
            self.test_assignments = self.model_trainer.assign_test_data(
                self.test_data, selected_ideal_functions)
            
            # Step 6: Store test assignments in database
            print("6. Storing test assignments in database...")
            self._store_test_assignments()
            
            # Step 7: Create visualizations
            print("7. Creating visualizations...")
            self.visualizer.create_comprehensive_plot(
                self.training_functions, selected_ideal_functions, self.test_assignments)
            
            self.visualizer.create_deviation_analysis_plot(
                self.model_trainer.training_deviations, self.test_assignments)
            
            # Step 8: Generate and display summary
            print("8. Generating results summary...")
            training_summary = self.model_trainer.get_training_summary()
            stats = self.visualizer.create_summary_statistics(training_summary, self.test_assignments)
            self.visualizer.print_results_summary(stats)
            
            print("\nAnalysis completed successfully!")
            print("Check the generated HTML files for visualizations.")
            
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            raise
        finally:
            # Ensure database connection is properly closed
            self.db_manager.close()
    
    def _store_data_in_database(self) -> None:
        """
        Store all loaded training and ideal function data in the database.
        
        This private method handles the database storage of training data and ideal functions.
        It creates appropriate database records and handles the complex mapping of multiple
        training datasets and ideal functions into the database schema.
        
        Database Operations:
            - Creates TrainingData records with x values and y1-y4 columns
            - Creates IdealFunctions records with x values and y1-y50 columns
            - Handles transaction management with proper rollback on errors
        
        Raises:
            DatabaseError: If there are issues storing data in the database
            
        Note:
            This method should only be called after successfully loading data
            with the data_reader component.
        """
        session = self.db_manager.get_session()
        
        try:
            # Store training data - combine all training datasets into single records
            for train_num, train_func in self.training_functions.items():
                for x, y in zip(train_func.x_values, train_func.y_values):
                    # Create a record with all training datasets
                    existing_record = session.query(TrainingData).filter_by(x=x).first()
                    
                    if existing_record is None:
                        record = TrainingData(x=x, y1=0, y2=0, y3=0, y4=0)
                        session.add(record)
                        session.flush()
                        existing_record = record
                    
                    # Set the appropriate y value for this training dataset
                    setattr(existing_record, f'y{train_num}', y)
            
            session.commit()
            
            # Store ideal functions - all 50 functions in single records per x value
            if self.ideal_functions:
                first_ideal = list(self.ideal_functions.values())[0]
                for i, x in enumerate(first_ideal.x_values):
                    y_values = {}
                    for ideal_num in range(1, 51):
                        if ideal_num in self.ideal_functions:
                            y_values[f'y{ideal_num}'] = self.ideal_functions[ideal_num].y_values[i]
                        else:
                            y_values[f'y{ideal_num}'] = 0
                    
                    record = IdealFunctions(x=x, **y_values)
                    session.add(record)
            
            session.commit()
            print("Data successfully stored in database")
            
        except Exception as e:
            session.rollback()
            raise DatabaseError(f"Error storing data in database: {str(e)}")
        finally:
            session.close()
    
    def _store_test_assignments(self) -> None:
        """
        Store test data assignment results in the database.
        
        This private method saves the results of test data assignment to ideal functions
        in the TestDataMappings table. Each test point is stored with its assignment
        information including which ideal function it was assigned to and the deviation.
        
        Database Operations:
            - Creates TestDataMappings records for each test point
            - Stores x, y coordinates, assigned ideal function, and deviation
            - Handles unassigned points (NULL values for assignment and deviation)
        
        Raises:
            DatabaseError: If there are issues storing test assignments in the database
            
        Note:
            This method should only be called after test data assignment is complete.
        """
        session = self.db_manager.get_session()
        
        try:
            for assignment in self.test_assignments:
                record = TestDataMappings(
                    x=assignment['x'],
                    y=assignment['y'],
                    assigned_ideal_function=assignment['assigned_ideal_function'],
                    deviation=assignment['deviation']
                )
                session.add(record)
            
            session.commit()
            print("Test assignments successfully stored in database")
            
        except Exception as e:
            session.rollback()
            raise DatabaseError(f"Error storing test assignments: {str(e)}")
        finally:
            session.close() 