import base64
from requests import post, get
import json
import os
import pandas as pd
from dotenv import load_dotenv
import streamlit as st


client_id = st.secrets["CLIENT_ID"]
client_secret = st.secrets["CLIENT_SECRET"]


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded" 
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def call_spotify_api(url):
    try:
        token = get_token()
        headers = get_auth_header(token)
        result = get(url, headers=headers)
        result.raise_for_status()  # Raise an exception for HTTP errors
        json_result = json.loads(result.content)
        return json_result
    except Exception as e:
        print(f"An error occurred while calling the Spotify API: {str(e)}")
        return None  # Return None to indicate an error
    
LIMIT_PER_PAGE = 10
GENRES = ["alt-rock", "hard-rock", "j-rock", "psych-rock", "punk-rock", "rock-n-roll", "rock", "rockabilly"]

# Define a function to check if a genre is in the list of target genres
def is_genre_target(genres):
    return any(genre in GENRES for genre in genres)

# Define a function to get songs for a given name
def get_tracks(name):
    print(name)
    print(client_id, client_secret)
    try:
        response = call_spotify_api(f"https://api.spotify.com/v1/search?q=track:{name}&type=track&offset={0}&limit={LIMIT_PER_PAGE}")
        if response is None:
            return []

        track_list = []
        for t in response["tracks"]["items"]:
            track_id = t.get("id")
            track_name = t.get("name")
            track_artist = t.get("artists")[0]["name"]

            if not track_id or not track_name:
                continue

            track_genre = call_spotify_api(f"https://api.spotify.com/v1/artists/{t.get('artists')[0]['id']}")
            #print("\n\n TARGET \n:",track_genre['genres'], "\n\n")


            if is_genre_target(track_genre['genres']):
                track = {
                    "display_name": track_name + " | " + track_artist,
                    "title": track_name,
                    "id": track_id,
                    "artist": track_artist
                }
            
            else:
                print("It's not a rock song mate ! ")

            # track_features = call_spotify_api(f"https://api.spotify.com/v1/audio-features/{track_id}")
            # if track_features is not None:
            #     track = {"genre": genre, **track, **track_features}
            track_list.append(track)
        return track_list
    except Exception as e:
        print(f"An error occurred while getting songs for title '{name}': {str(e)}")
        return []


def get_model_features(selected_track_id):
            try:
                track_features = call_spotify_api(f"https://api.spotify.com/v1/audio-features/{selected_track_id}")
                if track_features is None:
                    return []
                track_popularity = call_spotify_api(f"https://api.spotify.com/v1/tracks/{selected_track_id}")
                if track_popularity is None:
                    return []
                return [
                     track_popularity['popularity'],
                     track_features['acousticness'],
                     track_features['duration_ms'],
                     track_features['loudness'],
                     track_features['energy'],
                     track_features['valence'],
                     track_features['instrumentalness'],
                     track_features['danceability'],
                     track_features['liveness'],
                     track_features['tempo']
                ]

            except Exception as e:
                print(f"An error occurred while getting songs for id '{selected_track_id}': {str(e)}")
                return ''