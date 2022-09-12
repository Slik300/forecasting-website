import pandas as pd
import streamlit as st

from data.Information import STATES

import ee
from ee import ImageCollection
import geemap.foliumap as geemap

# Create an interactive map
Map = geemap.Map(plugin_Draw=True, Draw_export=False)

st.title('Food Security Forecast Explorer')
st.write('''
        ### Select a which County you are interested in exploring.
        ''')


state = st.selectbox("Select a state", STATES).strip()

ee.Initialize()
Map = geemap.Map()

county_shp = 'data/ee_shape/admin1/ind.shp'

ee_shape = geemap.shp_to_ee(county_shp)
county = ee_shape.filter(ee.Filter.eq("NAME1_", state))

Map.setCenter(78.9629, 20.5937, 5)
Map.addLayer(county)
Map.to_streamlit()
