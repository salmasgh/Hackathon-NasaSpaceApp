import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
import joblib
import numpy as np

# Path to the preprocessed CSV file
input_csv_file_path = './cleaned_data/preprocessed_data.csv'

# Load the preprocessed data
df = pd.read_csv(input_csv_file_path)

# Step 1: Remove the 'date' column since it's not needed for clustering
if 'date' in df.columns:
    print("DEBUG: Dropping 'date' column.")
    df.drop(columns=['date'], inplace=True)
else:
    print("DEBUG: 'date' column not found.")

# Debug: Data shape after dropping 'date'
print("DEBUG: Data shape after dropping 'date':", df.shape)

# Sample size for clustering
sample_size = 10000

if sample_size > df.shape[0]:
    raise ValueError("Sample size cannot be greater than the number of available rows in the DataFrame.")

random_indices = np.random.choice(df.index, sample_size, replace=False)
df = df.loc[random_indices]

# Step 2: Fit the K-Means model directly with a chosen number of clusters
optimal_k = 200  # Chosen number of clusters for testing
print(f"DEBUG: Fitting K-Means model with {optimal_k} clusters.")
kmeans = KMeans(n_clusters=optimal_k, random_state=42)

# Fit the model and assign clusters
df['cluster'] = kmeans.fit_predict(df)

# Debug: Cluster centers and inertia
print("DEBUG: Cluster centers:\n", kmeans.cluster_centers_)
print("DEBUG: Inertia:", kmeans.inertia_)

score = silhouette_score(df, kmeans.labels_)
print(f"DEBUG: Silhouette Score for {optimal_k} clusters: {score}")

# Step 3: Calculate aggregate metrics for each cluster
# Define relevant features for crop yield
relevant_features = ['soil_moisture', 'organic_content', 'sand_fraction', 'vegetation_water_content']
cluster_metrics = df.groupby('cluster')[relevant_features].mean().reset_index()

# Step 4: Score clusters based on aggregate metrics
cluster_metrics['score'] = (
    0.2 * cluster_metrics['soil_moisture'] + 
    0.2 * cluster_metrics['vegetation_water_content'] + 
    0.2 * cluster_metrics['organic_content'] -  
    0.4 * cluster_metrics['sand_fraction'] 
)

# Step 5: Rank and label the clusters based on score
cluster_metrics = cluster_metrics.sort_values(by='score', ascending=False)

def label_cluster(score):
    if score < 0.3: 
        return 'Worst'
    elif score < 0.5:
        return 'Poor'
    elif score < 0.7:
        return 'Average'
    else:
        return 'Good'

# Assign quality labels based on scores
cluster_metrics['quality_label'] = cluster_metrics['score'].apply(label_cluster)

# Step 6: Merge quality labels back to the original DataFrame
df = df.merge(cluster_metrics[['cluster', 'quality_label']], on='cluster', how='left')

# Plotting the clusters
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['soil_moisture'], df['organic_content'], c=df['cluster'], cmap='viridis', alpha=0.5)
plt.title(f'K-Means Clustering with {optimal_k} Clusters')
plt.xlabel('Soil Moisture')
plt.ylabel('Organic Content')
plt.colorbar(scatter, label='Cluster Label')
plt.show()

# Save the resulting DataFrame with cluster labels to a new CSV file
output_csv_file_path = './cleaned_data/clustering_results.csv'
df.to_csv(output_csv_file_path, index=False)
# Save the model
joblib.dump(kmeans, 'kmeans_model.pkl')

print(f"DEBUG: Clustering results have been successfully saved to {output_csv_file_path}")
