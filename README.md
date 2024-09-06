# UnderWaterExplosion

## Overview
UnderWaterExplosion is a project designed to analyze underwater explosions using sensor data and data management tools. This repository includes preprocessing scripts, data processing workflows, and visualization components to aid in the analysis.

## Contents
- `.idea/` - Project configuration files.
- `.vscode/` - VS Code workspace settings.
- `UnderWaterExplosion/` - Main application directory.
- `data_management/` - Scripts and tools for managing data.
- `data_processing/` - Modules for data processing.
- `user_management/` - User management functionalities.
- `vfrontend/` - Frontend components for visualizing results.
- `visualization/` - Visualization tools and scripts.
- `workflow_management/` - Scripts for managing different workflows.
- `2024_experiment_1_preprocess_data.csv` - Preprocessed data for Experiment 1.
- `2024_experiment_1_sensor_data.csv` - Raw sensor data for Experiment 1.
- `2024_features_features.csv` - Extracted features from data.
- `db.sqlite3` - SQLite database file.
- `manage.py` - Django management script.
- `test2.html` - HTML file for testing purposes.
- `tset.html` - Additional HTML test file.

## Prerequisites
- Python 3.x
- Django
- Other dependencies as listed in `requirements.txt` (if available).

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Demo-0416/UnderWaterExplosion.git
    ```
2. Navigate to the project directory:
    ```bash
    cd UnderWaterExplosion
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up the database:
    ```bash
    python manage.py migrate
    ```
5. Run the server:
    ```bash
    python manage.py runserver
    ```

## Usage
- **Data Management:** Manage and preprocess data using scripts located in the `data_management` directory.
- **Data Processing:** Use the modules in `data_processing` for analyzing the data.
- **Visualization:** Visualize the results using the tools in the `visualization` directory.

## Project Structure

```plaintext
UnderWaterExplosion/
├── .idea/                      # IDE configuration files
├── .vscode/                    # VS Code workspace settings
├── UnderWaterExplosion/        # Main application directory
├── data_management/            # Data management scripts
├── data_processing/            # Data processing scripts
├── user_management/            # User management components
├── vfrontend/                  # Frontend components
├── visualization/              # Visualization tools
├── workflow_management/        # Workflow management scripts
├── 2024_experiment_1_preprocess_data.csv  # Preprocessed data
├── 2024_experiment_1_sensor_data.csv      # Raw sensor data
├── 2024_features_features.csv             # Feature data
├── db.sqlite3                  # SQLite database
├── manage.py                   # Django management script
├── test2.html                  # HTML test file
├── tset.html                   # Additional HTML test file
