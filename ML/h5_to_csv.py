import h5py
import pandas as pd
import numpy as np

# Path to your HDF5 file
hdf5_file_path = 'downloads/'
csv_file_path = 'filtered_data/'

# Open the HDF5 file
with h5py.File(hdf5_file_path, 'r') as hdf5_file:
    
    # Access the 'Soil_Moisture_Retrieval_Data' group
    soil_moisture_group = hdf5_file['Soil_Moisture_Retrieval_Data']
    
    # Create an empty dictionary to hold the dataset data
    data = {}
    
    # Iterate over all datasets under the 'Soil_Moisture_Retrieval_Data' key
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
    
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data)
    
    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

print(f"Data has been successfully written to {csv_file_path}")
