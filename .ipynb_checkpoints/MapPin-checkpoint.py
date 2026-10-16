# Map Pin App
import streamlit as st
import pandas as pd
import numpy as np
st.title ('Find Location by Latitude and Longitude')

lat = st.number_input("Enter Latitude (for N use positive value and for S use negative value)", min_value=-90.0, max_value=90.0)
long = st.number_input("Enter Longitude (for E use positive value and for W use negative value)", min_value=-180.0, max_value=180.0,)

with st.form(key = "Location", enter_to_submit=True):
    submitted = st.form_submit_button("Show me the map")
    if submitted:
        df = pd.DataFrame({"lat": [lat], "lon":[long]})
        st.map(df, size=100, zoom=10)