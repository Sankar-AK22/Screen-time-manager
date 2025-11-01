"""
Data Preprocessing Module
Loads, cleans, and analyzes the screen time dataset
"""
import pandas as pd
import numpy as np
import os
import sys

def load_data(filepath='data/screen_time_data.csv'):
    """
    Load the screen time dataset
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded dataset
    """
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Data loaded successfully from {filepath}")
        print(f"📊 Dataset shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"❌ Error: File not found at {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        sys.exit(1)

def check_missing_values(df):
    """
    Check for missing values in the dataset
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        pd.Series: Missing value counts
    """
    missing = df.isnull().sum()
    print("\n🔍 Missing Values Check:")
    if missing.sum() == 0:
        print("✅ No missing values found!")
    else:
        print(missing)
    return missing

def handle_missing_values(df):
    """
    Handle missing values by filling with mean for numeric columns
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        pd.DataFrame: Dataset with handled missing values
    """
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_columns:
        if df[col].isnull().sum() > 0:
            mean_value = df[col].mean()
            df[col].fillna(mean_value, inplace=True)
            print(f"✅ Filled missing values in {col} with mean: {mean_value:.2f}")
    
    return df

def calculate_correlation(df):
    """
    Calculate correlation between variables
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        pd.DataFrame: Correlation matrix
    """
    numeric_df = df.select_dtypes(include=[np.number])
    correlation = numeric_df.corr()
    
    print("\n📊 Correlation Analysis:")
    print(correlation)
    
    print("\n🔍 Key Insights:")
    print(f"Screen Time vs Productivity: {correlation.loc['Screen_Time_Hours', 'Productivity_Score']:.3f}")
    print(f"Study Hours vs Productivity: {correlation.loc['Study_Hours', 'Productivity_Score']:.3f}")
    
    return correlation

def get_statistics(df):
    """
    Get statistical summary of the dataset
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        pd.DataFrame: Statistical summary
    """
    print("\n📈 Statistical Summary:")
    stats = df.describe()
    print(stats)
    return stats

def save_cleaned_data(df, output_path='data/cleaned_screen_time_data.csv'):
    """
    Save cleaned dataset to CSV
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        output_path (str): Output file path
    """
    try:
        df.to_csv(output_path, index=False)
        print(f"\n✅ Cleaned data saved to {output_path}")
    except Exception as e:
        print(f"❌ Error saving cleaned data: {e}")

def preprocess_data():
    """
    Main preprocessing pipeline
    """
    print("=" * 60)
    print("🔧 DATA PREPROCESSING PIPELINE")
    print("=" * 60)
    
    # Load data
    df = load_data()
    
    # Check for missing values
    check_missing_values(df)
    
    # Handle missing values
    df = handle_missing_values(df)
    
    # Get statistics
    get_statistics(df)
    
    # Calculate correlation
    calculate_correlation(df)
    
    # Save cleaned data
    save_cleaned_data(df)
    
    print("\n" + "=" * 60)
    print("✅ PREPROCESSING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    return df

if __name__ == "__main__":
    preprocess_data()

