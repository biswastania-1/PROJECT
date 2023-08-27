import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c3498a68be0d4124dbbb9615a82f499f&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster from API

        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies,recommend_movies_poster


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'What are you looking for today ?',
movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)  # Create 5 columns for displaying recommendations

    for i, col in enumerate(cols):
        col.text(names[i])
        col.image(posters[i])
        