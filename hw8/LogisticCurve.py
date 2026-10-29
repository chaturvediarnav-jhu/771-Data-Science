# Logistic Curve Tool
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# make X array
x = np.linspace(-10,10,100)
st.title ('Logistic Curve Adjustment Tool')

# make slider objects
b0 = st.slider(
    label="B_0", 
    min_value=-10, 
    max_value=10, 
    value=0, 
    step=1)

b1 = st.slider(
    label="B_1", 
    min_value=-10, 
    max_value=10, 
    value=0, 
    step=1)

# put in equation
fx = np.exp(b0+(b1*x)) / (1+np.exp(b0+(b1*x)))

# make plot
fig = px.line(fx, x=x, y=fx,
             title='Logistic Curve')  

st.plotly_chart(fig)