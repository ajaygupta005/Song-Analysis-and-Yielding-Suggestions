from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from src.utils.spark_session import get_spark

def train_als(processed_path, model_path):
    spark = get_spark()

    df = spark.read.parquet(f"{processed_path}/training_data")

    (train, test) = df.randomSplit([0.8, 0.2])

    als = ALS(
        maxIter=10,
        regParam=0.1,
        userCol="user_id",
        itemCol="track_id",
        ratingCol="rating",
        coldStartStrategy="drop"
    )

    model = als.fit(train)
    predictions = model.transform(test)

    evaluator = RegressionEvaluator(
        metricName="rmse",
        labelCol="rating",
        predictionCol="prediction"
    )

    rmse = evaluator.evaluate(predictions)
    print(f"ALS RMSE: {rmse}")

    model.write().overwrite().save(model_path)
    print("ALS model saved successfully!")