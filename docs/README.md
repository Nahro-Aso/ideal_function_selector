# Ideal Function Selector

A Python application for selecting ideal functions that best match training datasets and assigning test data points to these functions using mathematical optimization techniques.

## 🏗️ Project Structure

```
ideal_function_selector/
├── src/                          # Source code (Python package)
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Main entry point
│   ├── ideal_function_selector.py  # Main orchestrator class
│   ├── data_loader.py           # Data loading and validation
│   ├── database_handler.py      # Database models and operations
│   ├── function_matcher.py      # Core matching algorithm
│   ├── visualizer.py           # Bokeh-based visualizations
│   ├── matplotlib_viz.py       # Matplotlib visualizations
│   └── exceptions.py           # Custom exception classes
├── data/                        # Input data files
│   ├── train.csv               # Training datasets (4 functions)
│   ├── ideal.csv               # Ideal functions (50 functions)
│   └── test.csv                # Test data points
├── output/                      # Generated files (auto-created)
│   ├── ideal_functions.db      # SQLite database
│   ├── *.html                  # Interactive visualizations
│   └── *.png                   # Static plots
├── tests/                       # Test suite
│   └── test_suite.py           # Unit tests
├── scripts/                     # Utility scripts
│   └── run_project.sh          # Bash runner script
├── docs/                        # Documentation
│   └── README.md               # This file
├── requirements.txt             # Python dependencies
└── .gitignore                  # Git ignore rules
```

## 🎯 Features

- **Least Squares Matching**: Finds optimal ideal functions for training datasets
- **Test Data Assignment**: Assigns test points using sqrt(2) \* max_deviation threshold
- **Database Storage**: SQLite database for data persistence
- **Interactive Visualizations**: Bokeh-based web visualizations
- **Static Plots**: Matplotlib-based publication-ready figures
- **Comprehensive Logging**: Detailed progress and error reporting
- **Object-Oriented Design**: Clean, maintainable architecture

## 🔧 Algorithm Overview

1. **Load Data**: Read training, ideal, and test datasets from CSV files
2. **Function Matching**: For each training dataset:
   - Calculate least squares deviation against all 50 ideal functions
   - Select the ideal function with minimum deviation
3. **Test Assignment**: For each test point:
   - Calculate deviation to each selected ideal function
   - Assign to function if deviation ≤ sqrt(2) \* max_training_deviation
4. **Storage & Visualization**: Save results to database and generate plots

## 📋 Requirements

- **Python**: 3.7+
- **Core Libraries**: pandas, numpy, matplotlib, SQLAlchemy
- **Optional**: bokeh (for interactive visualizations)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ideal_function_selector
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 📊 Usage

### Quick Start

```bash
# Run the complete analysis (recommended)
python3 -m src.main

# Or use the bash script (Linux/macOS)
./scripts/run_project.sh

# Alternative: Run with PYTHONPATH
PYTHONPATH=. python3 src/main.py
```

### Manual Usage

```python
# When using as a module
from src.ideal_function_selector import IdealFunctionSelector

# Or when src is in PYTHONPATH
# from ideal_function_selector import IdealFunctionSelector

# Initialize selector
selector = IdealFunctionSelector("output/my_analysis.db")

# Run analysis
selector.run_complete_analysis(
    training_file="data/train.csv",
    ideal_file="data/ideal.csv",
    test_file="data/test.csv"
)
```

### Data Format Requirements

#### Training Data (`data/train.csv`)

```csv
x,y1,y2,y3,y4
-20,-12.96,5.36,5.36,-8.96
-19.8,-12.27,5.89,5.89,-8.27
...
```

#### Ideal Functions (`data/ideal.csv`)

```csv
x,y1,y2,y3,...,y50
-20,24.0,6.0,1.0,...,15.0
-19.8,25.2,6.1,1.1,...,15.1
...
```

#### Test Data (`data/test.csv`)

```csv
x,y
-19.52,10.63
8.65,-14.61
...
```

## 📈 Output Files

After running the analysis, check the `output/` directory for:

- **`ideal_functions.db`**: SQLite database with all results
- **`results_visualization.html`**: Interactive function plot
- **`deviation_analysis.html`**: Deviation analysis visualization
- **`matplotlib_visualization.png`**: Static publication-ready plot

