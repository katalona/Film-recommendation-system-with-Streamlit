import os

import streamlit as st
from dotenv import load_dotenv

from api.omdb import OMDBApi
from recsys import ContentBaseRecSys

from random import sample

import base64

load_dotenv()

API_KEY = os.getenv("API_KEY")
MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")

omdbapi = OMDBApi(API_KEY)


recsys = ContentBaseRecSys(
    movies_dataset_filepath=MOVIES,
    distance_filepath=DISTANCE,)

# фоновая картинка
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

#фон основной части страницы
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

#фон сайдбара
def set_background_sidebar(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    [data-testid="stSidebar"] > div:first-child {{
        background: url("data:image/png;base64,%s");
        background-position: center center;
    }}
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)    

#фон верхней строки
def set_title(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
        [data-testid="stHeader"] {{
        background: url("data:image/png;base64,%s");
        background-size: cover;
    }}
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background_sidebar('./assets/sidebar.png')
set_background('./assets/background.png')
set_title('./assets/background.png')


#остальные элементы страницы
st.sidebar.title(":orange[**Where am I?**]")
st.sidebar.info(""":green[**Welcome to our film recommendation system**]""")

st.sidebar.title(":orange[**How it works?**]")
st.sidebar.info("""
                :green[**1. Choose a movie from drop-down list**]
                :green[**2. Customize genre, year and number of recsults you would like to get**]
                :green[**3. Tap on 'Get recommendations' button**]""")


selected_movie = st.sidebar.selectbox(":orange[**Choose a movie**]", recsys.get_title())


selected_genre = st.sidebar.selectbox(":orange[**Choose a genre**]", ['', *recsys.get_genres()])


selected_year = st.sidebar.text_input(":orange[**Choose a year**]")


TOP_K = st.sidebar.text_input(":orange[**How many movies you want to see in recommendation list**]")

st.markdown(
    "<h1 style='text-align: center; color: red; font-family: Papyrus; font-size:430%;'>Film recommendation system</h1>", unsafe_allow_html=True)

#main page part
#here are 3 random films
st.header(':orange[**Three random movies**]')
with st.expander("", expanded=True):

    random_films = sample(list(recsys.get_title()), 3)

    random_movies_col = st.columns(3)

    for index, col in enumerate(random_movies_col):
        with col:
            film = random_films[index]
            st.subheader(f':green[{random_films[index]}]')
            random_movie_poster = omdbapi.get_posters([random_films[index]])
            st.image(random_movie_poster)

if TOP_K == '':
    TOP_K = 5

if st.sidebar.button('Get recommendations'):
    st.header(f':orange[Your film is "{selected_movie}"]')
    recommended_movie_posters = omdbapi.get_posters([selected_movie])
    st.image(recommended_movie_posters)

    st.header(":orange[Recommended films]")
    
    recommended_movie_names = recsys.recommendation(selected_movie, genre=selected_genre, year=selected_year, top_k=int(TOP_K))

    if len(recommended_movie_names) == 0:
        st.subheader(':orange[There are no results for your request]')
    else:
        max_length_movie = len(max(recommended_movie_names, key=len))
        # для вывода постеров в одну строку
        # movies_col = st.columns(int(TOP_K))
        # for index_2, col_2 in enumerate(movies_col):
        #     with col_2:
        #         # попытка выровнять длину названий фильмов для красивого отображения
        #         film_name = recommended_movie_names[index_2] + " ." * (max_length_movie - len(recommended_movie_names[index_2]))
        #         st.write(film_name)
        #         movie_poster = omdbapi.get_posters([recommended_movie_names[index_2]])
        #         st.image(movie_poster)

        #для вывода постеров друг за другом
        for film in recommended_movie_names:
            st.subheader(f':green[{film}, {recsys.get_year(film)}]')  
            with st.expander(f":orange[**Movie overview and poster**]", expanded=True):
                st.write(f':green[**{recsys.get_overview(film)[0]}**]')
                recommended_movie_posters = omdbapi.get_posters([film])
                st.image(recommended_movie_posters)
