"""
Database models and setup for the ideal function selection system.

This module defines the SQLAlchemy database models and provides database management
functionality for the ideal function selection system. It handles the storage and
retrieval of training data, ideal functions, and test data assignments using SQLite.

Database Schema:
    The database consists of three main tables:
    
    1. training_data: Stores the training datasets (4 functions with x, y1-y4 columns)
    2. ideal_functions: Stores all 50 ideal functions (x, y1-y50 columns)  
    3. test_data_mappings: Stores test point assignments and deviations
    
Database Design Rationale:
    - Wide table format chosen for efficient querying of function data
    - SQLite used for simplicity and portability
    - Foreign key relationships avoided to maintain flexibility
    - Nullable fields in test_data_mappings handle unassigned points

Classes:
    TrainingData: SQLAlchemy model for training datasets
    IdealFunctions: SQLAlchemy model for ideal functions (50 functions)
    TestDataMappings: SQLAlchemy model for test data assignments
    DatabaseManager: Main class for database operations and session management

Example:
    Basic database usage:
    
    >>> db_manager = DatabaseManager("my_analysis.db")
    >>> db_manager.create_database()
    >>> 
    >>> session = db_manager.get_session()
    >>> # Perform database operations...
    >>> session.close()
    >>> db_manager.close()
"""

from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional, Any
from .exceptions import DatabaseError

# Base class for all SQLAlchemy models
Base = declarative_base()

class TrainingData(Base):
    """
    SQLAlchemy model representing training datasets in the database.
    
    This table stores the four training datasets in a wide format where each row
    represents a single x-coordinate with corresponding y-values for all four
    training functions. This design allows efficient querying and comparison
    across training datasets.
    
    Table Structure:
        - id: Primary key (auto-increment)
        - x: X-coordinate (shared across all training datasets)
        - y1: Y-value for training dataset 1
        - y2: Y-value for training dataset 2  
        - y3: Y-value for training dataset 3
        - y4: Y-value for training dataset 4
    
    Attributes:
        id (int): Primary key identifier
        x (float): X-coordinate value
        y1 (float): Y-value for first training dataset
        y2 (float): Y-value for second training dataset
        y3 (float): Y-value for third training dataset
        y4 (float): Y-value for fourth training dataset
    
    Example:
        >>> # Query training data for a specific x value
        >>> record = session.query(TrainingData).filter_by(x=1.0).first()
        >>> print(f"At x={record.x}: y1={record.y1}, y2={record.y2}")
        
        >>> # Create new training data record
        >>> new_record = TrainingData(x=5.5, y1=10.2, y2=8.7, y3=12.1, y4=9.3)
        >>> session.add(new_record)
        >>> session.commit()
    """
    __tablename__ = 'training_data'
    
    id = Column(Integer, primary_key=True, doc="Primary key identifier")
    x = Column(Float, nullable=False, doc="X-coordinate value")
    y1 = Column(Float, nullable=False, doc="Y-value for training dataset 1")
    y2 = Column(Float, nullable=False, doc="Y-value for training dataset 2")
    y3 = Column(Float, nullable=False, doc="Y-value for training dataset 3")
    y4 = Column(Float, nullable=False, doc="Y-value for training dataset 4")
    
    def __repr__(self) -> str:
        """
        Return string representation of TrainingData record.
        
        Returns:
            str: Formatted string showing all y-values for the x-coordinate
        """
        return f"<TrainingData(x={self.x}, y1={self.y1}, y2={self.y2}, y3={self.y3}, y4={self.y4})>"

