"""
Prefect workflow orchestration for the music recommendation pipeline.
Provides task dependencies, retries, logging, and monitoring.
"""
import logging
from datetime import timedelta
from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
from src.data_preprocessing.generate_user_data import load_real_data
from src.data_preprocessing.feature_engineering import run_feature_engineering
from src.model.als_trainer import train_als
from src.config.config import RAW_DATA_PATH, PROCESSED_DATA_PATH, MODEL_PATH

logger = logging.getLogger(__name__)

@task(
    name="load_real_data",
    description="Load real user-song interaction data",
    retries=2,
    retry_delay_seconds=30,
    log_prints=True
)
def task_load_real_data():
    """
    Task 1: Data Loading
    Loads and prepares real user-song interaction data from CSV.
    """
    raw_path = str(RAW_DATA_PATH)
    logger.info("Starting data loading task")
    load_real_data(raw_path)
    logger.info("Data loading completed")
    return raw_path

@task(
    name="feature_engineering",
    description="Distributed feature engineering with Spark",
    retries=2,
    retry_delay_seconds=30,
    log_prints=True
)
def task_feature_engineering(processed_path: str):
    """
    Task 2: Feature Engineering
    Performs distributed data transformation using Apache Spark:
    - Load prepared interaction data
    - Type casting and validation
    - Data quality checks
    - Persist as Parquet for efficient querying
    """
    raw_path = str(RAW_DATA_PATH)
    logger.info("Starting feature engineering task")
    run_feature_engineering(raw_path, processed_path)
    logger.info("Feature engineering completed")
    return processed_path

@task(
    name="model_training",
    description="Train collaborative filtering model",
    retries=1,
    retry_delay_seconds=60,
    log_prints=True
)
def task_model_training(processed_path: str):
    """
    Task 3: Model Training
    Trains ALS collaborative filtering model:
    - Load processed training data
    - Train/test split
    - Hyperparameter configuration
    - Model evaluation (RMSE, MAE)
    - Persist model artifacts
    """
    model_path = str(MODEL_PATH)
    logger.info("Starting model training task")
    metrics = train_als(processed_path, model_path)
    logger.info(f"Model training completed with metrics: {metrics}")
    return model_path

@flow(
    name="music_recommendation_pipeline",
    description="End-to-end data pipeline for music recommendations",
    task_runner=SequentialTaskRunner(),
    log_prints=True
)
def recommendation_pipeline_flow(force_run: bool = False):
    """
    Main orchestration flow for the music recommendation system.
    
    Pipeline Stages:
    1. Data Loading: Load real user-song interactions
    2. Feature Engineering: Transform data using Spark
    3. Model Training: Train collaborative filtering model
    
    Args:
        force_run: If True, retrain model even if it exists
        
    Returns:
        model_path: Path to trained model artifacts
    """
    import os
    
    model_path = str(MODEL_PATH)
    
    if os.path.exists(model_path) and not force_run:
        logger.info(f"Model exists at {model_path}. Set force_run=True to retrain.")
        return model_path
    
    logger.info("Starting music recommendation pipeline with real data")
    
    raw_path = task_load_real_data()
    processed_path = str(PROCESSED_DATA_PATH)
    task_feature_engineering(processed_path)
    final_model_path = task_model_training(processed_path)
    
    logger.info("Pipeline execution completed successfully")
    return final_model_path

def run_pipeline(force_run: bool = False):
    """
    Entry point for pipeline execution.
    Can be called from Streamlit UI or command line.
    """
    return recommendation_pipeline_flow(force_run=force_run)

if __name__ == "__main__":
    # Run pipeline with Prefect orchestration
    run_pipeline(force_run=True)
