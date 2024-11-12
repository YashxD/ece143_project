import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [32.8812, -117.2344],
    columns=["lat", "lon"],
)
st.map(df, size=3)

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)