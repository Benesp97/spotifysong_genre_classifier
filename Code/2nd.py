import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

PATH =  os.path.join('.', 'spotify_tracks.csv')

df = pd.read_csv(PATH)
df = df.drop('Unnamed: 0', axis=1) # First we drop this useless column

target_genre = []

all_genres = list(df['track_genre'].unique())

for genre in all_genres:
    if 'rock' in genre:
        target_genre.append(genre)

df_target = df.apply(lambda row : row[df['track_genre'].isin(target_genre)]) # Keeping only rows with genres targeted
label_encoder = LabelEncoder()
df_target['track_genre'] = label_encoder.fit_transform(df_target['track_genre'])

df_model = df_target.drop(['track_id', 'artists','album_name', 'track_name'], axis = 1).reset_index().drop('index', axis=1)
df_model = pd.get_dummies(df_model, columns=['key', 'explicit', 'mode', 'time_signature'], dtype='int') # We have to domify those categorical columns

to_keep = ['popularity', 'acousticness', 'duration_ms', 'loudness', 'energy', 'valence', 'instrumentalness', 'danceability', 'liveness', 'tempo']
X = df_model[to_keep]
y = df_model[['track_genre']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True, stratify=y)

lgbm = LGBMClassifier(learning_rate=0.1, max_depth=3, n_estimators=100)
lgbm.fit(X_train, y_train)
y_pred_train = lgbm.predict(X_train)
y_pred_test = lgbm.predict(X_test)
acc_train = accuracy_score(y_pred_train, y_train)
acc_test = accuracy_score(y_pred_test, y_test)
print(f'Accuracy Without Scaling Train: {acc_train * 100}%')
print(f'Accuracy Without Scaling Test: {acc_test * 100}%\n')

# ebm = ExplainableBoostingClassifier()
# ebm.fit(X_train, y_train)

# y_pred_train = ebm.predict(X_train)
# y_pred_test = ebm.predict(X_test)
# acc_train = accuracy_score(y_pred_train, y_train)
# acc_test = accuracy_score(y_pred_test, y_test)
# print(f'Accuracy Without Scaling Train: {acc_train * 100}%')
# print(f'Accuracy Without Scaling Test: {acc_test * 100}%\n')

