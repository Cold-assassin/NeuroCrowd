import numpy as np
import pandas as pd

# Number of random LiDAR points to generate
NUM_POINTS = 5000  

# Generate random X, Y, Z coordinates
x = np.random.uniform(-50, 50, NUM_POINTS)  # X range (-50m to 50m)
y = np.random.uniform(-50, 50, NUM_POINTS)  # Y range (-50m to 50m)
z = np.random.uniform(0, 10, NUM_POINTS)    # Height (0m to 10m)

# Combine into a NumPy array
points = np.column_stack((x, y, z))

# Save as CSV file
df = pd.DataFrame(points, columns=["x", "y", "z"])
df.to_csv("simple_lidar_data.csv", index=False)

print("✅ LiDAR data saved as CSV: simple_lidar_data.csv")
