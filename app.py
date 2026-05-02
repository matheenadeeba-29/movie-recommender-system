import streamlit as st
import pickle
import os
import gdown

# ---------------- DOWNLOAD FILES FIRST ----------------
MOVIES_URL = "PASTE_MOVIES_LINK"
SIMILARITY_URL = "PASTE_SIMILARITY_LINK"

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

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


# ---------------- UI ----------------
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)

    st.subheader("Recommended Movies:")
    for movie in recommendations:
        st.write(movie)