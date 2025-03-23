import kagglehub
import os

# Download latest version of the dataset
print("Downloading dataset from Kaggle...")
path = kagglehub.dataset_download("shivamb/all-exoplanets-dataset")
print(f"Dataset downloaded to: {path}")

# List the files in the downloaded dataset
print("\nFiles in the dataset:")
for file in os.listdir(path):
    print(f" - {file}")
