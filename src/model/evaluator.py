from src.utils.spark_session import get_spark
from pyspark.ml.recommendation import ALSModel
from pyspark.ml.evaluation import RegressionEvaluator

# Use relative path to the processed Parquet data
PROCESSED_PATH = "data/processed"
MODEL_PATH = "models/als_model" # Corrected path to match pipeline

def run():
    print("Starting Spark session...")
    spark = get_spark() # Use the utility function

    print("Loading interactions and ALS model...")
    # Read the data saved by feature_engineering.py
    df_spark = spark.read.parquet(f"{PROCESSED_PATH}/training_data") 
    
    # Check if the model exists before trying to load it
    try:
        model = ALSModel.load(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model from {MODEL_PATH}: {e}")
        print("Please ensure the pipeline has run and trained the model.")
        return

    print("Making predictions...")
    predictions = model.transform(df_spark)

    evaluator = RegressionEvaluator(
        metricName="rmse",
        labelCol="rating", # CORRECTED: Changed 'play_count' to 'rating'
        predictionCol="prediction"
    )
    rmse = evaluator.evaluate(predictions)
    print(f"Model RMSE: {rmse:.4f}")

    spark.stop()

if __name__ == "__main__":
    run()