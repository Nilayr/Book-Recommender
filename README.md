\# 📚 Book Recommendation System



A web-based book recommendation system that suggests books to users based on popularity and item-based collaborative filtering. Built using Streamlit and deployed on Streamlit Cloud.



\## 🔗 Live App



👉 \[Launch App](https://book-recommender-eowotcueuihttamzgp5h2k.streamlit.app)



\## 📌 Project Structure



\- `app.py` - Main Streamlit application

\- `Books.xlsx`, `Ratings.csv`, `Users.csv` - Dataset files

\- `Project/Book\_Recommender\_System-main/` - Contains core logic and recommendation engine

\- `requirements.txt` - Dependencies

\- `background image.jpg` - UI background

\- `screenshots/` - Project UI captures



\## 📊 Features



\- 📈 Popularity-based book recommendations

\- 🤝 Item-based Collaborative Filtering using cosine similarity

\- 📚 Book cover images fetched via OpenLibrary API

\- 🎨 Clean UI with background image customization

\- ☁️ Deployed using Streamlit Cloud



\## 🖼️ Screenshots



| Homepage                            | Recommendation Section                   |

|------------------------------------|-------------------------------------------|

| !\[Homepage](screenshots/homepage.png) | !\[Recommendations](screenshots/results.png) |



\## ⚙️ Installation



Clone the repo and install dependencies:



```bash

git clone https://github.com/Nilayr/Book-Recommender.git

cd Book-Recommender

pip install -r requirements.txt

streamlit run app.py



