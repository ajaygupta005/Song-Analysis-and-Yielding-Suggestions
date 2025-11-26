import os
import logging
from pathlib import Path
from datetime import datetime
from src.data_preprocessing.generate_user_data import load_real_data
from src.data_preprocessing.feature_engineering import run_feature_engineering
from src.model.als_trainer import train_als
from src.config.config import RAW_DATA_PATH, PROCESSED_DATA_PATH, MODEL_PATH


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataPipeline:
    def __init__(self):
        self.raw_path = str(RAW_DATA_PATH)
        self.processed_path = str(PROCESSED_DATA_PATH)
        self.model_path = str(MODEL_PATH)
        
    def setup_directories(self):
        for path in [self.raw_path, self.processed_path, Path(self.model_path).parent]:
            os.makedirs(path, exist_ok=True)
            
    def validate_raw_data(self):
        required_file = Path(self.raw_path) / "personalized_music_recommendation.csv"
        if not required_file.exists():
            raise FileNotFoundError(f"Required raw data file not found: {required_file}")
        return True
        
    def run(self, force_run=False):
        pipeline_start = datetime.now()
        
        if os.path.exists(self.model_path) and not force_run:
            logger.info(f"Model exists at {self.model_path}. Set force_run=True to retrain.")
            return
        
        try:
            self.setup_directories()
            
            logger.info("Stage 1/3: Data Ingestion - Loading real user-song interactions")
            load_real_data(self.raw_path)
            
            logger.info("Stage 2/3: Data Transformation - Running distributed feature engineering")
            run_feature_engineering(self.raw_path, self.processed_path)
            
            logger.info("Stage 3/3: Model Training - Training collaborative filtering model")
            train_als(self.processed_path, self.model_path)
            
            duration = (datetime.now() - pipeline_start).total_seconds()
            logger.info(f"Pipeline completed successfully in {duration:.2f}s")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise

def run_pipeline(force_run=False):
    pipeline = DataPipeline()
    pipeline.run(force_run)

if __name__ == "__main__":
    run_pipeline()