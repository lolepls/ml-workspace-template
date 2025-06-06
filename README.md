# Machine Learning Workspace Guidelines

This repo is meant to be used as a template for machine learning projects. Clone this to your local machine to already have the needed folder structure and steps needed to build a ML-based application.

## Introduction - How to organize a ML Workspace

This document provides guidelines for organizing a machine learning project workspace. Following a consistent structure helps maintain clean code, improves collaboration, ensures reproducibility, and makes the project more maintainable as it grows. This structure is suitable for both small and large ML projects and strikes a balance between simplicity and scalability.

## Directory Structure Overview

```
ProjectName/
│
├── dashboard/                  # Interactive visualization application
│   ├── dashboard.py            # Main application entry point
│   └── utils/                  # Dashboard-specific utilities
│       └── data_loader.py      # Data loading functions
│
├── data/                       # Original, immutable raw data
│   ├── Dataset1/               # First dataset category
│   └── Dataset2/               # Second dataset category
│
├── notebooks/                  # Jupyter notebooks for analysis and exploration
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_development.ipynb
│   └── 04_model_evaluation.ipynb
│
├── processed_data/             # Processed versions of the raw data
│   ├── Dataset1/               # Processed first dataset
│   └── Dataset2/               # Processed second dataset
│
├── models/                     # Trained model artifacts
│   ├── saved_models/           # Serialized model files
│   └── model_metrics/          # Performance metrics and visualizations
│
├── src/                        # Source code for project modules
│   ├── __init__.py
│   ├── data/                   # Data processing code
│   │   ├── __init__.py
│   │   ├── preprocessing.py    # Data cleaning and transformation
│   │   └── features.py         # Feature extraction and engineering
│   │
│   ├── models/                 # ML modeling code
│   │   ├── __init__.py
│   │   ├── train.py            # Model training functions
│   │   └── predict.py          # Model inference functions
│   │
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       └── evaluation.py       # Model evaluation metrics
│
├── tests/                      # Unit tests
│   ├── test_preprocessing.py
│   └── test_models.py
│
├── requirements.txt            # Project dependencies
├── setup.py                    # Package installation
├── README.md                   # Project documentation
├── run.sh                      # Script to run components
└── docs/                       # Additional documentation
```

## Purpose of Each Directory

### 1. `dashboard/`

**Purpose**: Houses interactive visualization applications that allow stakeholders to explore data and model results.

- `dashboard.py`: Main entry point for the dashboard application (often built with tools like Streamlit, Dash, or Gradio)
- `utils/`: Utilities specific to the dashboard, e.g., data loading for visualization

**When to use**: When your project requires interactive visualizations or a user interface for non-technical users to interact with your data or models.

### 2. `data/`

**Purpose**: Stores the original, raw datasets that should remain immutable.

**Best practices**:
- Never modify files in this directory
- Document data sources and collection methodologies in README files
- Consider using version control for data or data versioning tools
- Organize by data types, sources, or categories

**When to use**: Always included in every ML project to maintain the original data source.

### 3. `notebooks/`

**Purpose**: Contains Jupyter notebooks used for experimentation, exploration, visualization, and communication.

**Recommended workflow**:
- `01_exploratory_data_analysis.ipynb`: Initial data exploration and insights
- `02_feature_engineering.ipynb`: Feature development and transformation
- `03_model_development.ipynb`: Model training and hyperparameter tuning
- `04_model_evaluation.ipynb`: Comprehensive model evaluation

**Best practices**:
- Number notebooks to indicate workflow order
- Keep notebooks focused on a single task
- Move reusable code to the `src/` directory
- Include markdown cells to explain your reasoning and findings

**When to use**: For exploration, visualization, and communication of results. Not for production code.

### 4. `processed_data/`

**Purpose**: Stores processed, cleaned, and transformed versions of the raw data.

**Best practices**:
- Maintain parallel structure to the `data/` directory
- Include versioning information in filenames or metadata
- Document transformations applied in README files
- Save intermediate data to avoid reprocessing

**When to use**: When data preprocessing is computationally expensive or time-consuming.

### 5. `models/`

**Purpose**: Stores trained model artifacts and evaluation metrics.

- `saved_models/`: Serialized model files (e.g., pickle, joblib, h5)
- `model_metrics/`: Performance visualizations and metrics reports

**Best practices**:
- Include metadata with models (training date, dataset version, hyperparameters)
- Use clear naming conventions for model files
- Save models in portable formats

**When to use**: For any project where models need to be persisted for later use or deployment.

### 6. `src/`

**Purpose**: Contains the reusable, production-ready source code organized into modules.

- `data/`: Code for data processing pipelines
  - `preprocessing.py`: Functions for cleaning and normalizing data
  - `features.py`: Functions for feature engineering

