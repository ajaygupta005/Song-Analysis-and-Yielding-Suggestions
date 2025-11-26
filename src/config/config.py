import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

RAW_DATA_PATH = BASE_DIR / "data" / "raw"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed"
MODEL_PATH = BASE_DIR / "models" / "als_model"
OUTPUT_PATH = BASE_DIR / "data" / "output"

USER_SONG_DATA_FILE = "personalized_music_recommendation.csv"

ALS_MAX_ITER = 10
ALS_REG_PARAM = 0.1
ALS_RANK = 20
TRAIN_TEST_SPLIT = 0.8

SPARK_SHUFFLE_PARTITIONS = 8
SPARK_APP_NAME = "SpotifyRecommender"

MIN_RATING = 0.5
MAX_RATING = 5.0