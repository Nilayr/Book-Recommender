# Book Recommendation System (Filtered)

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

# Load datasets (update path if needed)
books = pd.read_excel(r'C:\Users\Vaibhav Rathod\Desktop\Nilay\Data Science Projet PS554\Books.xlsx')
ratings = pd.read_csv(r'C:\Users\Vaibhav Rathod\Desktop\Nilay\Data Science Projet PS554\Ratings.csv', encoding='ISO-8859-1')
users = pd.read_csv(r'C:\Users\Vaibhav Rathod\Desktop\Nilay\Data Science Projet PS554\Users.csv', encoding='ISO-8859-1')

# Merge all data
book_ratings = pd.merge(ratings, books, on='ISBN')
user_book_df = pd.merge(book_ratings, users, on='User-ID')

# Remove datetime errors in Book-Title
import datetime
user_book_df = user_book_df[~user_book_df['Book-Title'].apply(lambda x: isinstance(x, datetime.datetime))]

# Fix data types
user_book_df['Book-Title'] = user_book_df['Book-Title'].astype(str)
user_book_df['User-ID'] = user_book_df['User-ID'].astype(str)
user_book_df['Book-Rating'] = pd.to_numeric(user_book_df['Book-Rating'], errors='coerce')
user_book_df.dropna(subset=['Book-Rating'], inplace=True)

# FILTERING to reduce memory usage
# Keep books with at least 50 ratings
popular_books = user_book_df['Book-Title'].value_counts()
popular_books = popular_books[popular_books >= 50].index
filtered_df = user_book_df[user_book_df['Book-Title'].isin(popular_books)]

# Keep users with at least 30 ratings
active_users = filtered_df['User-ID'].value_counts()
active_users = active_users[active_users >= 30].index
filtered_df = filtered_df[filtered_df['User-ID'].isin(active_users)]

# Create pivot table (item-user matrix)
book_user_matrix = filtered_df.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
book_user_matrix.fillna(0, inplace=True)

# Compute cosine similarity
book_similarity = cosine_similarity(book_user_matrix)
book_similarity_df = pd.DataFrame(book_similarity, index=book_user_matrix.index, columns=book_user_matrix.index)

# Recommendation function
def recommend_books(book_name, n=5):
    if book_name not in book_similarity_df:
        return f"'{book_name}' not found in dataset."
    similar_books = book_similarity_df[book_name].sort_values(ascending=False)[1:n+1]
    return similar_books

# Test the recommender
recommend_books('A Fine Balance', 5)

# --- Visualization: Sample Pivot Heatmap ---
sample_matrix = book_user_matrix.sample(10, axis=0).sample(10, axis=1)
plt.figure(figsize=(10, 6))
sns.heatmap(sample_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Sample of Book-User Rating Matrix')
plt.xlabel('User-ID')
plt.ylabel('Book Title')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# --- Visualization: Top 20 Books by Average Rating ---
avg_ratings = book_user_matrix.mean(axis=1).sort_values(ascending=False).head(20)
plt.figure(figsize=(12, 6))
avg_ratings.plot(kind='barh', color='skyblue')
plt.xlabel('Average Rating')
plt.title('Top 20 Books by Average Rating')
plt.gca().invert_yaxis()
plt.show()

# --- Visualization: Top 20 Most Rated Books ---
num_ratings = (book_user_matrix > 0).sum(axis=1).sort_values(ascending=False).head(20)
plt.figure(figsize=(12, 6))
num_ratings.plot(kind='barh', color='orange')
plt.xlabel('Number of Ratings')
plt.title('Top 20 Most Rated Books')
plt.gca().invert_yaxis()
plt.show()
