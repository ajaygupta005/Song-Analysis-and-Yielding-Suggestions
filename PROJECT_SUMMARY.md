# Music Recommendation System - Project Summary

## Overview
Production-ready data engineering pipeline for music recommendations using distributed processing and collaborative filtering.

## ✅ Core Technologies

### Data Engineering
- **Orchestration**: Prefect 2.14 (task dependencies, retries, monitoring)
- **Distributed Processing**: Apache Spark (PySpark 3.5.1)
- **Storage Format**: Parquet (columnar, optimized for analytics)
- **Configuration Management**: Centralized config module
- **Logging**: Structured logging with Python logging module

### Machine Learning
- **Algorithm**: Alternating Least Squares (ALS) Collaborative Filtering
- **Evaluation**: RMSE and MAE metrics
- **Model Persistence**: Spark ML model artifacts

### Deployment
- **Containerization**: Docker with Java 21
- **UI**: Streamlit web application
- **Orchestration**: Docker Compose

## 📁 Final Project Structure

```
spotify_analysis/
├── src/
│   ├── config/
│   │   └── config.py                 # Centralized configuration
│   ├── data_preprocessing/
│   │   ├── generate_user_data.py     # Synthetic data generation
│   │   └── feature_engineering.py    # Spark ETL transformations
│   ├── model/
│   │   ├── als_trainer.py            # Model training with evaluation
│   │   └── recommender.py            # Inference engine
│   ├── pipeline/
│   │   ├── prefect_pipeline.py       # Orchestrated workflow (Primary)
│   │   └── main_pipeline.py          # Direct execution (Fallback)
│   └── utils/
│       └── spark_session.py          # Spark session singleton
├── data/                             # Data directories (git-ignored)
├── models/                           # Model artifacts (git-ignored)
├── docker/
│   └── entrypoint.sh                 # Container startup script
├── streamlit_app.py                  # Web UI
├── docker-compose.yaml               # Multi-container orchestration
├── Dockerfile                        # Container definition
├── requirements.txt                  # Python dependencies
├── README.md                         # Full documentation
├── CLEANUP.md                        # Cleanup instructions
└── .gitignore                        # VCS ignore rules
```

## 🎯 Data Engineering Concepts Demonstrated

1. **Workflow Orchestration**
   - Task dependency management with Prefect
   - Automatic retry logic for fault tolerance
   - Distributed task execution support
   - Monitoring and observability

2. **Distributed Data Processing**
   - Apache Spark for horizontal scalability
   - Lazy evaluation and query optimization
   - Adaptive query execution
   - In-memory processing

3. **ETL Pipeline**
   - Extract: CSV data ingestion
   - Transform: Distributed joins, aggregations, type casting
   - Load: Parquet persistence for analytics

4. **Data Storage Optimization**
   - Columnar format (Parquet) for fast reads
   - Schema evolution support
   - Compression enabled
   - Predicate pushdown optimization

5. **Model Pipeline**
   - Train/test split for validation
   - Hyperparameter configuration
   - Model evaluation metrics
   - Artifact versioning and persistence

6. **Software Engineering**
   - OOP design patterns (classes, inheritance)
   - Configuration management
   - Proper logging and error handling
   - Docker containerization
   - Git version control

## 🚀 Execution Workflows

### 1. Orchestrated Pipeline (Prefect)
```python
from src.pipeline.prefect_pipeline import run_pipeline
run_pipeline(force_run=True)
```

**Tasks:**
- `task_data_ingestion` → Generates synthetic data
- `task_feature_engineering` → Spark transformations
- `task_model_training` → ALS model training

**Features:**
- Automatic retries (2x for ingestion/transform, 1x for training)
- Task logging and monitoring
- Dependency resolution
- State management

### 2. Direct Execution
```python
from src.pipeline.main_pipeline import run_pipeline
run_pipeline(force_run=True)
```

### 3. Streamlit UI
```bash
streamlit run streamlit_app.py
```
- Interactive pipeline execution
- User-friendly recommendation interface
- Real-time monitoring

### 4. Docker Deployment
```bash
docker-compose up
# Access: http://localhost:8501
```

## 📊 Pipeline Stages

### Stage 1: Data Ingestion
- Generates 500 users, 300 tracks, 5000 interactions
- Creates CSV files in `data/raw/`
- Configurable via `config.py`

### Stage 2: Feature Engineering (Spark)
- Loads raw CSV files
- Assigns unique track IDs
- Joins interactions with track catalog
- Type casting and validation
- Outputs Parquet to `data/processed/`
- Logs statistics (user count, rating distribution, etc.)

### Stage 3: Model Training (Spark ML)
- Loads processed Parquet data
- 80/20 train-test split
- Trains ALS model (rank=20, maxIter=10, regParam=0.1)
- Evaluates with RMSE and MAE
- Saves model to `models/als_model/`

### Stage 4: Inference (On-demand)
- Loads trained model
- Generates top-K recommendations per user
- Returns ranked track IDs with predicted scores

## 🔧 Configuration

All parameters centralized in `src/config/config.py`:

```python
# Data Generation
NUM_USERS = 500
NUM_TRACKS = 300
NUM_INTERACTIONS = 5000

# ALS Hyperparameters
ALS_MAX_ITER = 10
ALS_REG_PARAM = 0.1
ALS_RANK = 20

# Spark Configuration
SPARK_SHUFFLE_PARTITIONS = 8
```

## ✨ Key Features

✅ Production-grade orchestration (Prefect)  
✅ Distributed processing (Apache Spark)  
✅ Columnar storage (Parquet)  
✅ Task retry logic and fault tolerance  
✅ Comprehensive logging  
✅ OOP design patterns  
✅ Configuration management  
✅ Docker containerization  
✅ Interactive UI (Streamlit)  
✅ Model evaluation metrics  
✅ Clean, documented code  

## 🧹 Cleanup Instructions

See `CLEANUP.md` for removing deprecated files:
- Old Airflow directories (replaced by Prefect)
- Empty placeholder files
- Diagnostic scripts
- Temporary documentation

## 📝 Future Enhancements

- [ ] Content-based filtering for cold-start problem
- [ ] Hybrid recommendation (collaborative + content)
- [ ] Real-time streaming with Spark Structured Streaming
- [ ] A/B testing framework
- [ ] Data drift monitoring
- [ ] MLflow for experiment tracking
- [ ] Kubernetes deployment
- [ ] REST API with FastAPI

## 🎓 Learning Outcomes

This project demonstrates:
- End-to-end data engineering pipeline design
- Distributed computing with Apache Spark
- Workflow orchestration best practices
- ML model training and deployment
- Containerized application architecture
- Production-ready code structure

## 📚 Dependencies

See `requirements.txt` for full list. Key packages:
- `prefect==2.14.0` - Workflow orchestration
- `pyspark==3.5.1` - Distributed processing
- `streamlit` - Web UI
- `pandas`, `numpy` - Data manipulation
- `loguru` - Enhanced logging

## 🐳 Docker

**Base Image**: `python:3.10-slim`  
**Java**: OpenJDK 21 (required for Spark)  
**Port**: 8501 (Streamlit)

## 📄 License

MIT License - See project repository for details.

---

**Project**: Music Recommendation System  
**Architecture**: Distributed Data Pipeline  
**Technologies**: Spark, Prefect, Docker, Streamlit  
**Purpose**: Production-ready data engineering demonstration
