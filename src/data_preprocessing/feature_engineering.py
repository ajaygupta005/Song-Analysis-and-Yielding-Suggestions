from pyspark.sql.functions import col, monotonically_increasing_id
from src.utils.spark_session import get_spark

def run_feature_engineering(raw_path, processed_path):
    spark = get_spark()
    
    # --- 1. Process Real Track Data (data.csv) ---
    tracks_raw = spark.read.csv(f"{raw_path}/data.csv", header=True, inferSchema=True)

    # Assign a unique, sequential track_id. 
    # This ID will be used for the relational join with interactions.
    # Note: We cast to Integer type, which is safer for ALS.
    tracks_df = tracks_raw.withColumn("track_id", 
                                      monotonically_increasing_id().cast("integer"))
    
    print(f"Real track data processed. Total unique tracks: {tracks_df.count()}")

    # --- 2. Load Synthetic Data ---
    users = spark.read.csv(f"{raw_path}/users.csv", header=True, inferSchema=True)
    # The interactions table holds the synthetic user-track-rating data.
    interactions_raw = spark.read.csv(f"{raw_path}/user_track_interactions.csv", header=True, inferSchema=True)

    # --- 3. Join and Prepare ALS Training Data ---
    
    # The key is to map the synthetic interactions (which reference generic IDs) 
    # to the newly created unique IDs from the real track data.
    # We will join on the 'track_id' column, assuming the synthetic IDs fall within the range of real track IDs.
    
    # Select only user_id and rating from the synthetic interactions
    interactions_prepped = interactions_raw.select(col("user_id"), col("track_id").alias("synthetic_track_id"), col("rating"))
    
    # Join interactions with the real track data to ensure we only keep interactions 
    # that map to a song in the real data. We join on the synthetic ID.
    df_joined = interactions_prepped.join(
        tracks_df.select(col("track_id").alias("final_track_id"), col("track_id").alias("synthetic_track_id_map")), 
        col("synthetic_track_id") == col("synthetic_track_id_map"), 
        "inner"
    )

    # Final DF for ALS training (User ID, Final Track ID, Rating)
    df_training = df_joined.select(
        col("user_id").cast("integer"),
        col("final_track_id").alias("track_id").cast("integer"),
        col("rating").cast("float")
    )
    
    # Save the final dataset ready for ALS training
    df_training.write.mode("overwrite").parquet(f"{processed_path}/training_data")

    print(f"Feature engineering completed. Training interactions: {df_training.count()}.")