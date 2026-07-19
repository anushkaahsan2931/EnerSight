import pandas as pd

# Load original dataset
train = pd.read_feather("data/train.feather")

# Keep only a small sample for deployment
demo = train.sample(100000, random_state=42)

# Save lightweight version
demo.to_feather("data/demo_train.feather")

print("Demo dataset created!")