import streamlit as st
import pandas as pd
import os
from pathlib import Path
from src.pipeline.prefect_pipeline import run_pipeline
from src.model.recommender import recommend
from src.config.config import MODEL_PATH, PROCESSED_DATA_PATH

st.set_page_config(
    page_title="Music Recommendation System",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Spotify Music Recommendation Engine")
st.markdown("""
Real user data processing with **Apache Spark** and **Prefect orchestration** 
for personalized music recommendations using collaborative filtering.
""")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Pipeline Execution")
    st.markdown("Run the complete ETL pipeline with real user-song data:")
    
    if st.button("🚀 Execute Data Pipeline", type="primary"):
        with st.spinner("Running distributed data pipeline..."):
            try:
                run_pipeline(force_run=True)
                st.success("✅ Pipeline executed successfully!")
                st.info(f"Model artifacts saved to: `{MODEL_PATH}`")
            except Exception as e:
                st.error(f"Pipeline failed: {str(e)}")

with col2:
    st.header("Pipeline Stages")
    st.markdown("""
    **Orchestration**: Prefect workflow engine
    
    1. **Data Loading**: Load real user-song interactions
    2. **Transformation**: Spark-based feature engineering
    3. **Model Training**: ALS collaborative filtering
    
    Each task includes retry logic and logging.
    """)

st.divider()

st.header("Recommendation Service")

model_exists = os.path.exists(MODEL_PATH)

if model_exists:
    from src.config.config import RAW_DATA_PATH
    interactions_file = Path(RAW_DATA_PATH) / "user_track_interactions.csv"
    
    if interactions_file.exists():
        interactions_df = pd.read_csv(interactions_file)
        unique_users = sorted(interactions_df['user_id'].unique())
        
        col3, col4 = st.columns([1, 3])
        
        with col3:
            user_id = st.selectbox(
                "Select User ID:",
                options=unique_users,
                index=0
            )
            
            k = st.slider("Top-K Recommendations:", 1, 20, 5)
            
            generate_btn = st.button("Generate Recommendations", type="primary")
        
        with col4:
            if generate_btn:
                with st.spinner(f"Generating recommendations for User {user_id}..."):
                    try:
                        recommendations = recommend(str(MODEL_PATH), user_id, k)
                        
                        if not recommendations.empty:
                            st.subheader(f"Top {k} Recommendations for User {user_id}")
                            
                            recommendations.index = range(1, len(recommendations) + 1)
                            st.dataframe(
                                recommendations,
                                use_container_width=True,
                                hide_index=False
                            )
                        else:
                            st.warning("No recommendations available for this user.")
                            
                    except Exception as e:
                        st.error(f"Recommendation failed: {str(e)}")
    else:
        st.warning("Interaction data not found. Please run the pipeline first.")
else:
    st.warning("⚠️ Model not found. Execute the pipeline first to train the model.")