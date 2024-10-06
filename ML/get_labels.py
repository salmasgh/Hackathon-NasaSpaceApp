import pandas as pd

# Path to the clustering results CSV file
clustering_results_path = './cleaned_data/clustering_results.csv'
# Path for the output CSV containing clusters and quality labels
output_quality_labels_path = './cleaned_data/cluster_quality_labels.csv'

# Load the clustering results
df = pd.read_csv(clustering_results_path)

# Check if 'cluster' and 'quality_label' columns exist in the DataFrame
if 'cluster' not in df.columns or 'quality_label' not in df.columns:
    raise ValueError("The required columns 'cluster' or 'quality_label' are not found in the clustering results.")

# Extract the relevant columns
cluster_quality_df = df[['cluster', 'quality_label']].drop_duplicates()

# Save the extracted data to a new CSV file
cluster_quality_df.to_csv(output_quality_labels_path, index=False)

print(f"Cluster and quality label mappings have been successfully saved to {output_quality_labels_path}")
