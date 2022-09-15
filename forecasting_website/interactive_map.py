import os
import json

import pandas as pd
import streamlit as st
import geopandas as gpd
import pyproj
import plotly.graph_objs as go
#from plotly.subplots import make_subplot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_agg import RendererAgg

@st.experimental_memo
def load_yields(country_name, country_code, true_yield_file):
    predictions = pd.read_pickle(f'data/{country_code}.pkl')
    true = pd.read_csv(f'data/{true_yield_file}.csv')
    predictions_states = predictions['county_names'].str.lower().str.strip()
    true_states = true['STATE'].str.lower().str.strip()
    all_states = set(predictions_states.drop_duplicates()) & set(true_states.drop_duplicates())
    predictions = predictions[predictions_states.apply(lambda s: s in all_states)]
    true = true[true_states.apply(lambda s: s in all_states)]
    zmin = predictions['predictions'].min()
    zmax = predictions['predictions'].max()
    return {
        'predictions': predictions,
        'true': true,
        'zmin': zmin,
        'zmax': zmax,
    }

@st.experimental_memo
def load_geo(county_shp_path):

    shape_data = gpd.read_file(county_shp_path)
    map_df = shape_data

    path = f"tmp.json" # write GeoJSON to file
    map_df.to_file(path, driver = "GeoJSON")
    with open(path) as geofile:
        j_file = json.load(geofile)
    # index geojson
    i=1
    for feature in j_file["features"]:
       feature['id'] = str(i).zfill(2)
       i += 1
    return {'map_df': map_df, 'geojson': j_file}

def build_choropleths(yearly_yields, map_df, geojson, zmin, zmax):
    return {
        year: go.Choroplethmapbox(z=yields[yields != 0], locations = map_df[yields != 0].index, colorscale = 'Viridis', geojson=geojson, text = map_df['NAME1_'], marker_line_width=0.1, zmin=zmin, zmax=zmax)
        for year, yields in yearly_yields.items()
    }

def render(country_name, country_code, true_yield_file, center):

    st.set_page_config(layout="wide")
    _lock = RendererAgg.lock
    yield_data = load_yields(country_name, country_code, true_yield_file)

    county_shp = f'data/shape_files/{country_code}/admin1/{country_code.lower()}.shp'

    geo = load_geo(county_shp)

    map_df = geo['map_df']
    geojson = geo['geojson']

    zmin = yield_data['zmin']
    zmax = yield_data['zmax']
    predictions = yield_data['predictions']
    true = yield_data['true']

    inv_index = {row['NAME1_'].lower().strip(): i for i, row in map_df.iterrows()}

    yearly_predictions = {}
    for year, year_group in predictions.groupby('years'):
        pred = np.zeros(len(map_df))
        for i, row in year_group.iterrows():
            pred[inv_index[row['county_names'].lower().strip()]] = row['predictions']
        yearly_predictions[year] = pred

    mapboxt = os.environ.get("MAPBOXTOKEN")

    col1, col2 = st.columns(2)

    average_predictions = predictions.groupby('years').mean().reset_index()

    average_true = true.groupby('YEAR').mean().reset_index()

    st.title(f'{country_name} Crop Yield Prediction')
    st.write("")
    with col1:
        st.subheader("Prediction Map")
        choropleths = build_choropleths(yearly_predictions, map_df, geojson, zmin, zmax)
        year_select = st.select_slider("select year", choropleths.keys())
        layout = go.Layout(width=1000, height=1000, mapbox=dict(center=center, accesstoken=mapboxt, zoom=3,style="stamen-terrain"))
        #fig = make_subplots(rows=1, cols=2)
        #fig.add_trace(

        #)
        fig = go.Figure(data=choropleths[year_select], layout=layout)
        st.plotly_chart(fig)

    with col2, _lock:
        st.subheader("Prediction Timeseries")
        fig = plt.figure()
        state_select = st.selectbox("select state to view data for each year", options=predictions['county_names'].drop_duplicates()).lower().strip()
        ax = fig.add_subplot(1,1,1)

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        state_predictions = predictions[predictions['county_names'].str.lower().str.strip() == state_select]
        state_true = true[true['STATE'].str.lower().str.strip() == state_select]
        ax.scatter(
            state_predictions['years'], state_predictions['predictions'], color='red', label='predicted yield', alpha=0.6
        )
        ax.scatter(
            state_true['YEAR'], state_true['YIELD'], color='green', label='real yield', alpha=0.6
        )
        ax.scatter(
            average_predictions['years'], average_predictions['predictions'], color='red', label='predicted yield (mean)', alpha=0.2
        )
        ax.scatter(
            average_true['YEAR'], average_true['YIELD'], color='green', label='real yield (mean)', alpha=0.2
        )

        ax.legend(loc='upper left', prop={'size': 6})

        st.write(fig)
