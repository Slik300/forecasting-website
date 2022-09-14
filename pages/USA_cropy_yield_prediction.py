import streamlit as st
import pandas as pd
import numpy as np
from data.Crop import CROPS
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import RendererAgg
#Set page layout to wide
st.set_page_config(layout="wide")
#Allow sections of page to lock
_lock = RendererAgg.lock
#Set layout
sns.set_style("darkgrid")
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)
#Main page title
row0_1.title("Crop Yield United States of America")

with row0_2:
    st.write("")
# Parallel Sub-heading
row0_2.subheader(
    "Use this page to explore both the actual and predicted yields for various crops in the USA"
)
#Selection Box
state = st.selectbox("Select a crop", CROPS).strip()

st.write("")
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row3_1, _lock:
    st.subheader("Actual Yield")
        year_df = pd.DataFrame(df["read_at_year"].dropna().value_counts()).reset_index()
        year_df = year_df.sort_values(by="index")
        fig = Figure()
        ax = fig.subplots()
        sns.barplot(
            x=year_df["index"], y=year_df["read_at_year"], color="goldenrod", ax=ax
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Books Read")
        st.pyplot(fig)


with row3_2, _lock:
    st.subheader("Predicted Yield")
