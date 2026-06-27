import ee

def calculate_evi(image):
    """
    Calculates the Enhanced Vegetation Index (EVI).
    Provides better vegetation analysis in areas with high biomass.
    Formula: 2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))
    """
    evi = image.expression(
        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
            'NIR': image.select('B8'),
            'RED': image.select('B4'),
            'BLUE': image.select('B2')
        }).rename('EVI')
    return image.addBands(evi)

def calculate_savi(image, L=0.5):
    """
    Calculates Soil Adjusted Vegetation Index (SAVI).
    Used to correct for soil background brightness in areas with low vegetative cover.
    Formula: ((NIR - RED) / (NIR + RED + L)) * (1 + L)
    """
    savi = image.expression(
        '((NIR - RED) / (NIR + RED + L)) * (1 + L)', {
            'NIR': image.select('B8'),
            'RED': image.select('B4'),
            'L': L
        }).rename('SAVI')
    return image.addBands(savi)

def add_all_indices(image):
    """
    Master function to add all spectral indices (NDVI, NDMI, EVI, SAVI) to a given Sentinel-2 image.
    Note: Assumes calculate_ndvi and calculate_ndmi are imported if used externally, 
    but for simplicity, we map them directly here if part of a pipeline.
    """
    from preprocessing.ndvi import calculate_ndvi
    from preprocessing.ndmi import calculate_ndmi
    
    img_with_ndvi = calculate_ndvi(image)
    img_with_ndmi = calculate_ndmi(img_with_ndvi)
    img_with_evi = calculate_evi(img_with_ndmi)
    final_img = calculate_savi(img_with_evi)
    
    return final_img
