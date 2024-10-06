from flask import Flask, jsonify, request
import earthaccess
import requests
import os
import h5py
import numpy as np
import pandas as pd
from flask_cors import CORS
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app) 

@app.route('/api/data', methods=['GET'])
def fetch_data():
    # Get query parameters
    bounding_box = request.args.getlist('bounding_box', type=float)
    start_date = request.args.get('start_date', default= datetime.strptime('2024-09-29', '%Y-%m-%d')- timedelta(days=31) )
    end_date = request.args.get('end_date', default= datetime.strptime('2024-09-29', '%Y-%m-%d')) 
    # start_date = request.args.get('start_date', default= datetime.today().date() - timedelta(days=7) )
    # end_date = request.args.get('end_date', default= datetime.today().date() ) 
    short_name = 'SPL2SMP'

    # Ensure the bounding box is provided and is valid
    if len(bounding_box) != 4:
        return jsonify({"error" : "Bounding box must have exactly four float values: [west, south, east, north]."}), 400

    # Log in using netrc
    try:
        auth = earthaccess.login(strategy='netrc')
    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}. Attempting interactive login."}), 401

    # Fall back to interactive login if netrc fails
    try:
        auth = earthaccess.login()  
    except Exception as e:
        return jsonify({"error": f"Interactive login failed: {str(e)}"}), 401

    # Unpack bounding box values
    lower_left_lon, lower_left_lat, upper_right_lon, upper_right_lat = bounding_box

    # Search data
    results = earthaccess.search_data(
        short_name=short_name,
        bounding_box=(lower_left_lon, lower_left_lat, upper_right_lon, upper_right_lat),
        temporal=(start_date, end_date),
        count=1  
    )

    if not results:
        return jsonify({"message": "No results found."}), 404

    response_data = []
    download_links = []
    for result in results:
        download_links.extend([
            url['URL'] for url in result['umm'].get('RelatedUrls', [])
            if url['Type'] == 'GET DATA'
        ])
        response_data.append({
            "meta": result['meta'],
            "size": result['size'],
            "umm_keys": list(result['umm'].keys())
        })

    # Start download and monitor
    if download_links:
        download_url = download_links[0]
        print(f"Attempting to download from: {download_url}")

        # Attempt to download the file
        filename = download_file(download_url)
        if filename:
            # Convert the downloaded file to CSV
            convert_to_csv(filename)
            response_data.append({"message": "File download and conversion successful."})
        else:
            return jsonify({"error": "File download failed due to authorization issues"}), 401

    #Filter data
    csv_file_path = filename.replace('.h5', '.csv')
    filter_data(csv_file_path, bounding_box)

    json_data = csv_to_json(csv_file_path)

    # os.remove(csv_file_path)

    return jsonify(json_data)

def download_file(url):
    """Download a file and resume if incomplete."""
    try:
        filename = url.split('/')[-1]  # Extract filename from URL

        # Check if the file already exists
        resume_header = None
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            resume_header = {'Range': f'bytes={file_size}-'}

        # Use retries with backoff strategy for robust downloading
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))

        # Start or resume the download
        with session.get(url, headers=resume_header, stream=True) as response:
            if response.status_code == 416:
                print(f"Range not satisfiable. Starting fresh download of {filename}.")
                resume_header = None  # Reset range header to download the entire file
                response = session.get(url, headers=resume_header, stream=True)

            response.raise_for_status()  # Check for HTTP errors

            # Open the file in append mode for resuming
            with open(filename, 'ab' if resume_header else 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

        print(f"Download of {filename} complete")
        return filename

    except Exception as e:
        print(f"Failed to download file: {str(e)}")
        return None

def convert_to_csv(file_path):
    """Determine file type and convert to CSV."""
    file_name, file_ext = os.path.splitext(file_path)
    output_csv = file_name + ".csv"

    if file_ext in ['.h5']:
        convert_h5_to_csv(file_path, output_csv)
    else:
        print(f"Unsupported file format: {file_ext}")
    
    #delete file after conversion
    os.remove(file_path)

def convert_h5_to_csv(input_file, output_file):
    """Convert HDF5 (.h5) file to CSV using the provided key and underkey."""
    try:
        with h5py.File(input_file, 'r') as hdf5_file:
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
            df.to_csv(output_file, index=False)
            print(f"Successfully converted {input_file} to {output_file}.")
    except Exception as e:
        print(f"Conversion failed: {str(e)}")

def filter_data(file_path, bounding_box):
    """
    Filter the data based on the bounding box and save it to the same CSV file.
    Args:
    - file_path (str): Path to the CSV file.
    - bounding_box (list): A list of four float values: [west, south, east, north].
    """
    try:
        print(f"Attempting to filter data for bounding box: {bounding_box}")
        
        # Read the CSV file
        data = pd.read_csv(file_path)

        # Unpack bounding box values: [west, south, east, north]
        west, south, east, north = bounding_box

        # Filter the data based on latitude and longitude
        filtered_df = data[
            (data['latitude'] >= south) &
            (data['latitude'] <= north) &
            (data['longitude'] >= west) &
            (data['longitude'] <= east)
        ]

        # Specify the columns you want to keep (modify as necessary)
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
            'tb_time_utc',  # Include tb_time_utc for date extraction
            'surface_water_fraction_mb_h',
            'surface_water_fraction_mb_v',
        ]

        # Filter the DataFrame to keep only the specified columns
        filtered_df = filtered_df[columns_to_keep]

        # Exclude rows where soil_moisture is -9999.0 or NaN
        filtered_df = filtered_df[filtered_df['soil_moisture'].notna() & (filtered_df['soil_moisture'] != -9999.0)]

        # Save the averaged DataFrame to the same CSV file
        output_file = file_path
        filtered_df.to_csv(output_file, index=False)

        print(f"Filtered and averaged data saved to {output_file}")
    except Exception as e:
        print(f"Error filtering data: {str(e)}")
        return None

def csv_to_json(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Filter the relevant columns
    factors = ['clay_fraction', 'sand_fraction', 'organic_content', 'soil_moisture', 'albedo', 'vegetation_water_content']
    filtered_df = df[factors]
    
    # Calculate average values for the specified factors
    averages = filtered_df.mean().to_dict()  # Convert the averages to a dictionary
    
    # Convert the averages to JSON format
    json_data = json.dumps(averages, indent=4)
    
    # Return the JSON data as a dictionary
    return json.loads(json_data)

if __name__ == '__main__':
    app.run(debug=True)
