from flask import Flask, request, render_template
import requests
import difflib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Loading the dataset
movies = pd.read_csv('movies for project.csv')

# Filling NaN values with an empty string
movies['genres'] = movies['genres'].fillna('')
movies['keywords'] = movies['keywords'].fillna('')
movies['tagline'] = movies['tagline'].fillna('')
movies['cast'] = movies['cast'].fillna('')
movies['director'] = movies['director'].fillna('')

# Combining features
combined_features = movies['genres'] + '  ' + movies['keywords'] + '  ' + movies['tagline'] + '  ' + movies['cast'] + '  ' + movies['director']

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
features_vectors = vectorizer.fit_transform(combined_features)

# Compute cosine similarity
similarity = cosine_similarity(features_vectors)

# Movie titles list for close matches
list_of_all_titles = movies['title'].tolist()

API_KEY = 'b93e560c'

def get_movie_poster(movie_name):

    url = f'http://www.omdbapi.com/?t={movie_name.replace(" ", "+")}&apikey={API_KEY}'  # URL-encode movie name
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data['Response'] == 'True':
            return data['Poster']
        else:
            return 'https://via.placeholder.com/200x300.png?text=No+Poster'
    else:
        return 'https://via.placeholder.com/200x300.png?text=Error+Loading+Poster'


# Function to get movie recommendations
def get_movie_recommendations(movie_name):
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

    if not find_close_match:
        return []

    close_match = find_close_match[0]

    # Get the index of the movie
    index_of_the_movie = movies[movies.title == close_match].index.values[0]

    # Get similarity scores for all movies
    similarity_score = list(enumerate(similarity[index_of_the_movie]))

    # Sort movies based on similarity score
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommendations = []
    for i, movie in enumerate(sorted_similar_movies[1:11]):
        index = movie[0]
        title_from_index = movies.iloc[index]['title']
        recommendations.append(title_from_index)

    return recommendations


# Initialize Flask app
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/recommendation', methods=['POST', 'GET'])
def recommendation():
    if request.method == 'POST':
        movie_name = request.form.get('movies')

        if not movie_name:
            return render_template("prediction.html", status=False, error="Please select a movie")

        recommended_movies = get_movie_recommendations(movie_name)

        posters = []
        for movie in recommended_movies:
            poster_url = get_movie_poster(movie)
            posters.append(poster_url)

        return render_template(
            "prediction.html",
            status=True,
            poster=posters,
            movies_name=recommended_movies,
            error=None
        )
    else:
        movie_list = movies['title'].tolist()
        return render_template("prediction.html", movie_list=movie_list, status=False)

if __name__ == '__main__':
    app.debug = True
    app.run()