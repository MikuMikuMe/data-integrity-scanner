Creating a comprehensive Python program to detect and report data integrity issues involves several components. We need to build a flexible and efficient scanner to handle large datasets. Below is an example program to achieve this goal. This program checks for missing values, duplicate entries, and outliers. It also includes logging for error handling and better traceability.

```python
import pandas as pd
import numpy as np
import logging
from scipy import stats

# Configure logging
logging.basicConfig(filename='data_integrity_scanner.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    """
    Load data from a CSV file.
    
    Args:
    file_path (str): Path to the dataset file.
    
    Returns:
    pd.DataFrame: Loaded data as a pandas DataFrame.
    """
    try:
        data = pd.read_csv(file_path)
        logging.info(f'Data loaded successfully from {file_path}')
        return data
    except Exception as e:
        logging.error(f"Error loading data from {file_path}: {e}")
        raise

def check_missing_values(data):
    """
    Check for missing values in the dataset.
    
    Args:
    data (pd.DataFrame): Dataset to be checked.
    
    Returns:
    pd.Series: Count of missing values per column.
    """
    missing_values = data.isnull().sum()
    logging.info('Missing values checked')
    return missing_values

def check_duplicates(data):
    """
    Check for duplicate rows in the dataset.
    
    Args:
    data (pd.DataFrame): Dataset to be checked.
    
    Returns:
    int: Count of duplicate rows.
    """
    duplicate_count = data.duplicated().sum()
    logging.info('Duplicate rows checked')
    return duplicate_count

def check_outliers(data, z_thresh=3):
    """
    Check for outliers in the dataset using Z-score.
    
    Args:
    data (pd.DataFrame): Dataset to be checked.
    z_thresh (float): Z-score threshold to identify outliers (default is 3).
    
    Returns:
    dict: Dictionary with column names as keys and lists of outlier indices as values.
    """
    outliers = {}
    for col in data.select_dtypes(include=[np.number]).columns:
        z_scores = np.abs(stats.zscore(data[col].dropna()))
        outlier_indices = np.where(z_scores > z_thresh)[0]
        if len(outlier_indices) > 0:
            outliers[col] = outlier_indices.tolist()
    logging.info('Outliers checked')
    return outliers

def generate_report(missing_values, duplicate_count, outliers):
    """
    Generate a report of the integrity issues found in the dataset.
    
    Args:
    missing_values (pd.Series): Count of missing values.
    duplicate_count (int): Count of duplicate rows.
    outliers (dict): Dictionary of outlier indices.
    
    Returns:
    str: Formatted report of the dataset integrity issues.
    """
    report = "Data Integrity Report\n"
    report += "=====================\n"
    report += "Missing Values:\n"
    report += missing_values.to_string() + "\n\n"
    report += f"Duplicate Rows: {duplicate_count}\n\n"
    report += "Outliers:\n"
    for col, indices in outliers.items():
        report += f"{col}: {len(indices)} outliers at indices {indices}\n"
    logging.info('Report generated')
    return report

def main():
    # Specify the path to your dataset
    file_path = 'your_dataset.csv'  # Change this to your dataset path

    try:
        # Load the dataset
        data = load_data(file_path)
        
        # Check for data integrity issues
        missing_values = check_missing_values(data)
        duplicate_count = check_duplicates(data)
        outliers = check_outliers(data)
        
        # Generate and print the report
        report = generate_report(missing_values, duplicate_count, outliers)
        print(report)
    
    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")
        print(f"An error occurred. Please check the log file for details.")

if __name__ == "__main__":
    main()
```

### Key Components:
- **Logging**: Set up to track events and errors.
- **Data Loading**: Uses Pandas to load data, with error handling.
- **Integrity Checks**:
  - Missing values are detected and counted for each column.
  - Duplicate rows are identified and counted.
  - Outliers are detected using Z-score for numeric columns.
- **Report Generation**: A summary of findings is printed and logged.
- **Error Handling**: Catches and logs exceptions to ensure robustness.

Be sure to replace `'your_dataset.csv'` with the actual path to your dataset. This script is designed to be modular, allowing for easy addition of further integrity checks (e.g., data type validation, range checking) as needed.