import streamlit as st
import pandas as pd
import pickle
from streamlit import session_state as session
import requests
import numpy as np

def fetch_link(movie_name):
    movie_name='-'.join(movie_name.split())
    movie_link=f"https://www.justwatch.com/in/movie/{movie_name}"
    response = requests.get(movie_link)
    if response.status_code == 200:
        return movie_link
    else:
        tv_link=f"https://www.justwatch.com/in/tv-show/{movie_name}"
        response = requests.get(tv_link)
        if response.status_code == 200:
            return tv_link
    
    return  f"https://en.wikipedia.org/wiki/{'_'.join(movie_name.split())}"

def fetch_trailer(movie_name):
    return f"https://www.youtube.com/results?search_query={movie_name}+trailer"


def recommend(movies,input_movie):
    movie_index = movies[movies['title'] == input_movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_link = []
    recommended_movies_trailer_link = []
    for x in movies_list:
        movie_title = movies.iloc[x[0]].title
        recommended_movies.append(movie_title)
        recommended_movies_link.append(fetch_link(movie_title))
        recommended_movies_trailer_link.append(fetch_trailer(movie_title))
    return recommended_movies, recommended_movies_link,recommended_movies_trailer_link

similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_data=pd.read_csv("movies.csv") #you can either generate from scraper.py or can copy paste your own movies data


st.title("What to binge?")
st.subheader('Movie recommendation :film_projector:', divider='rainbow')
st.write("")
recent_movie=st.selectbox("Which movie/tv show you just watched :sunglasses:!!!",movie_data['title']) # input movie name 
recommend_movies={"Name":[],"Link":[]}
result = pd.DataFrame.from_dict(recommend_movies)
    
if st.button('Recommend'):
    names, links, trailers = recommend(movie_data,recent_movie)
    
    data_df = pd.DataFrame(
    {
        "Name": names,
        "Link": links,
        "Trailer": trailers
    }
    )

    st.data_editor(
        data_df,
        column_config={
            "Name": st.column_config.TextColumn(
                "Top Recommended Movies",
                help="The top recommended movies"
            ),
            "Link": st.column_config.LinkColumn(
                "(watch/description) Links",
                help="Links of recommended movies"
            ),
            "Trailer": st.column_config.LinkColumn(
                "Trailer Links",
                help="Youtuber trailer links of recommended movies"
            ),
        }
    )




    