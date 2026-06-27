import ee

def calculate_ndvi(image):
    """
    Calculates the Normalized Difference Vegetation Index (NDVI) for a Sentinel-2 image.
    NDVI = (NIR - RED) / (NIR + RED)
    
    In Sentinel-2:
    - Near-Infrared (NIR) = Band 8
    - Red = Band 4
    
    A healthy crop typically has an NDVI ~0.7, while a dry/stressed crop has ~0.2.
    """
    # Earth Engine has a built-in normalizedDifference function
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    
    # Return the original image with the new NDVI band appended
    return image.addBands(ndvi)
