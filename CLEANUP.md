# Project Cleanup Guide

## Files/Folders to Delete

Run the following commands to remove unnecessary files:

### Windows (PowerShell)
```powershell
cd C:\Users\ajayk\Downloads\spotify_analysis

# Remove deprecated Airflow directories
Remove-Item -Recurse -Force airflow, airflow_home, dags -ErrorAction SilentlyContinue

# Remove empty/unused directories
Remove-Item -Recurse -Force artifacts, notebooks -ErrorAction SilentlyContinue

# Remove unused Python files
Remove-Item -Force run_pipeline.py -ErrorAction SilentlyContinue
Remove-Item -Force check_spark_env.py -ErrorAction SilentlyContinue
Remove-Item -Force DOCKER_SETUP.md -ErrorAction SilentlyContinue
Remove-Item -Force src\model\content_based.py -ErrorAction SilentlyContinue
Remove-Item -Force src\model\evaluator.py -ErrorAction SilentlyContinue
Remove-Item -Force src\data_preprocessing\load_data.py -ErrorAction SilentlyContinue
```

### Linux/Mac
```bash
cd ~/spotify_analysis

# Remove deprecated directories
rm -rf airflow airflow_home dags artifacts notebooks

# Remove unused files
rm -f run_pipeline.py check_spark_env.py DOCKER_SETUP.md
rm -f src/model/content_based.py src/model/evaluator.py
rm -f src/data_preprocessing/load_data.py
```

## Why These Files Are Unnecessary

### Directories to Remove:
- **airflow/**, **airflow_home/**, **dags/** - Replaced by Prefect orchestration
- **artifacts/** - Empty, not used in pipeline
- **notebooks/** - Empty, not part of production pipeline

### Files to Remove:
- **run_pipeline.py** - Empty file, functionality in `src/pipeline/`
- **check_spark_env.py** - Diagnostic script, not needed in production
- **DOCKER_SETUP.md** - Temporary setup notes, info now in README.md
- **src/model/content_based.py** - Empty placeholder, not implemented
- **src/model/evaluator.py** - Redundant, evaluation done in als_trainer.py
- **src/data_preprocessing/load_data.py** - Not used in current pipeline

## Clean Project Structure (After Cleanup)

```
spotify_analysis/
├── data/
│   ├── raw/              # Source CSV data
│   ├── processed/        # Transformed Parquet files
│   └── output/           # Results
├── docker/
│   └── entrypoint.sh
├── models/               # Trained model artifacts
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── data_preprocessing/
│   │   ├── __init__.py
│   │   ├── generate_user_data.py
│   │   └── feature_engineering.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── als_trainer.py
│   │   └── recommender.py
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── prefect_pipeline.py  # Primary orchestration
│   │   └── main_pipeline.py     # Fallback
│   └── utils/
│       ├── __init__.py
│       └── spark_session.py
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── README.md
├── requirements.txt
└── streamlit_app.py
```

## Verification

After cleanup, verify the project still works:

```bash
# Install dependencies
pip install -r requirements.txt

# Test pipeline
python -m src.pipeline.prefect_pipeline

# Test Streamlit app
streamlit run streamlit_app.py
```
