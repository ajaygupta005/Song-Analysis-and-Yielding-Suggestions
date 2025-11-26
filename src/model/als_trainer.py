import logging
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from src.utils.spark_session import get_spark
from src.config.config import ALS_MAX_ITER, ALS_REG_PARAM, ALS_RANK, TRAIN_TEST_SPLIT

logger = logging.getLogger(__name__)

class ALSModelTrainer:
    def __init__(self, spark_session):
        self.spark = spark_session
        
    def load_training_data(self, data_path):
        df = self.spark.read.parquet(f"{data_path}/training_data")
        logger.info(f"Loaded {df.count()} training samples")
        return df
        
    def split_data(self, df):
        train, test = df.randomSplit([TRAIN_TEST_SPLIT, 1 - TRAIN_TEST_SPLIT], seed=42)
        logger.info(f"Train set: {train.count()} samples")
        logger.info(f"Test set: {test.count()} samples")
        return train, test
        
    def build_model(self):
        return ALS(
            maxIter=ALS_MAX_ITER,
            regParam=ALS_REG_PARAM,
            rank=ALS_RANK,
            userCol="user_id",
            itemCol="track_id",
            ratingCol="rating",
            coldStartStrategy="drop",
            nonnegative=True
        )
        
    def train_and_evaluate(self, train_df, test_df):
        als = self.build_model()
        
        logger.info("Training ALS model...")
        model = als.fit(train_df)
        
        logger.info("Evaluating model on test set...")
        predictions = model.transform(test_df)
        
        evaluator = RegressionEvaluator(
            metricName="rmse",
            labelCol="rating",
            predictionCol="prediction"
        )
        
        rmse = evaluator.evaluate(predictions)
        logger.info(f"Model RMSE: {rmse:.4f}")
        
        mae_evaluator = RegressionEvaluator(
            metricName="mae",
            labelCol="rating",
            predictionCol="prediction"
        )
        mae = mae_evaluator.evaluate(predictions)
        logger.info(f"Model MAE: {mae:.4f}")
        
        return model, {"rmse": rmse, "mae": mae}
        
    def save_model(self, model, model_path):
        model.write().overwrite().save(model_path)
        logger.info(f"Model saved to {model_path}")

def train_als(processed_path, model_path):
    spark = get_spark()
    trainer = ALSModelTrainer(spark)
    
    df = trainer.load_training_data(processed_path)
    train_df, test_df = trainer.split_data(df)
    
    model, metrics = trainer.train_and_evaluate(train_df, test_df)
    trainer.save_model(model, model_path)
    
    return metrics