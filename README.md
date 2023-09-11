# Spotify rock music classifier.


The training data set comes from features specific to the music referenced by Spotify via the API. (e.g. acousticness, danceability, etc). With this in mind, I tried to see if these characteristics could be used to separate musical genres. In order to progress gradually, I decided to focus my study on one genre: rock. Spotify lists 8 different rock genres, so I had 8 classes to predict. 

In order to develop a functional application, I came up with the idea of interacting with it by entering the name of the music whose genre you wanted to predict. I used Spotify's API to find the ID of a piece of music using the name, and then to find the features of that music using the ID. Finally, I extracted these features and ran them through my pre-trained LGBM model. 
I finally designed and deployed my application using Streamlit.


This is a first version with an accuracy score that is far from satisfying. Nevertheless, the basis for the work is there and this project will be pushed for a second version.

In this second version, we will be looking for more correlated features to increase accuracy. In addition, we will try to extend the scope of prediction to all genres of music. 
