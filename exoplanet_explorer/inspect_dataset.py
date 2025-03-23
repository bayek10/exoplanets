import kagglehub
import pandas as pd
import os

# Download the dataset
print("Downloading dataset from Kaggle...")
path = kagglehub.dataset_download("shivamb/all-exoplanets-dataset")

# List files in the downloaded directory
print("\nFiles in the downloaded directory:")
for file in os.listdir(path):
    print(f" - {file}")
    
    # If it's a CSV file, inspect its structure
    if file.endswith('.csv'):
        file_path = os.path.join(path, file)
        df = pd.read_csv(file_path)
        
        print(f"\nDataset shape: {df.shape}")
        print("\nColumn names:")
        for col in df.columns:
            print(f" - {col}")
            
        print("\nFirst few rows:")
        print(df.head())
        
        print("\nData types:")
        print(df.dtypes)
        
        print("\nSummary statistics:")
        print(df.describe())
