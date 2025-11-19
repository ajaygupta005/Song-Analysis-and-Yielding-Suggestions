import os
from src.data_preprocessing.generate_user_data import generate_user_data
from src.data_preprocessing.feature_engineering import run_feature_engineering
from src.model.als_trainer import train_als
# The recommender call is now handled by the Streamlit app.

# Define paths relative to the project root /app
RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"
MODEL_PATH = "models/als_model"

def run_pipeline(force_run=False):
    """Runs the full data engineering and ML pipeline."""
    
    if os.path.exists(MODEL_PATH) and not force_run:
        print("Pipeline skipped: Model already exists. Use force_run=True to retrain.")
        return

    # Ensure directories exist
    os.makedirs(RAW_PATH, exist_ok=True) 
    os.makedirs(PROCESSED_PATH, exist_ok=True)
    os.makedirs("models", exist_ok=True)
    
    # IMPORTANT: Assumes your real data.csv is already in data/raw!
    
    print("--- 1. Generating Synthetic User/Interaction Data ---")
    generate_user_data(RAW_PATH)
    
    print("--- 2. Running Feature Engineering & Data Integration (Spark) ---")
    run_feature_engineering(RAW_PATH, PROCESSED_PATH)
    
    print("--- 3. Training ALS Model (Spark) ---")
    train_als(PROCESSED_PATH, MODEL_PATH)
    
    print("Pipeline execution complete.")

if __name__ == "__main__":
    run_pipeline()