class IdealFunctions(Base):
    """
    SQLAlchemy model representing all 50 ideal functions in the database.
    
    This table stores all ideal functions in a wide format where each row represents
    a single x-coordinate with corresponding y-values for all 50 ideal functions.
    This design enables efficient comparison operations during the function selection
    process.
    
    Table Structure:
        - id: Primary key (auto-increment)
        - x: X-coordinate (shared across all ideal functions)
        - y1-y50: Y-values for ideal functions 1 through 50
    
    Design Considerations:
        - Wide table format chosen for performance during function matching
        - All y-columns are non-nullable to ensure data completeness
        - Single table approach avoids complex joins during analysis
    
    Attributes:
        id (int): Primary key identifier
        x (float): X-coordinate value
        y1-y50 (float): Y-values for ideal functions 1 through 50
    
    Example:
        >>> # Query ideal functions for a specific x value  
        >>> record = session.query(IdealFunctions).filter_by(x=2.0).first()
        >>> print(f"Ideal function 1 at x=2.0: y={record.y1}")
        >>> print(f"Ideal function 25 at x=2.0: y={record.y25}")
        
        >>> # Create new ideal functions record
        >>> new_record = IdealFunctions(x=3.14, y1=1.0, y2=2.0, ..., y50=50.0)
        >>> session.add(new_record)
    """
    __tablename__ = 'ideal_functions'
    
    id = Column(Integer, primary_key=True, doc="Primary key identifier")
    x = Column(Float, nullable=False, doc="X-coordinate value")
    
    # Y-values for all 50 ideal functions
    # Using individual columns for efficient querying and indexing
    y1 = Column(Float, nullable=False, doc="Y-value for ideal function 1")
    y2 = Column(Float, nullable=False, doc="Y-value for ideal function 2")
    y3 = Column(Float, nullable=False, doc="Y-value for ideal function 3")
    y4 = Column(Float, nullable=False, doc="Y-value for ideal function 4")
    y5 = Column(Float, nullable=False, doc="Y-value for ideal function 5")
    y6 = Column(Float, nullable=False, doc="Y-value for ideal function 6")
    y7 = Column(Float, nullable=False, doc="Y-value for ideal function 7")
    y8 = Column(Float, nullable=False, doc="Y-value for ideal function 8")
    y9 = Column(Float, nullable=False, doc="Y-value for ideal function 9")
    y10 = Column(Float, nullable=False, doc="Y-value for ideal function 10")
    y11 = Column(Float, nullable=False, doc="Y-value for ideal function 11")
    y12 = Column(Float, nullable=False, doc="Y-value for ideal function 12")
    y13 = Column(Float, nullable=False, doc="Y-value for ideal function 13")
    y14 = Column(Float, nullable=False, doc="Y-value for ideal function 14")
    y15 = Column(Float, nullable=False, doc="Y-value for ideal function 15")
    y16 = Column(Float, nullable=False, doc="Y-value for ideal function 16")
    y17 = Column(Float, nullable=False, doc="Y-value for ideal function 17")
    y18 = Column(Float, nullable=False, doc="Y-value for ideal function 18")
    y19 = Column(Float, nullable=False, doc="Y-value for ideal function 19")
    y20 = Column(Float, nullable=False, doc="Y-value for ideal function 20")
    y21 = Column(Float, nullable=False, doc="Y-value for ideal function 21")
    y22 = Column(Float, nullable=False, doc="Y-value for ideal function 22")
    y23 = Column(Float, nullable=False, doc="Y-value for ideal function 23")
    y24 = Column(Float, nullable=False, doc="Y-value for ideal function 24")
    y25 = Column(Float, nullable=False, doc="Y-value for ideal function 25")
    y26 = Column(Float, nullable=False, doc="Y-value for ideal function 26")
    y27 = Column(Float, nullable=False, doc="Y-value for ideal function 27")
    y28 = Column(Float, nullable=False, doc="Y-value for ideal function 28")
    y29 = Column(Float, nullable=False, doc="Y-value for ideal function 29")
    y30 = Column(Float, nullable=False, doc="Y-value for ideal function 30")
    y31 = Column(Float, nullable=False, doc="Y-value for ideal function 31")
    y32 = Column(Float, nullable=False, doc="Y-value for ideal function 32")
    y33 = Column(Float, nullable=False, doc="Y-value for ideal function 33")
    y34 = Column(Float, nullable=False, doc="Y-value for ideal function 34")
    y35 = Column(Float, nullable=False, doc="Y-value for ideal function 35")
    y36 = Column(Float, nullable=False, doc="Y-value for ideal function 36")
    y37 = Column(Float, nullable=False, doc="Y-value for ideal function 37")
    y38 = Column(Float, nullable=False, doc="Y-value for ideal function 38")
    y39 = Column(Float, nullable=False, doc="Y-value for ideal function 39")
    y40 = Column(Float, nullable=False, doc="Y-value for ideal function 40")
    y41 = Column(Float, nullable=False, doc="Y-value for ideal function 41")
    y42 = Column(Float, nullable=False, doc="Y-value for ideal function 42")
    y43 = Column(Float, nullable=False, doc="Y-value for ideal function 43")
    y44 = Column(Float, nullable=False, doc="Y-value for ideal function 44")
    y45 = Column(Float, nullable=False, doc="Y-value for ideal function 45")
    y46 = Column(Float, nullable=False, doc="Y-value for ideal function 46")
    y47 = Column(Float, nullable=False, doc="Y-value for ideal function 47")
    y48 = Column(Float, nullable=False, doc="Y-value for ideal function 48")
    y49 = Column(Float, nullable=False, doc="Y-value for ideal function 49")
    y50 = Column(Float, nullable=False, doc="Y-value for ideal function 50")

