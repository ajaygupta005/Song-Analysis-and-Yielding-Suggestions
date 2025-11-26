# Music Recommendation System - Data Engineering Project

A distributed data pipeline for music recommendations using Apache Spark and collaborative filtering.

## Architecture

```
                    ┌─────────────────────────┐
                    │   Prefect Orchestration │
                    │   (Workflow Engine)     │
                    └───────────┬─────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
        ┌───────────┐   ┌──────────────┐   ┌─────────────┐
        │   Task 1  │──▶│    Task 2    │──▶│   Task 3    │
        │Ingestion  │   │Transformation│   │  Training   │
        │(Synthetic)│   │ (Spark ETL)  │   │(ALS Model)  │
        └─────┬─────┘   └──────┬───────┘   └──────┬──────┘
              │                │                   │
              ▼                ▼                   ▼
         CSV Files        Parquet Files      Model Artifacts
```

## Data Engineering Concepts

### 1. **Workflow Orchestration with Prefect**
- Task dependency management and execution order
- Automatic retry logic for failed tasks
- Distributed task execution support
- Built-in logging and monitoring
- Flow state management

### 2. **Distributed Processing with Apache Spark**
- Leverages Spark's distributed computing for large-scale data processing
- Parquet format for columnar storage and efficient queries
- Adaptive query execution for optimized performance

### 3. **ETL Pipeline**
- **Extract**: Load raw CSV data and synthetic user interactions
- **Transform**: Feature engineering with distributed joins and aggregations
- **Load**: Persist processed data in Parquet format

### 4. **Data Validation & Quality**
- Schema inference and type casting
- Deduplication of user-track pairs
- Statistical validation of rating distributions

### 5. **Machine Learning Pipeline**
- Train/test split for model evaluation
- Collaborative filtering using ALS (Alternating Least Squares)
- Model persistence and versioning

## Project Structure

```
spotify_analysis/
├── data/
│   ├── raw/              # Source data (CSV)
│   ├── processed/        # Transformed data (Parquet)
│   └── output/           # Analysis results
├── models/               # Trained model artifacts
├── src/
│   ├── config/          # Configuration management
│   ├── data_preprocessing/  # ETL logic
│   ├── model/           # ML training and inference
│   ├── pipeline/        
│   │   ├── prefect_pipeline.py  # Orchestration with Prefect
│   │   └── main_pipeline.py     # Legacy direct execution
│   └── utils/           # Spark session management
├── docker-compose.yaml
├── Dockerfile
└── requirements.txt
```

## Setup

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run pipeline
python -m src.pipeline.main_pipeline
```

### Docker Deployment

```bash
# Build and run
docker-compose build
docker-compose up

# Access Streamlit UI
# Open http://localhost:8501
```

## Usage

### Run Complete Pipeline

**Option 1: With Prefect Orchestration (Recommended)**
```python
from src.pipeline.prefect_pipeline import run_pipeline

# Execute orchestrated pipeline
run_pipeline(force_run=True)
```

**Option 2: Command Line with Prefect**
```bash
python -m src.pipeline.prefect_pipeline
```

**Option 3: View Prefect UI**
```bash
prefect server start
# Open http://localhost:4200
```

### Generate Recommendations

```python
from src.model.recommender import recommend

# Get top-K recommendations
recommendations = recommend(
    model_path="models/als_model",
    user_id=42,
    k=10
)
```

### Streamlit Application

Launch the web interface:

```bash
streamlit run streamlit_app.py
```

## Configuration

Edit `src/config/config.py`:

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

## Pipeline Stages

### Stage 1: Data Ingestion
Generates synthetic user interaction data:
- User profiles (ID, age, country)
- Track metadata (ID, genre)
- User-track ratings (1-5 scale)

### Stage 2: Feature Engineering
Distributed transformation using Spark:
- Index assignment for tracks
- Join user interactions with track catalog
- Type casting and validation
- Statistical profiling

### Stage 3: Model Training
Collaborative filtering with ALS:
- Train/test split (80/20)
- Matrix factorization
- RMSE and MAE evaluation
- Model persistence

## Technical Stack

- **Orchestration**: Prefect 2.14 (workflow engine)
- **Data Processing**: Apache Spark (PySpark 3.5.1)
- **Storage**: Parquet (columnar format)
- **ML Algorithm**: Alternating Least Squares (ALS)
- **Web Framework**: Streamlit
- **Container**: Docker with Java 21
- **Language**: Python 3.10

## Key Features

✅ **Workflow orchestration** with Prefect  
✅ **Task dependencies** and retry logic  
✅ **Distributed computing** for scalability  
✅ **Columnar storage** with Parquet  
✅ **ETL pipeline** with proper stages  
✅ **Model versioning** and persistence  
✅ **Logging** for observability  
✅ **Configuration management**  
✅ **Docker deployment**  

## Performance Metrics

The ALS model is evaluated on:
- **RMSE** (Root Mean Square Error)
- **MAE** (Mean Absolute Error)

Logs show detailed statistics:
- Training/test set sizes
- Rating distributions
- Execution times per stage

## Future Enhancements

- Content-based filtering
- Hybrid recommendation approach
- Real-time inference API
- A/B testing framework
- Data drift monitoring

## Requirements

- Python 3.10+
- Java 21 (for Spark)
- 4GB+ RAM (for Spark local mode)
- Docker (for containerized deployment)

## License

MIT License
