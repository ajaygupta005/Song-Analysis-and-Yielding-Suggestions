import sys
import os
import logging
from pyspark.sql import SparkSession
from src.config.config import SPARK_SHUFFLE_PARTITIONS, SPARK_APP_NAME

logger = logging.getLogger(__name__)

_spark_session = None

def get_spark():
    global _spark_session
    
    if _spark_session is not None:
        return _spark_session
    
    os.environ["PYSPARK_PYTHON"] = sys.executable
    
    _spark_session = (
        SparkSession.builder
        .appName(SPARK_APP_NAME)
        .config("spark.sql.shuffle.partitions", str(SPARK_SHUFFLE_PARTITIONS))
        .config("spark.executorEnv.PYSPARK_PYTHON", sys.executable)
        .config("spark.hadoop.io.nativeio.enabled", "false")
        .config("spark.hadoop.hadoop.native.lib", "false")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .getOrCreate()
    )
    
    logger.info(f"Spark session initialized: {SPARK_APP_NAME}")
    return _spark_session

def stop_spark():
    global _spark_session
    if _spark_session is not None:
        _spark_session.stop()
        _spark_session = None
        logger.info("Spark session stopped")