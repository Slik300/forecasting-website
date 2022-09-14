import os
import json

import pandas as pd
import streamlit as st
import geopandas as gpd
import pyproj
import plotly.graph_objs as go
import numpy as np

def render(country_name, country_code, center):
    st.title(f'{country_name} Crop Yield Prediction')

    county_shp = f'data/shape_files/{country_code}/admin1/{country_code}.shp'

    shape_data = gpd.read_file(county_shp)
    map_df = shape_data

    path = f"{country_name}.json"# write GeoJSON to file
    map_df.to_file(path, driver = "GeoJSON")
    with open(path) as geofile:
        j_file = json.load(geofile)

    # index geojson
    i=1
    for feature in j_file["features"]:
       feature['id'] = str(i).zfill(2)
       i += 1

    predictions = pd.read_pickle(f'data/{country_code}.pkl')

    inv_index = {row['NAME1_'].lower().strip(): i for i, row in map_df.iterrows()}

    zmin = predictions['predictions'].min()
    zmax = predictions['predictions'].max()

    yearly_predictions = {}
    for year, year_group in predictions.groupby('years'):
        pred = np.zeros(len(map_df))
        for i, row in year_group.iterrows():
            pred[inv_index[row['county_names'].lower().strip()]] = row['predictions']
        yearly_predictions[year] = pred

    mapboxt = os.environ.get("MAPBOXTOKEN")

    choropleths = {
        year: go.Choroplethmapbox(z=pred[pred != 0], locations = map_df[pred != 0].index, colorscale = 'Viridis', geojson=j_file, text = map_df['NAME1_'], marker_line_width=0.1, zmin=zmin, zmax=zmax)
        for year, pred in yearly_predictions.items()
    }

    for k, v in choropleths.items():
        v.__dict__['year'] = k

    layer1 = st.select_slider("select year", list(choropleths.values()), format_func=lambda x : str(x.year))

    layout = go.Layout(width=1000, height=1000, mapbox=dict(center=center, accesstoken=mapboxt, zoom=3,style="stamen-terrain"))
    fig = go.Figure(data=layer1, layout=layout)
    st.plotly_chart(fig)
