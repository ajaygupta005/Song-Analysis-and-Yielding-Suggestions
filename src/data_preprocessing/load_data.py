import pandas as pd
import os

# Use relative paths consistent with the Docker container
RAW_DATA_PATH = "data/raw/data.csv"
PROCESSED_TRACKS_PATH = "data/processed/tracks_clean.csv"

def run():
    print("Loading raw dataset...")
    
    if not os.path.exists(RAW_DATA_PATH):
        print(f"Error: Raw data file not found at {RAW_DATA_PATH}")
        return

    df = pd.read_csv(RAW_DATA_PATH)

    print("Cleaning dataset...")
    # Drop duplicates (based on all columns for audio features)
    df.drop_duplicates(inplace=True)
    
    # Add a temporary track_id for local Pandas use
    if 'track_id' not in df.columns:
        df.insert(0, 'track_id', range(1, len(df) + 1))

    print(f"Saving cleaned tracks to {PROCESSED_TRACKS_PATH}")
    os.makedirs(os.path.dirname(PROCESSED_TRACKS_PATH), exist_ok=True)
    df.to_csv(PROCESSED_TRACKS_PATH, index=False)
    print("Done.")

if __name__ == "__main__":
    run()