class TestDataMappings(Base):
    """
    SQLAlchemy model representing test data point assignments and results.
    
    This table stores the results of the test data assignment process, including
    which ideal function each test point was assigned to and the corresponding
    deviation value. Points that couldn't be assigned to any ideal function
    have NULL values for assignment and deviation.
    
    Table Structure:
        - id: Primary key (auto-increment)
        - x, y: Test point coordinates
        - assigned_ideal_function: Number of assigned ideal function (nullable)
        - deviation: Deviation value for the assignment (nullable)
    
    Assignment Logic:
        - Points are assigned if deviation <= sqrt(2) * max_training_deviation
        - Unassigned points have NULL values for function and deviation
        - Each point is assigned to the ideal function with minimum valid deviation
    
    Attributes:
        id (int): Primary key identifier
        x (float): X-coordinate of test point
        y (float): Y-coordinate of test point
        assigned_ideal_function (int, optional): Number of assigned ideal function (1-50)
        deviation (float, optional): Deviation value between test point and ideal function
    
    Example:
        >>> # Query assigned test points
        >>> assigned_points = session.query(TestDataMappings).filter(
        ...     TestDataMappings.assigned_ideal_function.isnot(None)
        ... ).all()
        >>> 
        >>> # Query unassigned test points  
        >>> unassigned_points = session.query(TestDataMappings).filter(
        ...     TestDataMappings.assigned_ideal_function.is_(None)
        ... ).all()
        >>> 
        >>> # Create new test mapping
        >>> mapping = TestDataMappings(x=1.5, y=2.3, assigned_ideal_function=23, deviation=0.05)
        >>> session.add(mapping)
    """
    __tablename__ = 'test_data_mappings'
    
    id = Column(Integer, primary_key=True, doc="Primary key identifier")
    x = Column(Float, nullable=False, doc="X-coordinate of test point")
    y = Column(Float, nullable=False, doc="Y-coordinate of test point")
    assigned_ideal_function = Column(Integer, nullable=True, 
                                   doc="Number of assigned ideal function (1-50), NULL if unassigned")
    deviation = Column(Float, nullable=True, 
                      doc="Deviation value for assignment, NULL if unassigned")
    
    def __repr__(self) -> str:
        """
        Return string representation of TestDataMapping record.
        
        Returns:
            str: Formatted string showing test point coordinates, assignment, and deviation
        """
        return (f"<TestDataMapping(x={self.x}, y={self.y}, "
                f"function={self.assigned_ideal_function}, deviation={self.deviation})>")

