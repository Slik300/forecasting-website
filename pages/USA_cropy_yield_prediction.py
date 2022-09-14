import streamlit as st
from Crop.py import Crop
from Crop import CROPS
'''
# Crop Yield United States of America
'''

state = st.selectbox("Select a state", CROPS).strip()
