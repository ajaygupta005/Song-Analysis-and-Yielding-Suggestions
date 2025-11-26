import logging
from pyspark.sql.functions import col, count, avg, min as spark_min, max as spark_max
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType
from src.utils.spark_session import get_spark

logger = logging.getLogger(__name__)

class FeatureEngineer:
    def __init__(self, spark_session):
        self.spark = spark_session
        
    def load_interactions(self, processed_path):
        schema = StructType([
            StructField("user_id", IntegerType(), True),
            StructField("track_id", IntegerType(), True),
            StructField("rating", FloatType(), True)
        ])
        
        interactions = self.spark.read.csv(
            f"{processed_path}/user_track_interactions.csv", 
            header=True, 
            schema=schema
        )
        
        logger.info(f"Loaded {interactions.count()} interactions")
        return interactions
        
    def transform_data(self, interactions_df):
        training_df = interactions_df.select(
            col("user_id").cast("integer"),
            col("track_id").cast("integer"),
            col("rating").cast("float")
        )
        
        training_df = training_df.dropna()
        
        return training_df
        
    def validate_and_log_stats(self, df):
        stats = df.agg(
            count("*").alias("total_interactions"),
            avg("rating").alias("avg_rating"),
            spark_min("rating").alias("min_rating"),
            spark_max("rating").alias("max_rating")
        ).collect()[0]
        
        logger.info(f"Training set statistics:")
        logger.info(f"  Total interactions: {stats['total_interactions']}")
        logger.info(f"  Unique users: {df.select('user_id').distinct().count()}")
        logger.info(f"  Unique tracks: {df.select('track_id').distinct().count()}")
        logger.info(f"  Rating range: [{stats['min_rating']:.2f}, {stats['max_rating']:.2f}]")
        logger.info(f"  Average rating: {stats['avg_rating']:.2f}")
        
    def save_processed_data(self, df, output_path):
        df.write.mode("overwrite").parquet(f"{output_path}/training_data")
        logger.info(f"Saved training data to {output_path}/training_data")

def run_feature_engineering(raw_path, processed_path):
    spark = get_spark()
    engineer = FeatureEngineer(spark)
    
    interactions_df = engineer.load_interactions(raw_path)
    training_df = engineer.transform_data(interactions_df)
    engineer.validate_and_log_stats(training_df)
    engineer.save_processed_data(training_df, processed_path)