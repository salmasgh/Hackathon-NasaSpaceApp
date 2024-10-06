import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

# File paths
filtered_data_path = './cleaned_data/filtered_farming_data.csv'
kmeans_model_path = './kmeans_model.pkl'
scaler_path = './scaler_params.pkl'
cluster_quality_mapping_path = './cleaned_data/cluster_quality_labels.csv'

# Load the filtered farming data
df = pd.read_csv(filtered_data_path)

# Load the KMeans model and the scaler
kmeans = joblib.load(kmeans_model_path)
scaler_params = joblib.load(scaler_path)

# Load the cluster-to-quality-label mapping
cluster_quality_df = pd.read_csv(cluster_quality_mapping_path)

# Step 1: Pick a random row from the filtered farming data (excluding non-numerical columns)
random_row = df.sample(n=1).copy() 

print("Selected random row from the farming data:")
print(random_row)
print(scaler_params)


# Step 2: Drop any non-numerical columns from the random row
columns_to_drop = ['tb_time_utc', 'latitude', 'longitude', 'latitude_centroid', 'longitude_centroid', 'retrieval_qual_flag', 'albedo_option3']
random_row.drop(columns=columns_to_drop, inplace=True, errors='ignore')

# Step 3: Ensure the random row has the same columns as used during scaling
random_row = random_row[scaler_params['columns']]
print(random_row.to_string(index=False))

# Manual scaling function
def manual_scaler_transform(data, scaler_params):
    return (data - scaler_params['mean']) / scaler_params['scale']

# Step 4: Scale the selected random row
scaled_row = manual_scaler_transform(random_row, scaler_params)

# Step 5: Predict the cluster for the random row using the KMeans model
predicted_cluster = kmeans.predict(scaled_row)[0]  # Get the first (and only) prediction

print(f"Predicted cluster: {predicted_cluster}")

# Step 6: Map the predicted cluster to its quality label
quality_label = cluster_quality_df[cluster_quality_df['cluster'] == predicted_cluster]['quality_label'].values

if len(quality_label) > 0:
    print(f"The quality label for cluster {predicted_cluster} is: {quality_label[0]}")
else:
    print(f"No quality label found for cluster {predicted_cluster}")
