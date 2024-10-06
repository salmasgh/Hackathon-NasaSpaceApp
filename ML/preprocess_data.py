import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib  # Import joblib to save the scaler parameters
import numpy as np

# Path to the input CSV file
input_csv_file_path = './cleaned_data/filtered_farming_data.csv'
# Output path for preprocessed data
preprocessed_csv_file_path = './cleaned_data/preprocessed_data.csv'
# Output path for scaler parameters
scaler_params_path = './cleaned_data/scaler_params.pkl'

# Load the filtered data
df = pd.read_csv(input_csv_file_path)

# Display initial data shape and first few rows for inspection
print("Initial data shape:", df.shape)
print("First few rows of the DataFrame:")
print(df.head())

# Ensure tb_time_utc is properly decoded and is a string
if 'tb_time_utc' in df.columns:
    df['tb_time_utc'] = df['tb_time_utc'].astype(str) 
    df['tb_time_utc'] = df['tb_time_utc'].str.strip("b'Z")
    df['date'] = pd.to_datetime(df['tb_time_utc'], errors='coerce').dt.date

# Drop tb_time_utc after creating the date column
if 'tb_time_utc' in df.columns:
    df.drop(columns=['tb_time_utc'], inplace=True)
    df.drop(columns=['latitude'], inplace=True)
    df.drop(columns=['longitude'], inplace=True)
    df.drop(columns=['latitude_centroid'], inplace=True)
    df.drop(columns=['longitude_centroid'], inplace=True)
    df.drop(columns=['retrieval_qual_flag'], inplace=True)
    df.drop(columns=['albedo_option3'], inplace=True)

# Step 1: Check for missing values
missing_values = df.isnull().sum()
print("Missing values in each column:")
print(missing_values[missing_values > 0])  

# Handle missing values - Drop rows with any missing values, ignoring 'date' column
df = df.dropna()

# Display data shape after handling missing values
print("Data shape after handling missing values:", df.shape)

# Check if DataFrame is empty after dropping missing values
if df.shape[0] == 0:
    print("No data available after handling missing values. Exiting...")
    exit()

# Step 2: Check for redundant data (duplicates) ignoring the 'date' column
duplicates = df.duplicated(subset=df.columns.difference(['date'])).sum()
print(f"Number of duplicate rows (ignoring 'date' column): {duplicates}")

# Remove duplicate rows based on all columns except 'date'
df = df.drop_duplicates(subset=df.columns.difference(['date']))

# Check if DataFrame is empty after dropping duplicates
if df.shape[0] == 0:
    print("No data available after removing duplicate rows. Exiting...")
    exit()

# Drop tb_time_utc
if 'tb_time_utc' in df.columns:
    df.drop(columns=['tb_time_utc'], inplace=True)

# Display data shape after removing duplicates
print("Data shape after removing duplicates:", df.shape)

# Step 3: Standardize numerical features
# List of numerical columns (adjust if necessary)
columns_to_scale = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

# Check if there are columns to scale
if len(columns_to_scale) == 0:
    print("No numerical columns available for scaling. Exiting...")
    exit()

# Standardization
scaler = StandardScaler()
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

# Save the scaler parameters (mean and scale) to a file
scaler_params = {
    'mean': scaler.mean_,
    'scale': scaler.scale_,
    'columns': columns_to_scale  
}

# Save the scaler parameters using joblib
joblib.dump(scaler_params, scaler_params_path)
print("Scaler parameters have been saved successfully.")

# Step 4: Save the cleaned data to a new CSV file
df.to_csv(preprocessed_csv_file_path, index=False)

print(f"Preprocessed data has been successfully saved to {preprocessed_csv_file_path}")
