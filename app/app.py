import streamlit as st
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import seaborn as sns
from lazypredict.Supervised import LazyClassifier
from interpret.glassbox import ExplainableBoostingClassifier
from interpret import set_visualize_provider, show
from interpret.provider import InlineProvider
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from lightgbm import LGBMClassifier
import os


# Page
st.set_page_config(page_title="Spotify Song Genre Classifier", page_icon=":musical_notes", layout="wide")


# HEADER SECTION 
st.subheader("Let's choose a song and see the model identify a genre")
st.write("Check out my GitHub repository : https://github.com/Benesp97/spotifysong_genre_classifier")

PATH = os.path.join("..", "Data", "spotify_tracks.csv")
df = pd.read_csv(PATH)
# df = pd.read_csv('../Data/spotify_tracks.csv')
print(df.head(1))