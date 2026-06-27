import ee

def calculate_ndmi(image):
    """
    Calculates the Normalized Difference Moisture Index (NDMI) for a Sentinel-2 image.
    NDMI is highly correlated with crop water stress.
    
    NDMI = (NIR - SWIR) / (NIR + SWIR)
    
    In Sentinel-2:
    - Near-Infrared (NIR) = Band 8
    - Short-Wave Infrared (SWIR) = Band 11
    """
    # Calculate NDMI using normalizedDifference
    ndmi = image.normalizedDifference(['B8', 'B11']).rename('NDMI')
    
    # Return the original image with the new NDMI band appended
    return image.addBands(ndmi)
