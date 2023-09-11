import streamlit as st
import numpy as np
import pandas as pd
import pickle
from spotify_api import get_tracks, get_model_features
import os

RESULTS = {
    0: "alt-rock",
    1: "hard-rock",
    2: "j-rock",
    3: "psych-rock",
    4: "punk-rock",
    5: "rock-n-roll",
    6: "rock",
    7: "rockabilly"
}

# Page
st.set_page_config(page_title="Spotify Song Genre Classifier", page_icon=":musical_notes", layout="wide")


# HEADER SECTION 
st.header("Spotify Gender Classification Model")
st.subheader("Let's choose a rock song and see the model identify a genre")
st.write("Check out my GitHub repository : https://github.com/Benesp97/spotifysong_genre_classifier")
st.divider()

st.warning(' You have to choose a rock song ! 🤘🎸', icon="⚠️")

input = st.text_input(label="Song name :", value="", placeholder="Stairway To Heaven")

try :
    if input != '':
        list_of_songs = get_tracks(input)
        st.info('Confirm the track from the Spotify Api to run the model', icon="ℹ️")
        st.subheader("Please confirm the track")
        confirmed_track = st.selectbox(label="", options=pd.DataFrame(list_of_songs), key="title")
        selected_track_id = selected_track_id = next((song['id'] for song in list_of_songs if song['display_name'] == confirmed_track), None)
        st.divider()

        model_features = get_model_features(selected_track_id)

        pickled_model = pickle.load(open("Code/model_spotify_classifier.pkl", 'rb'))
        pick_pred = pickled_model.predict(np.array(model_features).reshape(1,-1))



        # st.write(RESULTS[pick_pred])
        genre = RESULTS[int(pick_pred)]
        st.success(f'This is the genre for {confirmed_track} !', icon="💡")
        st.success(genre, icon="✅")

    else:   
        st.info('To get the results please enter the song name in the input above', icon="ℹ️")
except :
    st.error("It seems that you haven't chosen a rock song 😡", icon="🚨")