import streamlit as st
import pandas as pd
import os
from src.pipeline.main_pipeline import run_pipeline, MODEL_PATH, RAW_PATH # Correct path
from src.model.recommender import recommend
# We remove the global call to get_spark() here.

# --- UI Layout ---
st.set_page_config(page_title="Spotify Recommender Demo")

st.title("🎧 Spotify ALS Recommender System")
st.markdown("Click the button to run the PySpark data pipeline and train the ALS model.")

# --- Pipeline Execution ---
st.header("1. Data Pipeline & Model Training")

if st.button("Run Full Pipeline (Generate Data & Train Model)"):
    # This is where the Spark initialization delay will now happen (on user click)
    with st.spinner('Starting PySpark and running pipeline... This may take a moment.'):
        run_pipeline(force_run=True)
    st.success(f"Pipeline complete! Model saved to `{MODEL_PATH}`.")

# --- Recommendation Generation ---
st.header("2. Get Recommendations")

if os.path.exists(MODEL_PATH):
    # Find available users from the generated data (assuming 500 users)
    available_users = [str(i) for i in range(1, 501)]
    
    user_id_str = st.selectbox(
        "Select a User ID for recommendation:",
        options=available_users
    )
    
    k = st.slider("Number of Recommendations (k):", 1, 20, 5)
    
    if st.button("Generate Recommendations"):
        user_id = int(user_id_str)
        
        with st.spinner(f"Generating top {k} recommendations for User {user_id}..."):
            # The recommender function will now call get_spark() internally.
            recommendations_df = recommend(MODEL_PATH, user_id, k)

            if recommendations_df is not None:
                st.subheader(f"Top {k} Tracks for User {user_id}")
                st.dataframe(recommendations_df)
            else:
                st.error("Could not generate recommendations. Check pipeline logs for errors.")

else:
    st.warning("Model not found. Please click 'Run Full Pipeline' above to train the model first.")