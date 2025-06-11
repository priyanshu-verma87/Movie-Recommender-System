import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# -----------------------------
# TMDb API Key 
# -----------------------------
API_KEY = "3cf25cc40dc2027311c6ca390f2bc44d"  

# -----------------------------
# Download similarity.pkl from Google Drive if not present
# -----------------------------
SIMILARITY_FILE = "similarity.pkl"
DRIVE_FILE_ID = "1vzUgzoPKTqp3JbSDKBLmGsYQX-VVlRn2"
if not os.path.exists(SIMILARITY_FILE):
    gdown.download(f"https://drive.google.com/uc?id={DRIVE_FILE_ID}", SIMILARITY_FILE, quiet=False)

# -----------------------------
# Load Pickled Data
# -----------------------------
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open(SIMILARITY_FILE, 'rb'))

# -----------------------------
# Poster Fetcher: By Title
# -----------------------------
def fetch_poster_by_title(title):
    try:
        query = title.replace(" ", "%20")
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get("results")
        if results and results[0].get("poster_path"):
            poster_path = results[0]["poster_path"]
            return "https://image.tmdb.org/t/p/w500" + poster_path
    except Exception as e:
        print(f"[ERROR] Poster fetch failed for '{title}': {e}")
    return "https://via.placeholder.com/500x750?text=No+Image"

# -----------------------------
# Recommender Logic
# -----------------------------
def recommend(movie_title):
    try:
        index = movies[movies['title'] == movie_title].index[0]
    except IndexError:
        return [], []

    distances = similarity[index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []
    for i in movie_indices:
        title = movies.iloc[i[0]].title
        recommended_titles.append(title)
        recommended_posters.append(fetch_poster_by_title(title))

    return recommended_titles, recommended_posters

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Choose a movie you like:", movies['title'].values)

if st.button("Recommend"):
    titles, posters = recommend(selected_movie)

    if titles:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(posters[i], use_container_width=True)
                st.caption(titles[i])
    else:
        st.warning("No recommendations found. Try another movie.")
