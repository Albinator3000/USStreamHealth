import streamlit as st
import pandas as pd
import kagglehub
import os

# Streamlit UI
st.title("USGS Streamgages Data Viewer")

# Download dataset manually from KaggleHub (Ensure kagglehub is installed)
st.write("Fetching dataset from Kaggle...")

try:
    path = kagglehub.dataset_download("protobioengineering/usgs-streamgages-all-50-states")
    st.success("Dataset successfully downloaded!")
except Exception as e:
    st.error(f"Error downloading dataset: {e}")

# Verify dataset path
if path and os.path.exists(path):
    dataset_files = os.listdir(path)
    st.write("Dataset files available:", dataset_files)
    
    # Load the first CSV file (assuming it's the main data file)
    csv_files = [file for file in dataset_files if file.endswith(".csv")]
    
    if csv_files:
        selected_file = st.selectbox("Select a dataset file to load", csv_files)
        data_file = os.path.join(path, selected_file)
        
        # Load data into Pandas
        df = pd.read_csv(data_file)
        st.write("### Dataset Preview")
        st.dataframe(df.head())

        # Show basic statistics
        st.write("### Basic Statistics")
        st.write(df.describe())

        # Select a column to visualize
        column = st.selectbox("Select a column to visualize", df.columns)
        if column:
            st.write(f"### Histogram of {column}")
            st.bar_chart(df[column].value_counts())
    else:
        st.write("No CSV files found in the dataset.")
else:
    st.error("Failed to locate dataset directory.")



