import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

print("Loading data...")

# Load datasets
train = pd.read_feather("data/train.feather")
building = pd.read_feather("data/building_metadata.feather")

# Keep electricity only
train = train[train["meter"] == 0]

# Merge building information
data = train.merge(building, on="building_id")

# Keep only useful columns
data = data[["square_feet", "meter_reading"]].dropna()

# Use a smaller sample for faster training
data = data.sample(n=100000, random_state=42)

print("Sample loaded:", len(data), "rows")

# Features and target
X = data[["square_feet"]]
y = data["meter_reading"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training model...")

# Train model
model = RandomForestRegressor(
    n_estimators=50,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Making predictions...")

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

print("\nMean Absolute Error:", round(mae, 2))

# Compare actual vs predicted
results = X_test.copy()
results["Actual"] = y_test.values
results["Predicted"] = predictions
results["Difference"] = results["Actual"] - results["Predicted"]

# Biggest unexpected energy usage
results = results.sort_values("Difference", ascending=False)

print("\nTop 10 Possible Energy Waste Cases:")
print(results.head(10))

# Save results
results.to_csv("reports/predictions.csv", index=False)

print("\nPredictions saved to reports/predictions.csv")