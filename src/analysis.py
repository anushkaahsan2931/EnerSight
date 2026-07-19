import pandas as pd
import matplotlib.pyplot as plt

# Load data
train = pd.read_feather("data/train.feather")

# Select electricity only
electricity = train[train["meter"] == 0]

print("Electricity data:")
print(electricity.head())

print("\nNumber of electricity readings:")
print(len(electricity))

# Energy statistics
print("\nElectricity statistics:")
print(electricity["meter_reading"].describe())

# Plot energy distribution
plt.figure(figsize=(10,5))
plt.hist(electricity["meter_reading"], bins=100)

plt.xlabel("Energy Consumption (kWh)")
plt.ylabel("Number of Readings")
plt.title("Electricity Consumption Distribution")

plt.savefig("graphs/energy_distribution.png")
print("Graph saved!")

# Remove extreme outliers for better visualization
normal_energy = electricity[electricity["meter_reading"] < 5000]

plt.figure(figsize=(10,5))

plt.hist(normal_energy["meter_reading"], bins=100)

plt.xlabel("Energy Consumption (kWh)")
plt.ylabel("Number of Readings")
plt.title("Normal Electricity Consumption Distribution")

plt.savefig("graphs/normal_energy_distribution.png")

print("Normal energy graph saved!")