## 🧪 Testing

Run the test suite:

```bash
# Using pytest (recommended)
python3 -m pytest tests/ -v

# Using unittest directly
PYTHONPATH=. python3 tests/test_suite.py

# Run specific test class
python3 -m pytest tests/test_suite.py::TestIdealFunctionSelector -v
```

## 🏛️ Architecture

### Design Patterns

- **Template Method**: BaseFunction with concrete implementations
- **Strategy Pattern**: Different deviation calculation strategies
- **Orchestrator Pattern**: IdealFunctionSelector coordinates components

### Key Classes

- **`BaseFunction`**: Abstract base for all function types
- **`TrainingFunction`**: Implements least squares deviation calculation
- **`IdealFunction`**: Handles test point validation logic
- **`ModelTrainer`**: Core algorithm implementation
- **`DatabaseManager`**: SQLAlchemy-based data persistence

### SOLID Principles

- **Single Responsibility**: Each class has focused purpose
- **Open/Closed**: Extensible through inheritance
- **Liskov Substitution**: Proper inheritance hierarchy
- **Interface Segregation**: Focused interfaces
- **Dependency Inversion**: Depends on abstractions

## 🐛 Troubleshooting

### Common Issues

**"Can't open file 'main.py'" Error**

```bash
# ❌ Wrong: python3 main.py (main.py is now in src/)
# ✅ Correct: Use module syntax
python3 -m src.main
```

**Import Errors**

```bash
# For direct script execution, set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:."

# Or use the module syntax (recommended)
python3 -m src.main
```

**Test Import Errors**

```bash
# Use pytest (handles imports automatically)
python3 -m pytest tests/ -v

# Or set PYTHONPATH for direct execution
PYTHONPATH=. python3 tests/test_suite.py
```

**Missing Data Files**

```bash
# Verify data files exist
ls data/
# Should show: ideal.csv  test.csv  train.csv
```

## 📝 Migration Notes

### Why the Running Method Changed

**Previous Structure (Deprecated):**

```
ideal_function_selector/
├── main.py              # Was in root directory
├── data_loader.py       # All files in root
├── ...
```

**Command:** `python3 main.py` ✅ (worked before)

**New Structure (Current):**

```
ideal_function_selector/
├── src/                 # Organized package structure
│   ├── main.py         # Now in src/ package
│   ├── data_loader.py  # All modules in src/
│   └── ...
```

**Command:** `python3 -m src.main` ✅ (works now)

### Benefits of New Structure

- ✅ **Professional**: Industry-standard Python package layout
- ✅ **Maintainable**: Clear separation of source, tests, data, docs
- ✅ **Installable**: Can be installed as a pip package
- ✅ **Scalable**: Easy to add new modules and organize features
- ✅ **Testable**: Proper package structure for comprehensive testing

### Quick Reference

| Task                | Command                       |
| ------------------- | ----------------------------- |
| **Run Application** | `python3 -m src.main`         |
| **Run Tests**       | `python3 -m pytest tests/ -v` |
| **Use Bash Script** | `./scripts/run_project.sh`    |
| **Install Package** | `pip install -e .`            |

**Permission Errors (run_project.sh)**

```bash
# Make script executable
chmod +x scripts/run_project.sh
```

**Database Locked**

```bash
# Remove existing database if corrupted
rm output/ideal_functions.db
```

## 📚 Mathematical Background

### Least Squares Method

For training function `f_train` and ideal function `f_ideal`:

```
deviation = Σ(f_train(x_i) - f_ideal(x_i))²
```

### Test Point Assignment Criterion

A test point `(x, y)` is assigned to ideal function `f` if:

```
|y - f(x)| ≤ √2 × max_training_deviation
```

Where `max_training_deviation` is the maximum point-wise deviation observed during training.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run tests: `python -m pytest tests/`
5. Format code: `black src/ tests/`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♀️ Support

For questions or issues:

1. Check the troubleshooting section above
2. Review the code documentation and docstrings
3. Create an issue in the repository
4. Ensure you're using the correct Python version (3.7+)

---

**Project Status**: ✅ Production Ready

**Last Updated**: June 2024
