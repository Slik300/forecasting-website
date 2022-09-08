import streamlit as st

#make streamlit

'''
# Food Security Forecaster
'''
# Import libraries
import ee
import geemap.foliumap as geemap

# Create an interactive map
Map = geemap.Map(plugin_Draw=True, Draw_export=False)
# Add a basemap
Map.add_basemap("TERRAIN")
# Retrieve Earth Engine dataset
dem = ee.Image("USGS/SRTMGL1_003")
# Set visualization parameters
vis_params = {
    "min": 0,
    "max": 4000,
    "palette": ["006633", "E5FFCC", "662A00", "D8D8D8", "F5F5F5"],
}
# Add the Earth Engine image to the map
Map.addLayer(dem, vis_params, "SRTM DEM", True, 0.5)
# Add a colorbar to the map
Map.add_colorbar(vis_params["palette"], 0, 4000, caption="Elevation (m)")
# Render the map using streamlit
Map.to_streamlit()
