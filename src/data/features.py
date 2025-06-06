import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union

def calculate_rolling_statistics(
    data: pd.DataFrame,
    window_size: int = 20,
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Calculate rolling statistical features (mean, std, min, max)
    
    Args:
        data: Input DataFrame
        window_size: Size of the rolling window
        columns: Columns to calculate statistics for (default: all non-time columns)
        
    Returns:
        DataFrame with added rolling statistics features
    """
    result = data.copy()
    
    if columns is None:
        columns = [col for col in data.columns if col not in ['Time', 'label']]
    
    for col in columns:
        # Add rolling mean
        result[f'{col}_rolling_mean'] = result[col].rolling(window=window_size, min_periods=1).mean()
        
        # Add rolling standard deviation
        result[f'{col}_rolling_std'] = result[col].rolling(window=window_size, min_periods=1).std().fillna(0)
        
        # Add rolling min and max
        result[f'{col}_rolling_min'] = result[col].rolling(window=window_size, min_periods=1).min()
        result[f'{col}_rolling_max'] = result[col].rolling(window=window_size, min_periods=1).max()
    
    return result

def calculate_derivatives(
    data: pd.DataFrame,
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Calculate first and second derivatives for numerical columns
    
    Args:
        data: Input DataFrame
        columns: Columns to calculate derivatives for (default: all non-time columns)
        
    Returns:
        DataFrame with added derivative features
    """
    result = data.copy()
    
    if columns is None:
        columns = [col for col in data.columns if col not in ['Time', 'label']]
    
    for col in columns:
        # First derivative (rate of change)
        result[f'{col}_deriv1'] = result[col].diff() / result['Time'].diff()
        
        # Second derivative (acceleration)
        result[f'{col}_deriv2'] = result[f'{col}_deriv1'].diff() / result['Time'].diff()
        
        # Fill NaN values with 0
        result[f'{col}_deriv1'] = result[f'{col}_deriv1'].fillna(0)
        result[f'{col}_deriv2'] = result[f'{col}_deriv2'].fillna(0)
    
    return result

def extract_frequency_features(
    data: pd.DataFrame,
    columns: Optional[List[str]] = None,
    window_size: int = 100
) -> pd.DataFrame:
    """
    Extract frequency domain features using FFT (Fast Fourier Transform)
    
    Args:
        data: Input DataFrame
        columns: Columns to extract frequency features for (default: all non-time columns)
        window_size: Window size for FFT calculation
        
    Returns:
        DataFrame with added frequency domain features
    """
    result = data.copy()
    
    if columns is None:
        columns = [col for col in data.columns if col not in ['Time', 'label']]
    
    for col in columns:
        # Calculate dominant frequency and magnitude for rolling windows
        dominant_freq = []
        dominant_magnitude = []
        
        for i in range(len(data)):
            start_idx = max(0, i - window_size + 1)
            window = data.iloc[start_idx:i+1][col].values
            
            if len(window) > 10:  # Need enough points for meaningful FFT
                fft_vals = np.abs(np.fft.rfft(window))
                fft_freq = np.fft.rfftfreq(len(window))
                
                # Get dominant frequency
                idx = np.argmax(fft_vals[1:]) + 1  # Skip DC component
                if idx < len(fft_freq):
                    dominant_freq.append(fft_freq[idx])
                    dominant_magnitude.append(fft_vals[idx])
                else:
                    dominant_freq.append(0)
                    dominant_magnitude.append(0)
            else:
                dominant_freq.append(0)
                dominant_magnitude.append(0)
        
        result[f'{col}_dom_freq'] = dominant_freq
        result[f'{col}_dom_mag'] = dominant_magnitude
    
    return result

def feature_engineering(
    data: pd.DataFrame,
    include_rolling: bool = True,
    include_derivatives: bool = True,
    include_frequency: bool = False,  # Computationally expensive, off by default
    window_size: int = 20
) -> pd.DataFrame:
    """
    Complete feature engineering pipeline
    
    Args:
        data: Input DataFrame
        include_rolling: Whether to include rolling statistics
        include_derivatives: Whether to include derivatives
        include_frequency: Whether to include frequency domain features
        window_size: Window size for rolling calculations
        
    Returns:
        DataFrame with engineered features
    """
    result = data.copy()
    
    # Extract columns that are neither Time nor label
    columns = [col for col in data.columns if col not in ['Time', 'label']]
    
    # Apply feature engineering steps
    if include_rolling:
        result = calculate_rolling_statistics(result, window_size, columns)
        
    if include_derivatives:
        result = calculate_derivatives(result, columns)
        
    if include_frequency:
        result = extract_frequency_features(result, columns, window_size*5)
    
    return result
