import h5py
import pandas as pd
import numpy as np
import os

# Path to your HDF5 files directory
hdf5_directory = 'downloads/'
# Output CSV file path
output_csv_file_path = 'filtered_farming_data.csv'

dataframes = []

# Iterate through all files in the downloads directory
for filename in os.listdir(hdf5_directory):
    if filename.endswith('.h5'):
        hdf5_file_path = os.path.join(hdf5_directory, filename)
        
        with h5py.File(hdf5_file_path, 'r') as hdf5_file:
            # Access the 'Soil_Moisture_Retrieval_Data' group
            soil_moisture_group = hdf5_file['Soil_Moisture_Retrieval_Data']
            data = {}
            
            for dataset_name in soil_moisture_group.keys():
                dataset = soil_moisture_group[dataset_name][:]
                
                # Flatten the dataset if it's multi-dimensional
                if dataset.ndim > 1:
                    dataset = dataset.flatten()
                
                # Add the dataset to the dictionary
                data[dataset_name] = dataset
            
            # Find the maximum length of the datasets
            max_length = max(len(d) for d in data.values())
            
            # Pad datasets with fewer elements with NaNs so they all have the same length
            for dataset_name in data:
                if len(data[dataset_name]) < max_length:
                    data[dataset_name] = np.pad(data[dataset_name], 
                                                (0, max_length - len(data[dataset_name])), 
                                                constant_values=np.nan)
            
            df = pd.DataFrame(data)
            
            # Append the DataFrame to the list
            dataframes.append(df)

# Combine all DataFrames into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Specify columns to keep
columns_to_keep = [
    'soil_moisture',
    'surface_temperature',
    'albedo',
    'albedo_option3',
    'roughness_coefficient',
    'bulk_density',
    'clay_fraction',
    'sand_fraction',
    'organic_content',
    'vegetation_water_content',
    'latitude',
    'longitude',
    'latitude_centroid',
    'longitude_centroid',
    'retrieval_qual_flag',
    'tb_time_utc',
    'surface_water_fraction_mb_h',
    'surface_water_fraction_mb_v',
]

# Filter the DataFrame to keep only the specified columns
filtered_df = combined_df[columns_to_keep]

# Exclude rows where soil_moisture is -9999.0 or empty
filtered_df = filtered_df[filtered_df['soil_moisture'].notna() & (filtered_df['soil_moisture'] != -9999.0)]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv(output_csv_file_path, index=False)

print(f"Filtered data has been successfully saved to {output_csv_file_path}")
