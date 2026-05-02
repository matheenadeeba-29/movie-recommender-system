import streamlit as st
import pickle
import os
import gdown

# ---------------- DOWNLOAD FILES FIRST ----------------
MOVIES_URL = "https://drive.google.com/uc?id=1tgHUuo7lnXoogvpfoFzcp7NC1iQUYiNC"
SIMILARITY_URL = "https://drive.google.com/uc?id=1TLUcp32DsVl2eXS6nv2-S2UL1UoJ_J8p"

if not os.path.exists("movies.pkl"):
    gdown.download(MOVIES_URL, "movies.pkl", quiet=False)

if not os.path.exists("similarity.pkl"):
    gdown.download(SIMILARITY_URL, "similarity.pkl", quiet=False)

# ---------------- LOAD AFTER DOWNLOAD ----------------
@st.cache_data
def load_data():
    with open("movies.pkl", "rb") as f:
        movies = pickle.load(f)
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
    return movies, similarity

movies, similarity = load_data()

# ---------------- RECOMMEND FUNCTION ----------------

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]

    recommended_movies = []
    seen = set()

    for i in movies_list:
        title = movies.iloc[i[0]].title
        if title not in seen:
            recommended_movies.append(title)
            seen.add(title)
        if len(recommended_movies) == 5:
            break

    return recommended_movies
# ---------------- UI ----------------
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    recommended_movies = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.text(recommended_movies[i])