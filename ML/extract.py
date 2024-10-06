import earthaccess
import os
import pandas as pd
from datetime import datetime, timedelta

# Authenticate with EarthAccess
auth = earthaccess.login(strategy='netrc')

# Define the bounding box (min_lon, min_lat, max_lon, max_lat)
bounding_box = (7.25, 32.5, 11.6, 37.5)  # Area coordinates

# Define the start and end dates
start_date = "2023-08-30"
end_date = "2024-08-30"

# Create a download directory if it does not exist
download_dir = './downloads'
os.makedirs(download_dir, exist_ok=True)

# Generate a list of dates to query
date_range = pd.date_range(start=start_date, end=end_date)

# Specify the dataset short name for SMAP data
short_name = 'SPL2SMP'

# Loop through each date in the range
for single_date in date_range:
    date_str = single_date.strftime("%Y-%m-%d")
    try:
        # Perform a search for datasets
        results = earthaccess.search_data(
            short_name=short_name,
            bounding_box=bounding_box,
            temporal=(date_str, date_str), 
            count=1  
        )
    except:
         print(f"No results found for {date_str}.")
         continue
    
    print(f"Results found for {date_str}: {len(results)}\n")
    for result in results:
        print("Meta:", result['meta'])  
        print("Size (MB):", result['size']) 
        print("UMM Keys:", result['umm'].keys())  
        
        # Check for related URLs and download links
        if 'RelatedUrls' in result['umm']:
            for url in result['umm']['RelatedUrls']:
                if url['Type'] == 'GET DATA':
                    print(f"Download link: {url['URL']}")
                    
                    # Download the data
                    response = earthaccess.download(url['URL'], local_path=download_dir)
                    if response:
                        print(f"Downloaded: {url['URL']}")
                    else:
                        print(f"Failed to download data from: {url['URL']}")
        else:
            print("No valid results found.")

        print("\n" + "-" * 40 + "\n")
