#!/bin/sh

# Set environment variables for PySpark
export PYSPARK_PYTHON=$(which python)
export PYSPARK_DRIVER_PYTHON=$(which python)

# Verify Java is available
java -version || echo "Warning: Java not found!"

# Execute the Streamlit application using 'python -m' to ensure correct path resolution.
# We are running the 'streamlit_app.py' file located in the root directory.
exec python -m streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0