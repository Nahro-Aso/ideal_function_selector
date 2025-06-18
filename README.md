# Ideal Function Selector

A Python application that implements an intelligent algorithm to select optimal ideal functions from a set of candidates based on training data, and then maps test data points to these selected functions using statistical criteria.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Algorithm Details](#algorithm-details)
- [Data Format](#data-format)
- [Visualization](#visualization)
- [Testing](#testing)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project solves the mathematical problem of selecting the "best" ideal functions from a large set of candidates (50 ideal functions) to match given training datasets (4 training functions). The selection is based on minimizing the sum of squared deviations between training and ideal functions. Once the best ideal functions are selected, the system maps test data points to these functions using a statistical criterion.

### Key Mathematical Concepts

- **Least Squares Method**: Used to find the ideal function that best fits each training dataset
- **Deviation Analysis**: Calculates squared differences between function values
- **Statistical Mapping**: Uses √2 × max_deviation as threshold for test point assignment
- **Interpolation**: Linear interpolation for calculating function values at arbitrary points

## ✨ Features

- **Object-Oriented Design**: Clean, modular architecture with inheritance and polymorphism
- **Robust Data Processing**: Handles CSV data with comprehensive validation
- **Interactive Visualizations**: Creates rich visualizations using Bokeh
- **Database Integration**: SQLite database for persistent data storage
- **Comprehensive Testing**: Unit tests covering all major components
- **Error Handling**: Custom exception classes for different error types
- **Statistical Analysis**: Detailed deviation analysis and summary statistics

## 📁 Project Structure

```
ideal_function_selector/
├── main.py                 # Main application orchestrator
├── data_loader.py          # Data loading and function classes
├── function_matcher.py     # Core algorithm for function matching
├── database_handler.py     # Database models and operations
├── visualizer.py          # Bokeh-based visualization
├── matplotlib_viz.py      # Alternative matplotlib visualizations
├── exceptions.py          # Custom exception classes
├── test_suite.py          # Comprehensive unit tests
├── train.csv             # Training data (4 functions)
├── ideal.csv             # Ideal functions (50 functions)
├── test.csv              # Test data points
└── README.md             # This file
```

### Core Components

#### 1. Data Loading (`data_loader.py`)

- **BaseFunction**: Abstract base class for all functions
- **TrainingFunction**: Handles training dataset with deviation calculations
- **IdealFunction**: Manages ideal functions with test point validation
- **DataReader**: CSV file processing with error handling

#### 2. Function Matching (`function_matcher.py`)

- **ModelTrainer**: Implements the core algorithm
  - Finds best ideal functions using least squares
  - Assigns test data points using statistical criteria
  - Tracks deviations and generates summaries

#### 3. Database Management (`database_handler.py`)

- **SQLAlchemy Models**:
  - `TrainingData`: Stores 4 training functions
  - `IdealFunctions`: Stores all 50 ideal functions
  - `TestDataMappings`: Stores test point assignments
- **DatabaseManager**: Handles database operations and connections

#### 4. Visualization (`visualizer.py`)

- Interactive plots with Bokeh
- Training data scatter plots
- Ideal function curves
- Test point assignments with color coding
- Deviation analysis charts

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Dependencies

```bash
pip install numpy pandas sqlalchemy bokeh matplotlib
```

### Setup

1. Clone the repository:

```bash
git clone https://github.com/Nahro-Aso/ideal_function_selector.git
cd ideal_function_selector
```

2. Install dependencies:

```bash
pip install -r requirements.txt  # If requirements.txt exists
# Or install manually:
pip install numpy pandas sqlalchemy bokeh matplotlib
```

3. Ensure CSV files are present:
   - `train.csv`: Training data with columns [x, y1, y2, y3, y4]
   - `ideal.csv`: Ideal functions with columns [x, y1, y2, ..., y50]
   - `test.csv`: Test data with columns [x, y]

## 🎮 Usage

### Basic Usage

Run the complete analysis:

```bash
python main.py
```

This will:

1. Load all CSV data files
2. Create and populate SQLite database
3. Find optimal ideal functions for each training dataset
4. Assign test data points to selected ideal functions
5. Generate interactive visualizations
6. Print comprehensive results summary

### Programmatic Usage

```python
from main import IdealFunctionSelector

# Initialize the selector
selector = IdealFunctionSelector("my_database.db")

# Run complete analysis
selector.run_complete_analysis(
    training_file="train.csv",
    ideal_file="ideal.csv",
    test_file="test.csv"
)

# Access results
best_matches = selector.best_matches
test_assignments = selector.test_assignments
```

### Custom Analysis

```python
from data_loader import DataReader
from function_matcher import ModelTrainer

# Load data
reader = DataReader()
training_functions = reader.read_training_data("train.csv")
ideal_functions = reader.read_ideal_data("ideal.csv")

# Find best matches
trainer = ModelTrainer()
best_matches = trainer.find_best_ideal_functions(training_functions, ideal_functions)

print(f"Best matches: {best_matches}")
```

## 🧮 Algorithm Details

### 1. Ideal Function Selection

For each training dataset, the algorithm:

1. **Calculates deviations** against all 50 ideal functions using:

   ```
   deviation = Σ(y_training - y_ideal)²
   ```

2. **Selects the ideal function** with minimum total squared deviation

3. **Tracks maximum point deviation** for later test point validation

### 2. Test Data Assignment

For each test data point:

1. **Calculates deviation** from each selected ideal function
2. **Applies statistical criterion**:
   ```
   threshold = √2 × max_training_deviation
   ```
3. **Assigns point** if deviation ≤ threshold
4. **Chooses best match** if multiple functions qualify

### 3. Mathematical Foundation

The algorithm is based on the **principle of least squares**:

- Minimizes the sum of squared residuals
- Provides optimal linear unbiased estimates
- Handles outliers through the √2 factor in test assignment

## 📊 Data Format

### Training Data (`train.csv`)

```csv
x,y1,y2,y3,y4
-20,-12.5,-14.2,-13.8,-15.1
-19.8,-11.8,-13.9,-13.5,-14.8
...
```

### Ideal Functions (`ideal.csv`)

```csv
x,y1,y2,y3,...,y50
-20,0.5,1.2,0.8,...,2.1
-19.8,0.6,1.3,0.9,...,2.2
...
```

### Test Data (`test.csv`)

```csv
x,y
17.5,34.16104
0.3,1.2151024
...
```

## 📈 Visualization

The system generates two main visualization files:

### 1. Results Visualization (`results_visualization.html`)

- **Training Data**: Scatter plots in different colors
- **Ideal Functions**: Smooth curves for selected functions
- **Test Points**:
  - Green squares: Successfully assigned
  - Red triangles: Unassigned points
- **Interactive Features**: Hover tooltips, legend toggling

### 2. Deviation Analysis (`deviation_analysis.html`)

- **Training Deviations**: Bar chart showing total deviations
- **Test Point Deviations**: Scatter plot of assignment deviations
- **Statistical Insights**: Visual representation of algorithm performance

## 🧪 Testing

Run the comprehensive test suite:

```bash
python -m unittest test_suite.py -v
```

### Test Coverage

- **Unit Tests**: All core classes and methods
- **Integration Tests**: Complete workflow testing
- **Data Validation**: Input validation and error handling
- **Database Operations**: SQLAlchemy model testing
- **Edge Cases**: Boundary conditions and error scenarios

### Test Categories

1. **BaseFunction Tests**: Validation, interpolation
2. **TrainingFunction Tests**: Deviation calculation
3. **IdealFunction Tests**: Test point validation
4. **DataReader Tests**: CSV file processing
5. **ModelTrainer Tests**: Algorithm correctness
6. **Database Tests**: CRUD operations
7. **Integration Tests**: End-to-end workflows

## 🗄️ Database Schema

### Training Data Table

```sql
CREATE TABLE training_data (
    id INTEGER PRIMARY KEY,
    x FLOAT NOT NULL,
    y1 FLOAT NOT NULL,
    y2 FLOAT NOT NULL,
    y3 FLOAT NOT NULL,
    y4 FLOAT NOT NULL
);
```

### Ideal Functions Table

```sql
CREATE TABLE ideal_functions (
    id INTEGER PRIMARY KEY,
    x FLOAT NOT NULL,
    y1 FLOAT NOT NULL,
    y2 FLOAT NOT NULL,
    ...,
    y50 FLOAT NOT NULL
);
```

### Test Data Mappings Table

```sql
CREATE TABLE test_data_mappings (
    id INTEGER PRIMARY KEY,
    x FLOAT NOT NULL,
    y FLOAT NOT NULL,
    assigned_ideal_function INTEGER,
    deviation FLOAT
);
```

## 🎯 Use Cases

- **Mathematical Modeling**: Function approximation and curve fitting
- **Data Science**: Feature selection and model validation
- **Engineering**: Signal processing and system identification
- **Research**: Algorithm development and statistical analysis
- **Education**: Demonstrating mathematical concepts and OOP principles

## 🔧 Configuration

The application supports several configuration options:

- **Database Path**: Custom SQLite database location
- **Visualization Output**: Custom HTML file names
- **Statistical Threshold**: Modify the √2 factor for test assignment
- **Interpolation Method**: Linear interpolation (extensible to other methods)

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add unit tests for new features
- Update documentation for API changes
- Use type hints for better code clarity

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [Repository](https://github.com/Nahro-Aso/ideal_function_selector)
- [Issues](https://github.com/Nahro-Aso/ideal_function_selector/issues)
- [Documentation](https://github.com/Nahro-Aso/ideal_function_selector/wiki)

## 📞 Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.

---

**Built with ❤️ using Python, SQLAlchemy, and Bokeh**
