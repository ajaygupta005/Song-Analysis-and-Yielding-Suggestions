from pyspark.ml.recommendation import ALSModel
from src.utils.spark_session import get_spark
import pandas as pd

def recommend(model_path, user_id, k=5):
    # Spark is initialized only when this function is called.
    spark = get_spark() 

    try:
        model = ALSModel.load(model_path)
    except Exception as e:
        print(f"Model not found at {model_path}: {e}")
        return None

    # Create a DataFrame for the user subset
    user_df = spark.createDataFrame([(user_id,)], ["user_id"])
    
    # Generate recommendations
    recommendations = model.recommendForUserSubset(user_df, k)
    
    # Extract and format recommendations
    if not recommendations.count():
        return pd.DataFrame({"Message": ["No recommendations found for this user."]})

    recs_list = recommendations.collect()[0]['recommendations']
    
    rec_data = [{'Track ID': r.track_id, 'Predicted Rating': f"{r.rating:.4f}"} for r in recs_list]
    
    return spark.createDataFrame(rec_data).toPandas()