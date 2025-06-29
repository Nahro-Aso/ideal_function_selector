"""
Setup script for the Ideal Function Selector project.
"""

from setuptools import setup, find_packages
import os

# Read the README file for the long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'docs', 'README.md')
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Ideal Function Selector - A Python application for mathematical function optimization"

# Read requirements from requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    try:
        with open(requirements_path, 'r', encoding='utf-8') as f:
            # Filter out comments and empty lines
            requirements = []
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
            return requirements
    except FileNotFoundError:
        # Fallback to core requirements
        return [
            'pandas>=1.3.0',
            'numpy>=1.21.0',
            'matplotlib>=3.4.0',
            'SQLAlchemy>=1.4.0'
        ]

setup(
    name="ideal-function-selector",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python application for selecting ideal functions using mathematical optimization",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ideal-function-selector",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "viz": [
            "bokeh>=2.4.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ideal-function-selector=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["data/*.csv"],
    },
    keywords="mathematics optimization function-fitting data-science machine-learning",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ideal-function-selector/issues",
        "Source": "https://github.com/yourusername/ideal-function-selector",
        "Documentation": "https://github.com/yourusername/ideal-function-selector/blob/main/docs/README.md",
    },
) 