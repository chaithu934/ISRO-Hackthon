import ee
import geemap
import os

def initialize_ee():
    """
    Initializes Google Earth Engine. 
    Note: The user must run `earthengine authenticate` in their terminal first.
    """
    try:
        # Initialize with the user's project ID
        ee.Initialize(project='crop-ai-project-500607')
        print("Earth Engine initialized successfully.")
        return True
    except Exception as e:
        print(f"Initialization failed: {e}")
        print("Please run 'earthengine authenticate' in your terminal.")
        return False

def get_sentinel2_data(roi, start_date, end_date, max_cloud_cover=20):
    """
    Fetches Sentinel-2 MSI Level-2A data (Optical).
    
    Args:
        roi (ee.Geometry): The region of interest.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        max_cloud_cover (int): Maximum percentage of cloud cover allowed.
        
    Returns:
        ee.ImageCollection: Filtered Sentinel-2 collection.
    """
    collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                  .filterBounds(roi)
                  .filterDate(start_date, end_date)
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', max_cloud_cover)))
    return collection

def get_sentinel1_data(roi, start_date, end_date):
    """
    Fetches Sentinel-1 SAR GRD data (Microwave).
    Useful because it can penetrate clouds and provides structural data.
    
    Args:
        roi (ee.Geometry): The region of interest.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        
    Returns:
        ee.ImageCollection: Filtered Sentinel-1 collection.
    """
    collection = (ee.ImageCollection("COPERNICUS/S1_GRD")
                  .filterBounds(roi)
                  .filterDate(start_date, end_date)
                  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
                  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
                  .filter(ee.Filter.eq('instrumentMode', 'IW')))
    return collection

def export_image_to_drive(image, description, folder, region, scale=10):
    """
    Exports an Earth Engine image to Google Drive as a GeoTIFF.
    """
    task = ee.batch.Export.image.toDrive(
        image=image,
        description=description,
        folder=folder,
        region=region,
        scale=scale,
        fileFormat='GeoTIFF',
        maxPixels=1e13
    )
    task.start()
    print(f"Export task '{description}' started. Check your Google Earth Engine tasks tab.")
    return task
