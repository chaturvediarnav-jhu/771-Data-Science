# BMI Calculator App
import streamlit as st
import pandas as pd
import numpy as np
st.title ('BMI Calculator')

wt = st.number_input("Enter your weight")
wtunit = st.selectbox(
    label = "What units are you using for weight",
    options = ["lbs" , "kg"])

ht = st.number_input("Enter your height")
htunit = st.selectbox(
    label = "What units are you using for height",
    options = ["ft" , "m"])

with st.form(key = "BMI", enter_to_submit=True):
    submitted = st.form_submit_button("What is my BMI?")
    if submitted:
        weight=float(wt)
        height=float(ht)

        # convert everything to metric for simplicity 
        if wtunit == "lbs":
            weight = weight * 0.453592
        if htunit == "ft":
            height = height * 0.3048

        BMIval = weight / (height**2)
        st.write(f"Your BMI is {BMIval:.1f}")