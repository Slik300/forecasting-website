import streamlit as st

st.set_page_config(layout="wide")

'''
# Food Security Forecaster
'''
# Import libraries

import ee
import geemap.foliumap as geemap

# Create an interactive map
Map = geemap.Map(plugin_Draw=True, Draw_export=False)
# Add Gif to Map
#Map.add_landsat_ts_gif(label='USA', start_year=2018, bands=['NIR', 'Red', 'Green'], frames_per_second=10)
# Add Map Centre (Focus on Area)
Map.setCenter(-95.7129, 37.0902, 3)
# Add a basemap
Map.add_basemap('NASAGIBS.ASTER_GDEM_Greyscale_Shaded_Relief')  #'OpenStreetMap.HOT'
# Retrieve Earth Engine dataset
dataset = ee.ImageCollection('MODIS/061/MOD13Q1').filter(ee.Filter.date('2000-01-01', '2018-05-01'))
ndvi = dataset.select('NDVI')
# Set visualization parameters
vizParams = {
  min: 0,
  max: 8000,
  "palette": ['FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
    '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
    '012E01', '011D01', '011301']
}
# Add the Earth Engine image to the map
Map.addLayer(ndvi, vizParams, "NVDI Layer", True, 0.6)
# Add a colorbar to the map
Map.add_colorbar(vizParams, label="NDVI Level 0-8000")
# Render the map using streamlit
Map.to_streamlit()