- `models/`: Code for ML model development
  - `train.py`: Functions for training models
  - `predict.py`: Functions for making predictions

- `utils/`: Utility functions used across the project
  - `evaluation.py`: Model evaluation metrics and reporting functions

**Best practices**:
- Write modular, reusable code
- Include documentation strings
- Follow a consistent coding style
- Create proper Python packages with `__init__.py` files

**When to use**: For all reusable code that will be imported into multiple notebooks or scripts.

### 7. `tests/`

**Purpose**: Contains unit tests and integration tests for the code in `src/`.

**Best practices**:
- Mirror the structure of the `src/` directory
- Aim for high test coverage of critical components
- Automate testing in your workflow

**When to use**: For any project that requires reliability and maintainability.

### 8. Other Files

- `requirements.txt`: Lists all Python dependencies with versions
- `setup.py`: Allows the project to be installed as a package
- `README.md`: Project documentation and instructions
- `run.sh`: Shell script to execute various project components
- `docs/`: Additional documentation

## Setting Up a New Project

### Step 1: Create the Basic Directory Structure

```bash
# Create main project directory
mkdir ProjectName && cd ProjectName

# Create basic directory structure
mkdir -p dashboard/utils data notebooks processed_data models/{saved_models,model_metrics} src/{data,models,utils} tests docs

# Create __init__.py files
touch src/__init__.py src/data/__init__.py src/models/__init__.py src/utils/__init__.py

# Create basic files
touch README.md requirements.txt setup.py run.sh
```

### Step 2: Set Up Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install initial dependencies
pip install jupyter pandas numpy matplotlib scikit-learn
pip freeze > requirements.txt
```

### Step 3: Initialize Notebooks

Create initial Jupyter notebooks with a consistent template:

```bash
# Navigate to notebooks directory
cd notebooks

# Create notebooks
jupyter notebook
```

### Step 4: Create Core Modules

Set up basic functionality in the `src/` directory:

- `src/data/preprocessing.py`: Basic data cleaning functions
- `src/data/features.py`: Initial feature engineering functions
- `src/models/train.py`: Model training framework
- `src/utils/evaluation.py`: Evaluation metrics

### Step 5: Create Dashboard (if needed)

```bash
# Install dashboard library (e.g., Streamlit)
pip install streamlit
pip freeze > requirements.txt

# Create basic dashboard
touch dashboard/dashboard.py
touch dashboard/utils/data_loader.py
```

### Step 6: Create Run Script

Create a `run.sh` script that can execute different components:

```bash
#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Parse command line arguments
ACTION=${1:-"dashboard"}  # Default action

case "$ACTION" in
    dashboard)
        echo "Starting dashboard..."
        streamlit run dashboard/dashboard.py
        ;;
    notebook)
        echo "Starting Jupyter notebook server..."
        jupyter notebook --notebook-dir=notebooks
        ;;
    # Add other actions as needed
    *)
        echo "Usage: $0 [dashboard|notebook|...]"
        exit 1
        ;;
esac
```

## Best Practices

### 1. Code Organization

- **Modularity**: Keep functions and classes focused on a single responsibility
- **Reusability**: Write code in `src/` that can be imported into notebooks
- **Consistency**: Follow a consistent coding style (e.g., PEP 8)

### 2. Data Management

- **Immutability**: Never modify raw data files
- **Versioning**: Track versions of processed datasets
- **Documentation**: Document data sources and transformations

### 3. Model Development

- **Experiment Tracking**: Log hyperparameters, metrics, and results
- **Reproducibility**: Set random seeds and document environment
- **Evaluation**: Use consistent evaluation metrics across experiments

### 4. Collaboration

- **Documentation**: Maintain clear documentation for others (and future you)
- **Version Control**: Use git with meaningful commit messages
- **Dependencies**: Keep `requirements.txt` updated

### 5. Scaling Considerations

- **Pipeline Automation**: Create pipelines for repeatable processes
- **Efficiency**: Optimize code for larger datasets when needed
- **Configuration**: Use configuration files for different environments

## Adapting the Structure

This structure can be adapted based on project needs:

- **Smaller Projects**: Simplify by removing unnecessary directories
- **Larger Projects**: Add more specialized directories (e.g., `configs/`, `api/`)
- **Specialized Projects**: Add domain-specific directories (e.g., `embeddings/`, `annotations/`)

## Conclusion

Following a consistent project structure enhances productivity, collaboration, and maintainability. This template provides a starting point that can be adapted to specific project requirements while maintaining core ML workflow principles.

Remember that the structure should serve the project's needs – don't be afraid to adjust it as the project evolves, but maintain consistency throughout development to ensure all team members can navigate the codebase effectively.
