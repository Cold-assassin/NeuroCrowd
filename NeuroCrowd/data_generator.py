import numpy as np

def generate_static_lidar_data(num_points=1000, num_people=10, area_size=50):
    """
    Generates a static LiDAR dataset.
    - num_people: Number of people to simulate.
    - num_points: Total LiDAR points (including ground & noise).
    """
    x = np.random.uniform(-area_size, area_size, num_points)
    y = np.random.uniform(-area_size, area_size, num_points)
    z = np.random.uniform(0, 1, num_points)  # Ground & low obstacles

    # Generate people as vertical clusters
    person_points = []
    for _ in range(num_people):
        px, py = np.random.uniform(-area_size, area_size, 1), np.random.uniform(-area_size, area_size, 1)
        pz = np.linspace(0, 1.7, 10)  # Simulating human height
        for zz in pz:
            person_points.append([px[0], py[0], zz])

    person_points = np.array(person_points)
    all_points = np.vstack((np.column_stack((x, y, z)), person_points))

    # Save the dataset
    np.save("lidar_data.npy", all_points)
    print("Static LiDAR dataset saved as 'lidar_data.npy'.")

# Run this to generate the dataset
generate_static_lidar_data()
