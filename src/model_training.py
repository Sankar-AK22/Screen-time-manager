"""
Model Training Module
Train a Linear Regression model to predict productivity based on screen time and study hours
"""
import pandas as pd
import numpy as np
import joblib
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def load_cleaned_data(filepath='data/cleaned_screen_time_data.csv'):
    """
    Load the cleaned dataset
    
    Args:
        filepath (str): Path to the cleaned CSV file
        
    Returns:
        pd.DataFrame: Loaded dataset
    """
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Cleaned data loaded successfully from {filepath}")
        print(f"📊 Dataset shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"❌ Error: File not found at {filepath}")
        print("💡 Tip: Run data_preprocessing.py first to generate cleaned data")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        sys.exit(1)

def prepare_features(df):
    """
    Prepare features (X) and target (y) for model training
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        tuple: (X, y) features and target
    """
    # Features: Screen_Time_Hours and Study_Hours
    X = df[['Screen_Time_Hours', 'Study_Hours']]
    
    # Target: Productivity_Score
    y = df['Productivity_Score']
    
    print("\n📊 Features (X):")
    print(X.head())
    print(f"\nShape: {X.shape}")
    
    print("\n🎯 Target (y):")
    print(y.head())
    print(f"Shape: {y.shape}")
    
    return X, y

def split_data(X, y, test_size=0.2, random_state=42):
    """
    Split data into training and testing sets
    
    Args:
        X: Features
        y: Target
        test_size (float): Proportion of test set
        random_state (int): Random seed
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    print(f"\n✂️ Data Split (Test Size: {test_size*100}%):")
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Testing set: {X_test.shape[0]} samples")
    
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    """
    Train a Linear Regression model
    
    Args:
        X_train: Training features
        y_train: Training target
        
    Returns:
        LinearRegression: Trained model
    """
    print("\n🤖 Training Linear Regression Model...")
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    print("✅ Model trained successfully!")
    
    # Display model coefficients
    print("\n📊 Model Coefficients:")
    print(f"Screen Time Hours coefficient: {model.coef_[0]:.4f}")
    print(f"Study Hours coefficient: {model.coef_[1]:.4f}")
    print(f"Intercept: {model.intercept_:.4f}")
    
    return model

def evaluate_model(model, X_train, X_test, y_train, y_test):
    """
    Evaluate the trained model
    
    Args:
        model: Trained model
        X_train: Training features
        X_test: Testing features
        y_train: Training target
        y_test: Testing target
        
    Returns:
        dict: Evaluation metrics
    """
    print("\n📈 MODEL EVALUATION")
    print("=" * 60)
    
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Training metrics
    train_r2 = r2_score(y_train, y_train_pred)
    train_mse = mean_squared_error(y_train, y_train_pred)
    train_rmse = np.sqrt(train_mse)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    
    # Testing metrics
    test_r2 = r2_score(y_test, y_test_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)
    test_rmse = np.sqrt(test_mse)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    
    print("📊 Training Set Performance:")
    print(f"  R² Score: {train_r2:.4f}")
    print(f"  MSE: {train_mse:.4f}")
    print(f"  RMSE: {train_rmse:.4f}")
    print(f"  MAE: {train_mae:.4f}")
    
    print("\n📊 Testing Set Performance:")
    print(f"  R² Score: {test_r2:.4f}")
    print(f"  MSE: {test_mse:.4f}")
    print(f"  RMSE: {test_rmse:.4f}")
    print(f"  MAE: {test_mae:.4f}")
    
    # Check for overfitting
    if train_r2 - test_r2 > 0.1:
        print("\n⚠️ Warning: Possible overfitting detected!")
    else:
        print("\n✅ Model generalization looks good!")
    
    metrics = {
        'train_r2': train_r2,
        'train_mse': train_mse,
        'train_rmse': train_rmse,
        'train_mae': train_mae,
        'test_r2': test_r2,
        'test_mse': test_mse,
        'test_rmse': test_rmse,
        'test_mae': test_mae
    }
    
    return metrics

def save_model(model, filepath='models/linear_regression_model.pkl'):
    """
    Save the trained model to disk
    
    Args:
        model: Trained model
        filepath (str): Output file path
    """
    try:
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        joblib.dump(model, filepath)
        print(f"\n✅ Model saved successfully to {filepath}")
    except Exception as e:
        print(f"❌ Error saving model: {e}")

def train_pipeline():
    """
    Main training pipeline
    """
    print("=" * 60)
    print("🤖 MODEL TRAINING PIPELINE")
    print("=" * 60)
    
    # Load cleaned data
    df = load_cleaned_data()
    
    # Prepare features and target
    X, y = prepare_features(df)
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    metrics = evaluate_model(model, X_train, X_test, y_train, y_test)
    
    # Save model
    save_model(model)
    
    print("\n" + "=" * 60)
    print("✅ MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    return model, metrics

if __name__ == "__main__":
    train_pipeline()

