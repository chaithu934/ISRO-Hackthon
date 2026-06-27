import ee
import geemap
import os
import sys

# Ensure the script can import from utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.satellite import initialize_ee, get_sentinel2_data, get_sentinel1_data

def download_data():
    if not initialize_ee():
        print("Initialization failed. Please authenticate first using 'earthengine authenticate' in your terminal.")
        return

    # Define a small Region of Interest (ROI) - e.g., an agricultural area
    # Format: [longitude_min, latitude_min, longitude_max, latitude_max]
    print("\nDefining Region of Interest (ROI)...")
    roi = ee.Geometry.Rectangle([-100.50, 38.50, -100.45, 38.55])  # Kansas, USA (Wheat)
    
    start_date = '2023-05-01'
    end_date = '2023-06-30'

    # 1. Optical Data (Sentinel-2)
    print("\n--- Fetching Optical (Sentinel-2) Data ---")
    s2_collection = get_sentinel2_data(roi, start_date, end_date)
    # Get the median pixel values over the month to reduce clouds, then clip to our ROI
    s2_image = s2_collection.median().clip(roi)
    # Select key bands: B4 (Red), B8 (NIR), B11 (SWIR)
    s2_image = s2_image.select(['B4', 'B8', 'B11'])

    # 2. Microwave Data (Sentinel-1 SAR)
    print("\n--- Fetching Microwave (Sentinel-1) Data ---")
    s1_collection = get_sentinel1_data(roi, start_date, end_date)
    s1_image = s1_collection.median().clip(roi)
    # Select SAR polarization bands
    s1_image = s1_image.select(['VV', 'VH'])

    # 3. Export to local directory
    out_dir = os.path.join(os.getcwd(), 'dataset')
    s2_out = os.path.join(out_dir, 'sentinel2', 'wheat_optical_sample.tif')
    s1_out = os.path.join(out_dir, 'sentinel1', 'wheat_microwave_sample.tif')

    print(f"\nDownloading Optical Data to: {s2_out}")
    print("This may take a minute...")
    try:
        geemap.ee_export_image(s2_image, filename=s2_out, scale=10, region=roi, file_per_band=False)
        print("Optical Data Downloaded Successfully! ✅")
    except Exception as e:
        print(f"Failed to download Optical data: {e}")

    print(f"\nDownloading Microwave Data to: {s1_out}")
    try:
        geemap.ee_export_image(s1_image, filename=s1_out, scale=10, region=roi, file_per_band=False)
        print("Microwave Data Downloaded Successfully! ✅")
    except Exception as e:
        print(f"Failed to download Microwave data: {e}")

if __name__ == "__main__":
    download_data()
