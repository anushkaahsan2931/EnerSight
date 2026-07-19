import streamlit as st
import pandas as pd
from PIL import Image


st.set_page_config(
    page_title="EnerSight",
    page_icon="⚡",
    layout="wide"
)


# Load data FIRST
waste = pd.read_csv(
    "reports/waste_scores.csv"
)
train = pd.read_feather(
    "data/train.feather"
)


# Logo + title
logo = Image.open("assets/logo.png")

col1, col2 = st.columns([0.7, 4])

with col1:
    st.image(
        logo,
        width=120
    )

with col2:
    st.title("EnerSight")
    st.caption("AI-Powered Energy Intelligence for Smarter Buildings")


# Dashboard metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Buildings Analyzed",
        len(waste)
    )

with col2:
    st.metric(
        "Highest Waste Score",
        round(waste["waste_score"].max(), 2)
    )

with col3:
    st.metric(
        "Average Waste Score",
        round(waste["waste_score"].mean(), 2)
    )
# Waste Ranking Table

st.divider()

st.header("Top Energy Waste Buildings")

st.dataframe(
    waste.head(10),
    use_container_width=True
)

# Building search

st.divider()

st.header("Building Analysis")

selected_building = st.selectbox(
    "Select a Building ID",
    waste["building_id"].unique()
)

building_data = waste[
    waste["building_id"] == selected_building
]
# Energy trend for selected building

building_energy = train[
    train["building_id"] == selected_building
]

building_energy["timestamp"] = pd.to_datetime(
    building_energy["timestamp"]
)

daily_energy = (
    building_energy
    .groupby("timestamp")["meter_reading"]
    .mean()
)


st.subheader(
    "Energy Consumption Over Time"
)

st.line_chart(
    daily_energy
)

st.subheader(
    f"Building {selected_building} Details"
)

st.dataframe(
    building_data,
    use_container_width=True
)
# Recommendations

st.subheader("EnerSight Recommendations")


score = building_data["waste_score"].values[0]
night = building_data["night_energy"].values[0]


if score > 60:
    st.warning(
        "High energy waste detected. "
        "Consider HVAC optimization, equipment scheduling, "
        "and building system inspection."
    )

elif score > 40:
    st.info(
        "Moderate energy inefficiency detected. "
        "Review energy usage patterns and operational schedules."
    )

else:
    st.success(
        "Energy usage appears efficient compared with other buildings."
    )


if night > building_data["night_energy"].mean():
    st.warning(
        "High nighttime energy consumption detected. "
        "Check unnecessary equipment operation outside working hours."
    )
# Waste Score Chart

st.header("Waste Score Distribution")

st.bar_chart(
    waste.head(10)
    .set_index("building_id")["waste_score"]
)


# Completion message

st.success(
    "EnerSight analysis complete!"
)