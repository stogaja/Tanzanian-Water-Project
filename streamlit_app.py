import functions
import plotly.express as px
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from streamlit_option_menu import option_menu
import pandas as pd
from logging import PlaceHolder
import streamlit as st
import plotly.figure_factory as ff
import numpy as np


# This code is different for each deployed app.
CURRENT_THEME = "light"
IS_DARK_THEME = False
EXPANDER_TEXT = """
    This is Streamlit's default *Light* theme. It should be enabled by default 🎈
    If not, you can enable it in the app menu (☰ -> Settings -> Theme).
    """

# importing the required libraries

# let's read our data
tz = pd.read_csv("data/tz.csv")


@st.cache
def get_data(filename):
    tz_data = pd.read_csv(filename)

    return tz_data


st.markdown("<h1 style='text-align: center;'> Predict Pump Status </h1>",
            unsafe_allow_html=True)

st.text('Input pump details to figure out its status here ')

# creating a navigation bar
selected = option_menu(menu_title=None, options=['Home', 'Analysis', 'Predict Pump Status'], icons=[
                       'house', 'boxes', 'cast'], menu_icon='cast', default_index=0, orientation='horizontal')

if selected == 'Home':
    st.markdown("<h2 style='text-align: center;'>PUMP IT UP</h2>",
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
    #st.subheader('Tanzanian Water Dataset')
    #import streamlit as st


    #st.set_page_config(layout="wide", page_icon='logo.png', page_title='EDA')

    st.header("Pump it Up Exploratory Data Analysis")

    st.write('<p style="font-size:160%">You will be able to✅:</p>',
            unsafe_allow_html=True)

    st.write('<p style="font-size:100%">&nbsp 1. See the whole dataset</p>',
            unsafe_allow_html=True)
    st.write('<p style="font-size:100%">&nbsp 2. Get column names, data types info</p>',
            unsafe_allow_html=True)
    st.write('<p style="font-size:100%">&nbsp 3. Get the count and percentage of NA values</p>',
            unsafe_allow_html=True)
    st.write('<p style="font-size:100%">&nbsp 4. Get descriptive analysis </p>',
            unsafe_allow_html=True)
    st.write('<p style="font-size:100%">&nbsp 5. Check inbalance or distribution of target variable:</p>',
            unsafe_allow_html=True)
    st.write('<p style="font-size:100%">&nbsp 6. See distribution of numerical columns</p>',
            unsafe_allow_html=True)
    st.write('<p style="font-size:100%">&nbsp 7. See count plot of categorical columns</p>',
            unsafe_allow_html=True)
    st.write('<p style="font-size:100%">&nbsp 8. Get outlier analysis with box plots</p>',
            unsafe_allow_html=True)
    st.write('<p style="font-size:100%">&nbsp 9. Obtain info of target value variance with categorical columns</p>', unsafe_allow_html=True)
    #st.image('header2.png', use_column_width = True)

    functions.space()
    st.write('<p style="font-size:130%">Import Dataset</p>', unsafe_allow_html=True)

    file_format = st.radio('Select file format:',
                        ('csv', 'excel'), key='file_format')
    dataset = st.file_uploader(label='')

    use_defo = st.checkbox('Proceed to view analysis')
    if use_defo:
        dataset = 'data/merged_dataset.csv'

    st.sidebar.header('Import Dataset to Use Available Features: 👉')

    if dataset:
        if file_format == 'csv' or use_defo:
            df = pd.read_csv(dataset)
        else:
            df = pd.read_excel(dataset)

        st.subheader('Dataframe:')
        n, m = df.shape
        st.write(
            f'<p style="font-size:130%">Dataset contains {n} rows and {m} columns.</p>', unsafe_allow_html=True)
        st.dataframe(df)

        all_vizuals = ['Info', 'NA Info', 'Descriptive Analysis', 'Target Analysis',
                    'Distribution of Numerical Columns', 'Count Plots of Categorical Columns',
                    'Box Plots', 'Outlier Analysis', 'Variance of Target with Categorical Columns']
        functions.sidebar_space(3)
        vizuals = st.sidebar.multiselect(
            "Choose which visualizations you want to see 👇", all_vizuals)

        if 'Info' in vizuals:
            st.subheader('Info:')
            c1, c2, c3 = st.columns([1, 2, 1])
            c2.dataframe(functions.df_info(df))

        if 'NA Info' in vizuals:
            st.subheader('NA Value Information:')
            if df.isnull().sum().sum() == 0:
                st.write('There is not any NA value in your dataset.')
            else:
                c1, c2, c3 = st.columns([0.5, 2, 0.5])
                c2.dataframe(functions.df_isnull(df), width=1500)
                functions.space(2)

        if 'Descriptive Analysis' in vizuals:
            st.subheader('Descriptive Analysis:')
            st.dataframe(df.describe())

        if 'Target Analysis' in vizuals:
            st.subheader("Select target column:")
            target_column = st.selectbox("", df.columns, index=len(df.columns) - 1)

            st.subheader("Histogram of target column")
            fig = px.histogram(df, x=target_column)
            c1, c2, c3 = st.columns([0.5, 2, 0.5])
            c2.plotly_chart(fig)

        num_columns = df.select_dtypes(exclude='object').columns
        cat_columns = df.select_dtypes(include='object').columns

        if 'Distribution of Numerical Columns' in vizuals:

            if len(num_columns) == 0:
                st.write('There is no numerical columns in the data.')
            else:
                selected_num_cols = functions.sidebar_multiselect_container(
                    'Choose columns for Distribution plots:', num_columns, 'Distribution')
                st.subheader('Distribution of numerical columns')
                i = 0
                while (i < len(selected_num_cols)):
                    c1, c2 = st.columns(2)
                    for j in [c1, c2]:

                        if (i >= len(selected_num_cols)):
                            break

                        fig = px.histogram(df, x=selected_num_cols[i])
                        j.plotly_chart(fig, use_container_width=True)
                        i += 1

        if 'Count Plots of Categorical Columns' in vizuals:

            if len(cat_columns) == 0:
                st.write('There is no categorical columns in the data.')
            else:
                selected_cat_cols = functions.sidebar_multiselect_container(
                    'Choose columns for Count plots:', cat_columns, 'Count')
                st.subheader('Count plots of categorical columns')
                i = 0
                while (i < len(selected_cat_cols)):
                    c1, c2 = st.columns(2)
                    for j in [c1, c2]:

                        if (i >= len(selected_cat_cols)):
                            break

                        fig = px.histogram(
                            df, x=selected_cat_cols[i], color_discrete_sequence=['indianred'])
                        j.plotly_chart(fig)
                        i += 1

        if 'Box Plots' in vizuals:
            if len(num_columns) == 0:
                st.write('There is no numerical columns in the data.')
            else:
                selected_num_cols = functions.sidebar_multiselect_container(
                    'Choose columns for Box plots:', num_columns, 'Box')
                st.subheader('Box plots')
                i = 0
                while (i < len(selected_num_cols)):
                    c1, c2 = st.columns(2)
                    for j in [c1, c2]:

                        if (i >= len(selected_num_cols)):
                            break

                        fig = px.box(df, y=selected_num_cols[i])
                        j.plotly_chart(fig, use_container_width=True)
                        i += 1

        if 'Outlier Analysis' in vizuals:
            st.subheader('Outlier Analysis')
            c1, c2, c3 = st.columns([1, 2, 1])
            c2.dataframe(functions.number_of_outliers(df))

        if 'Variance of Target with Categorical Columns' in vizuals:

            df_1 = df.dropna()

            high_cardi_columns = []
            normal_cardi_columns = []

            for i in cat_columns:
                if (df[i].nunique() > df.shape[0] / 10):
                    high_cardi_columns.append(i)
                else:
                    normal_cardi_columns.append(i)

            if len(normal_cardi_columns) == 0:
                st.write(
                    'There is no categorical columns with normal cardinality in the data.')
            else:

                st.subheader(
                    'Variance of target variable with categorical columns')
                model_type = st.radio(
                    'Select Problem Type:', ('Regression', 'Classification'), key='model_type')
                selected_cat_cols = functions.sidebar_multiselect_container(
                    'Choose columns for Category Colored plots:', normal_cardi_columns, 'Category')

                if 'Target Analysis' not in vizuals:
                    target_column = st.selectbox(
                        "Select target column:", df.columns, index=len(df.columns) - 1)

                i = 0
                while (i < len(selected_cat_cols)):

                    if model_type == 'Regression':
                        fig = px.box(df_1, y=target_column,
                                    color=selected_cat_cols[i])
                    else:
                        fig = px.histogram(
                            df_1, color=selected_cat_cols[i], x=target_column)

                    st.plotly_chart(fig, use_container_width=True)
                    i += 1

                if high_cardi_columns:
                    if len(high_cardi_columns) == 1:
                        st.subheader(
                            'The following column has high cardinality, that is why its boxplot was not plotted:')
                    else:
                        st.subheader(
                            'The following columns have high cardinality, that is why its boxplot was not plotted:')
                    for i in high_cardi_columns:
                        st.write(i)

                    st.write(
                        '<p style="font-size:140%">Do you want to plot anyway?</p>', unsafe_allow_html=True)
                    answer = st.selectbox("", ('No', 'Yes'))

                    if answer == 'Yes':
                        for i in high_cardi_columns:
                            fig = px.box(df_1, y=target_column, color=i)
                            st.plotly_chart(fig, use_container_width=True)

    ###############################################################
    ### ENDS HERE#################################################
    ##############################################################

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
