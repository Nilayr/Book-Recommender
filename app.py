import streamlit as st
import base64
import pandas as pd
import requests
from books_recommender.config.configuration import AppConfiguration
from books_recommender.pipeline.training_pipeline import TrainingPipeline
from books_recommender.pipeline.prediction_pipeline import PredictionPipeline

# Background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("background.jpg")

# App title
st.title("📚 Book Recommendation System")

# Sidebar
app_mode = st.sidebar.selectbox("Choose the operation", ["Run Pipeline", "Recommend Books"])
app_config = AppConfiguration()

# Run the pipeline
if app_mode == "Run Pipeline":
    st.subheader("🔁 Run Data Ingestion & Training Pipeline")
    if st.button("Run Pipeline"):
        try:
            pipeline = TrainingPipeline(app_config)
            pipeline.run_pipeline()
            st.success("Pipeline completed successfully ✅")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Recommendation section
elif app_mode == "Recommend Books":
    st.subheader("🔍 Get Book Recommendations")
    book_name = st.text_input("Enter a book title")

    if st.button("Recommend"):
        if book_name:
            try:
                predictor = PredictionPipeline(app_config)
                recommendations = predictor.get_detailed_recommendations(book_name)  # You must return DataFrame or dict from this function

                if recommendations is not None and not recommendations.empty:
                    st.markdown("### 🏆 Recommended Books")

                    for idx, row in recommendations.iterrows():
                        st.image(row['Image-URL-M'], width=120)
                        st.markdown(f"**📖 Title:** {row['Book-Title']}")
                        st.markdown(f"**✍️ Author:** {row['Book-Author']}")
                        st.markdown(f"**⭐ Rating:** {row['Rating']:.2f}")
                        st.markdown("---")

                else:
                    st.warning("No recommendations found. Try another book.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please enter a book title to get recommendations.")
