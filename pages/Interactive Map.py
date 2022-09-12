import pandas as pd
import streamlit as st

from data.Information import STATES

import ee
import geemap
from ee import ImageCollection


st.title('Food Security Forecast Explorer')
st.write('''
        ### Select a Geography
        Identify which County you are interested in exploring.
        ''')


state = st.selectbox("Select a state", STATES).strip()

ee.Initialize()
Map = geemap.Map()

county_shp = 'data/ee_shape/gadm41_IND_1.shp'

ee_shape = geemap.shp_to_ee(county_shp)

county = ee_shape.filter(ee.Filter.eq("NAME_1,C,22", state))

Map.addLayer(county.geometry())
Map
