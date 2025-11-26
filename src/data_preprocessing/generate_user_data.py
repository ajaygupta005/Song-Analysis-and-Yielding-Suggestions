import pandas as pd
import os
import logging
from pathlib import Path
from src.config.config import USER_SONG_DATA_FILE, MIN_RATING, MAX_RATING

logger = logging.getLogger(__name__)

class RealDataLoader:
    def __init__(self, raw_path):
        self.raw_path = Path(raw_path)
        
    def load_and_prepare_data(self):
        logger.info("Loading real user-song interaction data")
        
        input_file = self.raw_path / USER_SONG_DATA_FILE
        
        if not input_file.exists():
            raise FileNotFoundError(
                f"Data file not found: {input_file}\n"
                f"Please ensure '{USER_SONG_DATA_FILE}' exists in {self.raw_path}"
            )
        
        df = pd.read_csv(input_file)
        logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns")
        
        required_cols = ['user_id', 'song_id']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        df['rating'] = df.apply(self._calculate_rating, axis=1)
        
        interactions = df[['user_id', 'song_id', 'rating']].copy()
        interactions = interactions.drop_duplicates(subset=['user_id', 'song_id'])
        
        interactions.columns = ['user_id', 'track_id', 'rating']
        
        logger.info(f"Prepared {len(interactions)} unique user-track interactions")
        logger.info(f"Rating range: [{interactions['rating'].min():.2f}, {interactions['rating'].max():.2f}]")
        logger.info(f"Average rating: {interactions['rating'].mean():.2f}")
        
        return interactions
        
    def _calculate_rating(self, row):
        rating = 2.5
        
        if 'liked' in row and row['liked'] == 1:
            rating += 2.0
        
        if 'finished_song' in row and row['finished_song'] == 1:
            rating += 0.5
        
        if 'skip_count' in row and row['skip_count'] > 0:
            rating -= min(row['skip_count'] * 0.3, 1.5)
        
        if 'repeat_count' in row and row['repeat_count'] > 0:
            rating += min(row['repeat_count'] * 0.5, 1.0)
        
        if 'play_count' in row and row['play_count'] > 1:
            rating += min(row['play_count'] * 0.2, 1.0)
        
        return max(MIN_RATING, min(MAX_RATING, rating))
    
    def save_prepared_data(self, interactions, output_path):
        os.makedirs(output_path, exist_ok=True)
        
        output_file = f"{output_path}/user_track_interactions.csv"
        interactions.to_csv(output_file, index=False)
        
        logger.info(f"Saved {len(interactions)} interactions to {output_file}")
        logger.info(f"Unique users: {interactions['user_id'].nunique()}")
        logger.info(f"Unique tracks: {interactions['track_id'].nunique()}")

def load_real_data(raw_path):
    """Load and prepare real user-song interaction data"""
    loader = RealDataLoader(raw_path)
    interactions = loader.load_and_prepare_data()
    loader.save_prepared_data(interactions, raw_path)

def generate_user_data(output_path):
    """Legacy wrapper for backwards compatibility"""
    raw_path = str(Path(output_path).parent / "raw")
    load_real_data(raw_path)
