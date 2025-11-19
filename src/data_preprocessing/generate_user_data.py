import pandas as pd
import numpy as np
import os

def generate_user_data(output_path):

    os.makedirs(output_path, exist_ok=True)

    users = pd.DataFrame({
        "user_id": np.arange(1, 501),
        "age": np.random.randint(18, 60, 500),
        "country": np.random.choice(["India", "USA", "UK"], 500)
    })

    tracks = pd.DataFrame({
        "track_id": np.arange(1, 301),
        "genre": np.random.choice(["Pop", "Rock", "HipHop", "Jazz"], 300)
    })

    interactions = pd.DataFrame({
        "user_id": np.random.choice(users["user_id"], 5000),
        "track_id": np.random.choice(tracks["track_id"], 5000),
        "rating": np.random.randint(1, 6, 5000)
    })

    users.to_csv(f"{output_path}/users.csv", index=False)
    tracks.to_csv(f"{output_path}/tracks.csv", index=False)
    interactions.to_csv(f"{output_path}/user_track_interactions.csv", index=False)

    print("Synthetic data generated successfully!")
