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

# to dipaly in one column
# if st.button('Show Recommendation'):
#     recommended_movie_names,recommended_movie_posters,recommended_movie_overview = recommend(selected_movie)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#         st.text(recommended_movie_overview[0])
#     with col2:
#         st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])
#         st.text(recommended_movie_overview[1])

#     with col3:
#         st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#         st.text(recommended_movie_overview[2])
#     with col4:
#         st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#         st.text(recommended_movie_overview[3])
#     with col5:
#         st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])
#         st.text(recommended_movie_overview[4])
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_overview = recommend(selected_movie)
    
    # Calculate the number of rows needed
    num_movies = len(recommended_movie_names)
    num_columns = 1  # You can adjust the number of columns as needed
    num_rows = (num_movies + num_columns - 1) // num_columns
    
    # Create columns for each movie
    for row in range(num_rows):
        cols = st.columns(num_columns)
        for col in range(num_columns):
            index = row * num_columns + col
            if index < num_movies:
                with cols[col]:
                    st.text(recommended_movie_names[index])
                    st.image(recommended_movie_posters[index])
                    st.text(recommended_movie_overview[index])



# run with:: streamlit run app.py


