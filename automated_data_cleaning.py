import pandas as pd
from pathlib import Path

def load_dataset(file_path, **kwargs):
    """
    Load data from various file formats while handling common issues.
    
    Args:
        file_path (str): Path to the data file
        **kwargs: Additional arguments to pass to the appropriate pandas reader
    
    Returns:
        pd.DataFrame: Loaded and initially processed dataframe
    """
    file_type = Path(file_path).suffix.lower()
    
    # Dictionary of file handlers
    handlers = {
        '.csv': pd.read_csv,
        '.xlsx': pd.read_excel,
        '.json': pd.read_json,
        '.parquet': pd.read_parquet
    }
    
    # Get appropriate reader function
    reader = handlers.get(file_type)
    if reader is None:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    # Load data with common cleaning parameters
    df = reader(file_path, **kwargs)
    
    # Initial cleaning steps
    df.columns = df.columns.str.strip().str.lower() # Standardize column names
    df = df.replace('', pd.NA) # Convert empty strings to NA
    
    return df


def validate_dataset(df, validation_rules=None):
    """
    Apply validation rules to a dataframe and return validation results.
    
    Args:
        df (pd.DataFrame): Input dataframe
        validation_rules (dict): Dictionary of column names and their validation rules
        
    Returns:
        dict: Validation results with issues found
    """
    if validation_rules is None:
        validation_rules = {
            'numeric_columns': {
                'check_type': 'numeric',
                'min_value': 0,
                'max_value': 1000000
            },
            'date_columns': {
                'check_type': 'date',
                'min_date': '2000-01-01',
                'max_date': '2025-12-31'
            }
        }
    
    validation_results = {}
    
    for column, rules in validation_rules.items():
        if column not in df.columns:
            continue
            
        issues = []
        
        # Check for missing values
        missing_count = df[column].isna().sum()
        if missing_count > 0:
            issues.append(f"Found {missing_count} missing values")
            
        # Type-specific validations
        if rules['check_type'] == 'numeric':
            if not pd.api.types.is_numeric_dtype(df[column]):
                issues.append("Column should be numeric")
            else:
                out_of_range = df[
                    (df[column] < rules['min_value']) | 
                    (df[column] > rules['max_value'])
                ]
                if len(out_of_range) > 0:
                    issues.append(f"Found {len(out_of_range)} values outside allowed range")
                    
        validation_results[column] = issues
    
    return validation_results


class DataCleaningPipeline:
    """
    A modular pipeline for cleaning data with customizable steps.
    """
    
    def __init__(self):
        self.steps = []
        
    def add_step(self, name, function):
        """Add a cleaning step."""
        self.steps.append({'name': name, 'function': function})
        
    def execute(self, df):
        """Execute all cleaning steps in order."""
        results = []
        current_df = df.copy()
        
        for step in self.steps:
            try:
                current_df = step['function'](current_df)
                results.append({
                    'step': step['name'],
                    'status': 'success',
                    'rows_affected': len(current_df)
                })
            except Exception as e:
                results.append({
                    'step': step['name'],
                    'status': 'failed',
                    'error': str(e)
                })
                break
                
        return current_df, results


def remove_duplicates(df):
    """Remove duplicate rows."""
    return df.drop_duplicates()


def standardize_dates(df):
    """Convert date columns to standardized datetime format."""
    date_columns = df.select_dtypes(include=['datetime64']).columns
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df


def clean_text_columns(df, columns=None):
    """
    Apply standardized text cleaning to specified columns.
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (list): List of columns to clean. If None, clean all object columns
    
    Returns:
        pd.DataFrame: Dataframe with cleaned text columns
    """
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns
        
    df = df.copy()
    
    for column in columns:
        if column not in df.columns:
            continue
            
        # Apply string cleaning operations
        df[column] = (df[column]
                     .astype(str)
                     .str.strip()
                     .str.lower()
                     .replace(r'\s+', ' ', regex=True) # Replace multiple spaces
                     .replace(r'[^\w\s]', '', regex=True)) # Remove special characters
                     
    return df


def generate_quality_metrics(df, baseline_metrics=None):
    """
    Generate quality metrics for a dataset and compare with baseline if provided.
    
    Args:
        df (pd.DataFrame): Input dataframe
        baseline_metrics (dict): Previous metrics to compare against
        
    Returns:
        dict: Current metrics and comparison with baseline
    """
    metrics = {
        'row_count': len(df),
        'missing_values': df.isna().sum().to_dict(),
        'unique_values': df.nunique().to_dict(),
        'data_types': df.dtypes.astype(str).to_dict()
    }
    
    # Add descriptive statistics for numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns
    metrics['numeric_stats'] = df[numeric_columns].describe().to_dict()
    
    # Compare with baseline if provided
    if baseline_metrics:
        metrics['changes'] = {
            'row_count_change': metrics['row_count'] - baseline_metrics['row_count'],
            'missing_values_change': {
                col: metrics['missing_values'][col] - baseline_metrics['missing_values'][col]
                for col in metrics['missing_values']
            }
        }
    
    return metrics


# Example Usage:
if __name__ == "__main__":
    # Load dataset
    file_path = "Data/netflix_titles.csv"
    df = load_dataset(file_path)

    # Validate dataset
    validation_results = validate_dataset(df)
    print("Validation Results:", validation_results)

    # Initialize cleaning pipeline
    pipeline = DataCleaningPipeline()
    pipeline.add_step('remove_duplicates', remove_duplicates)
    pipeline.add_step('standardize_dates', standardize_dates)
    pipeline.add_step('clean_text_columns', clean_text_columns)

    # Execute cleaning pipeline
    cleaned_df, pipeline_results = pipeline.execute(df)
    print("Cleaning Pipeline Results:", pipeline_results)

    # Generate quality metrics
    quality_metrics = generate_quality_metrics(cleaned_df)
    print("Quality Metrics:", quality_metrics)