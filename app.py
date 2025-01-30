import streamlit as st
import pandas as pd
import numpy as np
import kagglehub
import os

# Streamlit Dashboard
st.title("USGS Stream Health Dashboard")

# Download dataset
url = "https://www.kaggle.com/datasets/protobioengineering/usgs-streamgages-all-50-states"
st.write("Using Dataset [Unite States Gauge Streams](%s) from Kaggle" % url, "        |             App Version:", 1.00)
path = kagglehub.dataset_download("protobioengineering/usgs-streamgages-all-50-states")

# Load dataset
csv_files = [file for file in os.listdir(path) if file.endswith(".csv")]
df_list = []
for file in csv_files:
    df_list.append(pd.read_csv(os.path.join(path, file)))
df = pd.concat(df_list, ignore_index=True)
st.sidebar.success("Dataset loaded successfully!")

# Data Preprocessing
st.sidebar.header("Filter Data")
county_filter = st.sidebar.multiselect("Select Counties", df["county"].unique())
if county_filter:
    df = df[df["county"].isin(county_filter)]

# Key Metrics
st.write("### Overview of Stream Health Indicators")
st.write("**Average Drainage Area:**", f"{round(df['drainage_area'].mean(), 2)} sq mi")
st.write("**Average Datum of Gage:**", f"{round(df['datum_of_gage'].mean(), 2)} ft")
st.write("**Total Unique Hydrologic Units:**", df['hydrologic_unit'].nunique())
st.write("**Total Streamgages Monitored:**", df['location_id'].nunique())

# Visualizations using Streamlit
st.write("### Distribution of Streamgage Attributes")
st.bar_chart(df["drainage_area"], use_container_width=True)
st.bar_chart(df["datum_of_gage"], use_container_width=True)

# Stream Health Analysis
st.write("### Stream Health Report")
def health_rating(datum):
    if datum >= df["datum_of_gage"].quantile(0.75):
        return "🟢 Very Healthy"
    elif datum >= df["datum_of_gage"].median():
        return "🟡 Moderately Healthy"
    elif datum >= df["datum_of_gage"].quantile(0.25):
        return "🟠 At Risk"
    else:
        return "🔴 Critically Unhealthy"

df["health_status"] = df["datum_of_gage"].apply(health_rating)

def color_code(status):
    return {"🟢 Very Healthy": "#00FF00", "🟡 Moderately Healthy": "#FFFF00", "🟠 At Risk": "#FFA500", "🔴 Critically Unhealthy": "#FF0000"}[status]

# Group health status by county with expanders
st.write("### Stream Health by County")
for county in df["county"].unique():
    county_df = df[df["county"] == county].sort_values(by="health_status", ascending=True)
    with st.expander(f"{county} County (Click to Expand)"):
        tabs = st.tabs(["Healthy Streams", "Moderate Streams", "At-Risk Streams", "Critical Streams"])
        for index, row in county_df.iterrows():
            health_category = row["health_status"]
            if health_category == "🟢 Very Healthy":
                with tabs[0]:
                    st.markdown(f'<div style="background-color:{color_code(health_category)}; padding:10px; margin:5px; border-radius:5px;">' \
                                f'<b>{row["name"]}</b>: {health_category}</div>', 
                                unsafe_allow_html=True)
            elif health_category == "🟡 Moderately Healthy":
                with tabs[1]:
                    st.markdown(f'<div style="background-color:{color_code(health_category)}; padding:10px; margin:5px; border-radius:5px;">' \
                                f'<b>{row["name"]}</b>: {health_category}</div>', 
                                unsafe_allow_html=True)
            elif health_category == "🟠 At Risk":
                with tabs[2]:
                    st.markdown(f'<div style="background-color:{color_code(health_category)}; padding:10px; margin:5px; border-radius:5px;">' \
                                f'<b>{row["name"]}</b>: {health_category}</div>', 
                                unsafe_allow_html=True)
            elif health_category == "🔴 Critically Unhealthy":
                with tabs[3]:
                    st.markdown(f'<div style="background-color:{color_code(health_category)}; padding:10px; margin:5px; border-radius:5px;">' \
                                f'<b>{row["name"]}</b>: {health_category}</div>', 
                                unsafe_allow_html=True)

# Recommended Actions
st.write("### Suggested Actions for At-Risk Streams")
attention_df = df[df["health_status"].isin(["🟠 At Risk", "🔴 Critically Unhealthy"])]
if not attention_df.empty:
    st.write("- Investigate low datum of gage levels to ensure stability against extreme water events.")
    st.write("- Improve drainage management to ensure healthy watershed function.")
    st.write("- Monitor hydrologic units for changes that may affect water quality.")
else:
    st.write("All monitored streams are within stable levels! ✅")


