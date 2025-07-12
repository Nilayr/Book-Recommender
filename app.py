import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import base64

# ✅ Set Streamlit page config
st.set_page_config(page_title="📚 Book Recommender", layout="centered")

# ✅ Background image function
def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.88);
            padding: 2rem;
            border-radius: 1rem;
        }}
        img.book-cover {{
            border-radius: 8px;
            margin-bottom: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Apply background
set_background("background image.jpg")

# ✅ Load data
@st.cache_data
def load_data():
    ratings = pd.read_csv("Ratings.csv", encoding='latin1')
    books = pd.read_excel("Books.xlsx")
    return ratings, books

ratings, books = load_data()

# ✅ Filter active users and popular books
active_users = ratings['User-ID'].value_counts()[ratings['User-ID'].value_counts() >= 10].index
popular_books = ratings['ISBN'].value_counts()[ratings['ISBN'].value_counts() >= 20].index

filtered_ratings = ratings[
    (ratings['User-ID'].isin(active_users)) &
    (ratings['ISBN'].isin(popular_books)) &
    (ratings['Book-Rating'] > 0)
]

# ✅ Create user-item matrix
user_item_matrix = filtered_ratings.pivot_table(index='User-ID', columns='ISBN', values='Book-Rating').fillna(0)

# ✅ Compute item-item similarity
item_similarity = cosine_similarity(user_item_matrix.T)
item_similarity_df = pd.DataFrame(
    item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns
)

# ✅ Fallback popular books
top_books = filtered_ratings.groupby('ISBN')['Book-Rating'].mean().sort_values(ascending=False).index.tolist()

# ✅ Recommendation logic
def recommend_books(user_id, N=5):
    if user_id not in user_item_matrix.index:
        return top_books[:N]

    user_ratings = user_item_matrix.loc[user_id]
    rated_books = user_ratings[user_ratings > 0].index.tolist()
    scores = {}

    for book in rated_books:
        if book not in item_similarity_df:
            continue
        similar_books = item_similarity_df[book].drop(book)
        user_rating = user_ratings[book]
        for sim_book, similarity in similar_books.items():
            if sim_book in rated_books:
                continue
            scores.setdefault(sim_book, 0)
            scores[sim_book] += similarity * user_rating

    recommended = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [isbn for isbn, _ in recommended[:N]]

# ✅ Streamlit UI
st.title("📚 Book Recommendation System")
st.write("Get personalized book recommendations using item-based collaborative filtering.")

user_ids = user_item_matrix.index.tolist()
user_id = st.selectbox("Select your User ID", sorted(user_ids))

if st.button("Recommend Books"):
    rec_books = recommend_books(user_id)
    st.subheader("📖 Recommended Books:")

    for isbn in rec_books:
        title = books.loc[books['ISBN'] == isbn, 'Book-Title'].values
        author = books.loc[books['ISBN'] == isbn, 'Book-Author'].values
        rating = filtered_ratings[filtered_ratings['ISBN'] == isbn]['Book-Rating'].mean()
        cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

        st.markdown(f"""
            <div style="margin-bottom: 25px; padding: 10px; background-color: #f9f9f9; border-radius: 10px;">
                <img src="{cover_url}" width="120" class="book-cover"/>
                <h4 style="margin-bottom: 5px;">📘 {title[0] if len(title) > 0 else isbn}</h4>
                <p style="margin-top: 0;">👤 <em>{author[0] if len(author) > 0 else 'Unknown Author'}</em></p>
                <p style="margin-top: 0;">⭐ <strong>Average Rating:</strong> {rating:.2f}</p>
            </div>
        """, unsafe_allow_html=True)
