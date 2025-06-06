import pandas as pd
import numpy as np
import os
from typing import Dict, List, Tuple, Optional, Union

def load_raw_data(
    recipe: str,
    session: str,
    data_folder: str = "data",
    base_dir: Optional[str] = None,
    temperature: Optional[str] = None
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    """
    Load raw data and labels from the specified session
    
    Args:
        recipe: Name of the recipe ('EggWhitesWhisking' or 'Whipping Cream')
        session: Name of the session folder
        data_folder: Name of the data folder (default: 'data')
        base_dir: Base directory path (default: current directory)
        temperature: Temperature setting (only for EggWhitesWhisking)
        
    Returns:
        Tuple of (data DataFrame, labels DataFrame)
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    if recipe == "EggWhitesWhisking" and temperature:
        data_file = os.path.join(base_dir, data_folder, recipe, temperature, session, "data.data")
        label_file = os.path.join(base_dir, data_folder, recipe, temperature, session, "labels.label")
    else:
        data_file = os.path.join(base_dir, data_folder, recipe, session, "data.data")
        label_file = os.path.join(base_dir, data_folder, recipe, session, "labels.label")
    
    # Load data
    data = pd.read_csv(data_file)
    
    # Load labels if they exist
    labels = None
    if os.path.exists(label_file):
        labels = pd.read_csv(label_file)
    
    return data, labels

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw data by handling missing values and outliers
    
    Args:
        data: Raw data DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    # Create a copy to avoid modifying the original data
    cleaned_data = data.copy()
    
    # Handle missing values
    cleaned_data = cleaned_data.fillna(method='ffill').fillna(method='bfill')
    
    # Detect and handle outliers using IQR method
    for column in cleaned_data.columns:
        if column != 'Time':  # Skip time column
            Q1 = cleaned_data[column].quantile(0.25)
            Q3 = cleaned_data[column].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define outlier bounds
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Replace outliers with bounds
            cleaned_data[column] = cleaned_data[column].clip(lower_bound, upper_bound)
    
    return cleaned_data

def normalize_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the data using min-max scaling
    
    Args:
        data: DataFrame to normalize
        
    Returns:
        Normalized DataFrame
    """
    # Create a copy to avoid modifying the original data
    normalized_data = data.copy()
    
    # Skip time column for normalization
    for column in normalized_data.columns:
        if column != 'Time':
            min_val = normalized_data[column].min()
            max_val = normalized_data[column].max()
            if max_val > min_val:
                normalized_data[column] = (normalized_data[column] - min_val) / (max_val - min_val)
    
    return normalized_data

def add_label_column(
    data: pd.DataFrame, 
    labels: pd.DataFrame
) -> pd.DataFrame:
    """
    Add a 'label' column to the data based on the labels DataFrame
    
    Args:
        data: Data DataFrame
        labels: Labels DataFrame
        
    Returns:
        Data DataFrame with added label column
    """
    if labels is None or labels.empty:
        return data
    
    # Create a copy to avoid modifying the original data
    result = data.copy()
    
    # Add a 'label' column with default value 'NotReady'
    result['label'] = 'NotReady'
    
    # Apply labels based on time ranges
    for _, label_row in labels.iterrows():
        start_time = label_row['Time(Seconds)']
        end_time = start_time + label_row['Length(Seconds)']
        label_value = label_row['Label(string)']
        
        # Set label for data points within the time range
        mask = (result['Time'] >= start_time) & (result['Time'] <= end_time)
        result.loc[mask, 'label'] = label_value
    
    return result

def preprocess_data(
    data: pd.DataFrame, 
    labels: Optional[pd.DataFrame] = None,
    clean: bool = True, 
    normalize: bool = True,
    add_labels: bool = True
) -> pd.DataFrame:
    """
    Complete preprocessing pipeline for the data
    
    Args:
        data: Raw data DataFrame
        labels: Labels DataFrame
        clean: Whether to clean the data
        normalize: Whether to normalize the data
        add_labels: Whether to add label column
        
    Returns:
        Preprocessed DataFrame
    """
    result = data.copy()
    
    if clean:
        result = clean_data(result)
    
    if normalize:
        result = normalize_data(result)
    
    if add_labels and labels is not None:
        result = add_label_column(result, labels)
    
    return result
