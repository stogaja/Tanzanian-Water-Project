
# importing the required libraries
from logging import PlaceHolder
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# let's read our data
tz = pd.read_csv("data/tz.csv")

# let's declare our containers
header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

@st.cache
def get_data(filename):
    tz_data = pd.read_csv(filename)

    return tz_data

    # st.write(tz.head())

    # st.subheader('Current Pump Status Distribution')
    # tz_1 = get_data('merged_dataset.csv')
    # source_dist = pd.DataFrame(tz_1['status_group'].value_counts()).head(50)
    # st.bar_chart(source_dist)


st.header('Predict Pump Status!')
st.text('Input pump details to figure out its status here ')

# creating a navigation bar
selected = option_menu(menu_title=None, options=['Home', 'Analysis', 'Predict Pump Status'], icons=[
                       'house', 'boxes', 'cast'], menu_icon='cast', default_index=0, orientation='horizontal')

if selected == 'Home':
    st.markdown("<h2 style='text-align: center; color: black;'>PUMP IT UP</h2>",
                unsafe_allow_html=True)
    st.subheader("Data Mining the Water Table")
    st.text('We are Providing Information About The State Of Pumps In The Tanzania Water System')

    st.subheader('Tanzanian Water Dataset')
    st.text("""
	Pumps in the dataset were distributed in the following nature:

	Functional Pumps           -> 32259
	Non functional Pumps       -> 22824
	Functional needs repair    ->  4317
	""")

    st.subheader('Current Pump Status Distribution')
    tz_1 = get_data('data/merged_dataset.csv')
    source_dist = pd.DataFrame(tz_1['status_group'].value_counts()).head(50)
    st.bar_chart(source_dist)

if selected == 'Analysis':
    st.subheader('Tanzanian Water Dataset')

if selected == 'Predict Pump Status':
    # let's create a form to input the data
    with st.form("my_form1", clear_on_submit=True):
        st.write("Inside the form")
        water = st.text_input(
            "Enter the water level", placeholder="Enter water level as either empty, half or full.")
        # water_point_type = st.text_input("Enter the water point type")
        age = st.number_input("Enter the age of the pump (Years)")
        amount_allocated = st.number_input(
            "Enter the amount allocated to the water point (Tanzanian shillings)")

        submit = st.form_submit_button("Submit")

        if submit == True:
            # or water != "half" or water != "empty" or water != "full"
            if water == "" or age < 0 or age > 30 or amount_allocated < 0:
                st.error('Please enter the correct values for the spaces given')
            else:
                if water == "empty" and age > 10 and amount_allocated <= 1000:
                    st.error('The pump is broken')
                elif water == "full" or "half" and age < 10 and amount_allocated > 1000:
                    st.success('The pump is working normally')
                elif water == "half" and age > 10 and amount_allocated > 1000:
                    st.warning("The pump needs some maintenance")
