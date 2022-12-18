import streamlit as st
import pandas as pd
import pickle
import requests

# set icon and title...
from PIL import Image
img = Image.open('Multimedia-Film.ico')
st.set_page_config(page_title='Movie Recommender System', page_icon=img)

# set Background Image...
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://www.brycheiniog.co.uk/application/files/1616/0621/2569/web-2.jpg");
             background-attachment: fixed;
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

# hide navbar...
hide_menu_style = """
        <style>
        .css-1avcm0n {
               background: none;
        },
        .css-14xtw13 {
    visibility: hidden;
}
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
         
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# fetch movie data...
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        # fetch the movie poster...
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

# import Model...
movies_list = pickle.load(open('Model/movie_list.pkl','rb'))
similarity = pickle.load(open('Model/similarity.pkl','rb'))
movies =pd.DataFrame(movies_list)

st.header('Movie Recommender System')

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values)

# show recommended movie...
if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
