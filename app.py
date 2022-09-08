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
Map.add_basemap('OpenStreetMap.HOT')
# Retrieve Earth Engine dataset
dataset = ee.ImageCollection('MODIS/061/MOD13Q1').filter(ee.Filter.date('2018-01-01', '2018-05-01'))
ndvi = dataset.select('NDVI')
# Set visualization parameters
vizParams = {
  min: 0,
  max: 8000,
  "palette": ["006633", "E5FFCC", "662A00", "D8D8D8", "F5F5F5"]
}
# Add the Earth Engine image to the map
Map.addLayer(ndvi, vizParams, "NVDI Layer", True, 0.9)
# Add a colorbar to the map

vis_params = {
    "palette": vizParams['palette'],
    'min': 0,
    'max': 4000,
}

Map.add_colorbar(vis_params, label="NDVI Level 0-4000")
# Render the map using streamlit
Map.to_streamlit()
