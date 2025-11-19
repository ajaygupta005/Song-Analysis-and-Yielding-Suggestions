from pyspark.sql import SparkSession
import sys
import os

def get_spark():
    # Set PYSPARK_PYTHON to use the current Python executable
    os.environ["PYSPARK_PYTHON"] = sys.executable
    
    return (
        SparkSession.builder
        .appName("SpotifyRecommender")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.executorEnv.PYSPARK_PYTHON", sys.executable)
        .config("spark.hadoop.io.nativeio.enabled", "false")
        .config("spark.hadoop.hadoop.native.lib", "false")
        .getOrCreate()
    )