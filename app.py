import streamlit as st
import pickle
import pandas as pd
import requests

# TMDb API Key
API_KEY = "3cf25cc40dc2027311c6ca390f2bc44d"

# Load pickled data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Fetch poster using TMDb API
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

# Recommend function
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

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Choose a movie you like:", movies['title'].values)

if st.button("Recommend"):
    titles, posters = recommend(selected_movie)

    if titles:
        st.markdown("### Recommended Movies")
        cols = st.columns(len(titles))  # dynamically create 5 columns

        for i in range(len(titles)):
            with cols[i]:
                st.image(posters[i], width=250)
                st.caption(titles[i])
    else:
        st.warning("No recommendations found. Try another movie.")
