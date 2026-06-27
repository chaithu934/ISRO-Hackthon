import rasterio
import numpy as np
import folium
import matplotlib.colors as mcolors

def generate_crop_map_overlay(tif_path, folium_map):
    """
    Reads a GeoTIFF satellite image, performs a pixel-wise semantic segmentation 
    (simulated via NDVI thresholds for the prototype), and overlays a colored crop mask 
    onto the provided folium map.
    """
    try:
        with rasterio.open(tif_path) as src:
            # Check if image has enough bands (Optical typically has Red & NIR at 1 and 2)
            if src.count < 2:
                print("Image doesn't have enough bands for Pixel-wise classification.")
                return False
                
            # Read Red and Near-Infrared bands
            red = src.read(1).astype(float)
            nir = src.read(2).astype(float)
            
            # Calculate NDVI pixel by pixel
            np.seterr(divide='ignore', invalid='ignore')
            ndvi = (nir - red) / (nir + red)
            ndvi = np.nan_to_num(ndvi, nan=0.0)
            
            # Bounding box of the satellite image
            bounds = src.bounds
            
            # Create a classification mask based on NDVI ranges
            # This is a rule-based pixel classifier for the prototype
            classes = np.zeros_like(ndvi, dtype=np.uint8)
            classes[(ndvi > 0.1) & (ndvi <= 0.3)] = 1  # Wheat
            classes[(ndvi > 0.3) & (ndvi <= 0.45)] = 2 # Maize
            classes[(ndvi > 0.45) & (ndvi <= 0.6)] = 3 # Cotton
            classes[(ndvi > 0.6) & (ndvi <= 0.70)] = 4 # Rice
            classes[(ndvi > 0.70) & (ndvi <= 0.85)] = 5 # Sugarcane
            classes[ndvi > 0.85] = 6                   # Groundnut
            
            # Define colors for each crop
            cmap = mcolors.ListedColormap([
                'transparent',    # 0 Non-crop/Water (transparent)
                '#f1c40f',        # 1 Wheat (Yellow)
                '#e67e22',        # 2 Maize (Orange)
                '#ffffff',        # 3 Cotton (White)
                '#2ecc71',        # 4 Rice (Green)
                '#9b59b6',        # 5 Sugarcane (Purple)
                '#e74c3c'         # 6 Groundnut (Red)
            ])
            
            # Convert classification array to an RGBA image array
            norm = mcolors.BoundaryNorm(boundaries=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], ncolors=7)
            rgba_image = cmap(norm(classes))
            
            # Make the 'non-crop' class fully transparent
            rgba_image[classes == 0, 3] = 0.0
            
            # Map boundaries format: [[lat_min, lon_min], [lat_max, lon_max]]
            image_bounds = [[bounds.bottom, bounds.left], [bounds.top, bounds.right]]
            
            # Overlay the Image onto the Interactive Map
            folium.raster_layers.ImageOverlay(
                image=rgba_image,
                bounds=image_bounds,
                opacity=0.7,
                name='AI Crop Classification Mask',
                interactive=True
            ).add_to(folium_map)
            
            # Add Layer Control
            folium.LayerControl().add_to(folium_map)
            
            # Automatically center and zoom the map to fit the uploaded farm perfectly
            folium_map.fit_bounds(image_bounds)
            
            # Add a floating Legend to the map UI
            legend_html = '''
             <div style="position: fixed; 
                         bottom: 20px; left: 20px; width: 140px; height: 190px; 
                         background-color: rgba(11, 15, 25, 0.85); border:1px solid #00ff88; 
                         backdrop-filter: blur(5px);
                         z-index:9999; font-size:14px; color: white;
                         padding: 12px; border-radius: 8px; font-family: 'Inter', sans-serif;">
             <b style="color:#00ff88;">Crop Classes</b><br><br>
             <i style="background:#f1c40f; width: 12px; height: 12px; float: left; margin-right: 8px; margin-top: 3px; border-radius:2px;"></i> Wheat<br>
             <i style="background:#e67e22; width: 12px; height: 12px; float: left; margin-right: 8px; margin-top: 3px; border-radius:2px;"></i> Maize<br>
             <i style="background:#ffffff; width: 12px; height: 12px; float: left; margin-right: 8px; margin-top: 3px; border-radius:2px;"></i> Cotton<br>
             <i style="background:#2ecc71; width: 12px; height: 12px; float: left; margin-right: 8px; margin-top: 3px; border-radius:2px;"></i> Rice<br>
             <i style="background:#9b59b6; width: 12px; height: 12px; float: left; margin-right: 8px; margin-top: 3px; border-radius:2px;"></i> Sugarcane<br>
             <i style="background:#e74c3c; width: 12px; height: 12px; float: left; margin-right: 8px; margin-top: 3px; border-radius:2px;"></i> Groundnut<br>
             </div>
             '''
            folium_map.get_root().html.add_child(folium.Element(legend_html))
            
            return True
            
    except Exception as e:
        print(f"Failed to generate pixel map: {e}")
        return False
