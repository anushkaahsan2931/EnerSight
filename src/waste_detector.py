import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
train = pd.read_feather("data/train.feather")
building = pd.read_feather("data/building_metadata.feather")
weather = pd.read_feather("data/weather_train.feather")
# Electricity only
electricity = train[train["meter"] == 0]

# Average energy per building
energy = electricity.groupby("building_id")["meter_reading"].mean()

# Add building information
energy = energy.reset_index()

energy = energy.merge(
    building,
    on="building_id",
    how="left"
)

# Energy efficiency metric
energy["energy_per_sqft"] = (
    energy["meter_reading"] / energy["square_feet"]
)

# Rank inefficient buildings
waste_ranking = energy.sort_values(
    "energy_per_sqft",
    ascending=False
)

print("Top 10 inefficient buildings:")
print(
    waste_ranking[
        [
            "building_id",
            "primary_use",
            "square_feet",
            "energy_per_sqft"
        ]
    ].head(10)
)
# Visualize top waste buildings

top10 = waste_ranking.head(10)

plt.figure(figsize=(10,5))

plt.bar(
    top10["building_id"].astype(str),
    top10["energy_per_sqft"]
)

plt.xlabel("Building ID")
plt.ylabel("Energy Consumption per sqft")
plt.title("Top 10 Energy Inefficient Buildings")

plt.xticks(rotation=45)

plt.savefig("graphs/top_waste_buildings.png")

print("Waste ranking graph saved!")

# Convert timestamp
electricity["timestamp"] = pd.to_datetime(electricity["timestamp"])

# Extract hour
electricity["hour"] = electricity["timestamp"].dt.hour

# Define nighttime hours (12 AM - 6 AM)
night_usage = electricity[
    (electricity["hour"] >= 0) &
    (electricity["hour"] <= 6)
]

# Average nighttime energy by building
night_waste = (
    night_usage
    .groupby("building_id")["meter_reading"]
    .mean()
    .sort_values(ascending=False)
)

print("\nTop buildings with high nighttime energy usage:")
print(night_waste.head(10))
# Combine waste indicators

# Get average nighttime usage per building
night_waste_df = night_waste.reset_index()
night_waste_df.columns = [
    "building_id",
    "night_energy"
]



# Merge with efficiency data
final_score = energy.merge(
    night_waste_df,
    on="building_id",
    how="left"
)

# Fill missing nighttime values
final_score["night_energy"] = (
    final_score["night_energy"]
    .fillna(0)
)

# Normalize scores from 0-100
final_score["energy_score"] = (
    final_score["energy_per_sqft"] /
    final_score["energy_per_sqft"].max()
) * 100

final_score["night_score"] = (
    final_score["night_energy"] /
    final_score["night_energy"].max()
) * 100


# Final waste score
final_score["waste_score"] = (
    0.6 * final_score["energy_score"] +
    0.4 * final_score["night_score"]
)


# Rank buildings
final_score = final_score.sort_values(
    "waste_score",
    ascending=False
)


print("\nEnerSight Waste Score Ranking:")
print(
    final_score[
        [
            "building_id",
            "primary_use",
            "energy_per_sqft",
            "night_energy",
            "waste_score"
        ]
    ].head(10))
# Save results

final_score.to_csv(
    "reports/waste_scores.csv",
    index=False
)

print("\nWaste scores saved!")


# Analyze weather impact

weather["timestamp"] = pd.to_datetime(weather["timestamp"])

weather_summary = weather.groupby("timestamp")[
    "air_temperature"
].mean()

print("\nAverage temperature range:")
print(weather_summary.describe())