import pandas as pd

# Load datasets
train = pd.read_feather("data/train.feather")
building = pd.read_feather("data/building_metadata.feather")
weather = pd.read_feather("data/weather_train.feather")
print("Train data:")
print(train.head())

print("\nBuilding data:")
print(building.head())

print("\nWeather data:")
print(weather.head())