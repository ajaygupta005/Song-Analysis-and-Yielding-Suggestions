import logging
from pyspark.ml.recommendation import ALSModel
from src.utils.spark_session import get_spark
import pandas as pd

logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self, model_path):
        self.spark = get_spark()
        self.model = self._load_model(model_path)
        
    def _load_model(self, model_path):
        try:
            model = ALSModel.load(model_path)
            logger.info(f"Model loaded from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
            
    def get_recommendations(self, user_id, k=5):
        from pyspark.sql.types import IntegerType, StructType, StructField
        schema = StructType([StructField("user_id", IntegerType(), True)])
        user_df = self.spark.createDataFrame([(int(user_id),)], schema)
        
        recommendations = self.model.recommendForUserSubset(user_df, k)
        
        if not recommendations.count():
            logger.warning(f"No recommendations found for user {user_id}")
            return pd.DataFrame({"message": ["No recommendations available"]})
        
        recs_list = recommendations.collect()[0]['recommendations']
        
        results = [{
            'track_id': rec.track_id,
            'predicted_score': round(rec.rating, 4)
        } for rec in recs_list]
        
        return pd.DataFrame(results)
        
    def get_batch_recommendations(self, user_ids, k=5):
        from pyspark.sql.types import IntegerType, StructType, StructField
        schema = StructType([StructField("user_id", IntegerType(), True)])
        users_df = self.spark.createDataFrame(
            [(int(uid),) for uid in user_ids], 
            schema
        )
        
        recommendations = self.model.recommendForUserSubset(users_df, k)
        return recommendations.toPandas()

def recommend(model_path, user_id, k=5):
    engine = RecommendationEngine(model_path)
    return engine.get_recommendations(user_id, k)