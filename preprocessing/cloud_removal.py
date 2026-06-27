import ee

def mask_s2_clouds(image):
    """
    Masks clouds in Sentinel-2 images using the QA60 band.
    This helps in removing cloudy pixels from the optical imagery before analysis.
    """
    qa = image.select('QA60')

    # Bits 10 and 11 are clouds and cirrus, respectively.
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11

    # Both flags should be set to zero, indicating clear conditions.
    mask = qa.bitwiseAnd(cloudBitMask).eq(0) \
        .And(qa.bitwiseAnd(cirrusBitMask).eq(0))

    # Scale the image bands to surface reflectance (0-1) by dividing by 10000
    # and update the mask.
    return image.updateMask(mask).divide(10000)
