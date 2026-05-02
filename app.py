import streamlit as st
import pickle
import os
import gdown

import requests

def fetch_poster(movie_id):
    api_key = "22130acc2554f50d77f5399e4e172c37"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

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
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters
# ---------------- UI ----------------
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.image(posters[i])
            st.caption(names[i])