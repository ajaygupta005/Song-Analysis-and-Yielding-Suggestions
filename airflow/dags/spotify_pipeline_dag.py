from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.data_preprocessing.load_data import load_and_clean_data
from src.data_preprocessing.generate_user_data import generate_synthetic_user_data
from src.model.als_trainer import train_als_model
from src.model.evaluator import evaluate_model
from src.model.recommender import generate_recommendations
from src.config.config import DATA_PROCESSED, OUTPUT_DIR
import os

def run_load_data():
    load_and_clean_data()

def run_generate_user_data():
    import pandas as pd
    df = pd.read_csv(os.path.join(DATA_PROCESSED, "tracks_clean.csv"))
    generate_synthetic_user_data(df)

def run_train_model():
    train_als_model(os.path.join(DATA_PROCESSED, "user_track_interactions.csv"))

def run_evaluate_model():
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName("EvalALS").getOrCreate()
    spark.stop()
    print("✅ Model evaluation done (placeholder).")

def run_generate_recommendations():
    generate_recommendations(None, os.path.join(OUTPUT_DIR, "recommendations.json"))

default_args = {
    'owner': 'ajaygupta',
    'depends_on_past': False,
    'start_date': datetime(2025, 11, 9),
    'retries': 1,
}

with DAG(
    dag_id='spotify_recommendation_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='Spotify Recommendation Pipeline Orchestrated via Airflow'
) as dag:

    task_load_data = PythonOperator(
        task_id='load_data',
        python_callable=run_load_data
    )

    task_generate_user_data = PythonOperator(
        task_id='generate_user_data',
        python_callable=run_generate_user_data
    )

    task_train_model = PythonOperator(
        task_id='train_model',
        python_callable=run_train_model
    )

    task_evaluate_model = PythonOperator(
        task_id='evaluate_model',
        python_callable=run_evaluate_model
    )

    task_generate_recommendations = PythonOperator(
        task_id='generate_recommendations',
        python_callable=run_generate_recommendations
    )

    # Task dependency chain
    task_load_data >> task_generate_user_data >> task_train_model >> task_evaluate_model >> task_generate_recommendations