class DatabaseManager:
    """
    Main database management class for the ideal function selection system.
    
    This class provides a high-level interface for database operations including
    database creation, session management, and connection handling. It uses SQLite
    as the backend database and SQLAlchemy for ORM functionality.
    
    Key Features:
        - Automatic database creation with all required tables
        - Session management with proper connection handling
        - Error handling with custom exceptions
        - Resource cleanup and connection disposal
    
    Attributes:
        db_path (str): Path to the SQLite database file
        engine (sqlalchemy.Engine): SQLAlchemy database engine
        Session (sqlalchemy.orm.sessionmaker): Session factory for database operations
    
    Example:
        >>> # Basic usage
        >>> db_manager = DatabaseManager("analysis_results.db")
        >>> db_manager.create_database()
        >>> 
        >>> # Use in context manager style
        >>> session = db_manager.get_session()
        >>> try:
        ...     # Perform database operations
        ...     result = session.query(TrainingData).all()
        ...     session.commit()
        ... except Exception as e:
        ...     session.rollback()
        ...     raise
        ... finally:
        ...     session.close()
        >>> 
        >>> # Clean up
        >>> db_manager.close()
    """
    
    def __init__(self, db_path: str = "ideal_functions.db"):
        """
        Initialize the DatabaseManager with specified database path.
        
        Args:
            db_path (str, optional): Path to the SQLite database file.
                                   Defaults to "ideal_functions.db".
                                   If the file doesn't exist, it will be created
                                   when create_database() is called.
        
        Note:
            The constructor only sets up the path. The actual database connection
            is established when create_database() is called.
        """
        self.db_path = db_path
        self.engine: Optional[Any] = None
        self.Session: Optional[sessionmaker] = None
        
    def create_database(self) -> None:
        """
        Create the database and all required tables.
        
        This method establishes the database connection, creates all tables defined
        in the SQLAlchemy models, and sets up the session factory for subsequent
        database operations.
        
        Tables Created:
            - training_data: For storing training datasets
            - ideal_functions: For storing all 50 ideal functions
            - test_data_mappings: For storing test point assignments
        
        Raises:
            DatabaseError: If there are issues creating the database or tables
        
        Side Effects:
            - Creates SQLite database file if it doesn't exist
            - Initializes self.engine and self.Session
            - Prints success message to console
        
        Example:
            >>> db_manager = DatabaseManager("new_analysis.db")
            >>> db_manager.create_database()
            Database created successfully at new_analysis.db
        """
        try:
            # Create SQLAlchemy engine with SQLite database
            self.engine = create_engine(f'sqlite:///{self.db_path}')
            
            # Create all tables defined in the models
            Base.metadata.create_all(self.engine)
            
            # Set up session factory
            self.Session = sessionmaker(bind=self.engine)
            
            print(f"Database created successfully at {self.db_path}")
            
        except Exception as e:
            raise DatabaseError(f"Failed to create database: {str(e)}")
            
    def get_session(self):
        """
        Get a new database session for performing operations.
        
        Returns a new SQLAlchemy session that can be used for querying,
        inserting, updating, and deleting data. The caller is responsible
        for closing the session when finished.
        
        Returns:
            sqlalchemy.orm.Session: New database session
        
        Raises:
            DatabaseError: If the database hasn't been initialized or if
                         there are issues creating the session
        
        Example:
            >>> db_manager = DatabaseManager()
            >>> db_manager.create_database()
            >>> 
            >>> session = db_manager.get_session()
            >>> try:
            ...     # Perform database operations
            ...     records = session.query(TrainingData).all()
            ...     # ... more operations ...
            ...     session.commit()
            ... except Exception as e:
            ...     session.rollback()
            ...     raise
            ... finally:
            ...     session.close()  # Always close the session
        """
        if self.Session is None:
            raise DatabaseError("Database not initialized. Call create_database() first.")
        return self.Session()
        
    def close(self) -> None:
        """
        Close the database connection and clean up resources.
        
        This method should be called when finished with the database to ensure
        proper cleanup of connections and resources. It's particularly important
        in long-running applications to prevent connection leaks.
        
        Side Effects:
            - Disposes of the SQLAlchemy engine
            - Closes all associated connections
            - Resets engine and Session to None
        
        Example:
            >>> db_manager = DatabaseManager()
            >>> db_manager.create_database()
            >>> # ... perform database operations ...
            >>> db_manager.close()  # Clean up when finished
        """
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.Session = None
