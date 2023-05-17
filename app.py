import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    overview=data['overview']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path,overview

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    # enumerazte is used to add index with distance so that after sorting index is not lost.
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_overview=[]
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        path,overview=fetch_poster(movie_id)
        recommended_movie_posters.append(path)
        recommended_movie_overview.append(overview)
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters,recommended_movie_overview


st.header('Movie Recommender System')

# unpickling
movies = pd.read_pickle(open('movie_list.pkl','rb'))
similarity = pd.read_pickle(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters,recommended_movie_overview = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.rows(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        st.text(recommended_movie_overview[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        st.text(recommended_movie_overview[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        st.text(recommended_movie_overview[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
        st.text(recommended_movie_overview[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        st.text(recommended_movie_overview[4])


# run with:: streamlit run app.py


