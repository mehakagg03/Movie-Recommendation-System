# Movie-Recommendation-System
A Movie Recommendation System that suggests movies based on a user's input using the features like genre, keywords, tagline, cast, and director. The system uses a Cosine Similarity algorithm to recommend similar movies based on the content of a given movie.


TECHNOLOGIES USED

Flask: A web framework for Python to build the web application.

Pandas: Data analysis library for reading and processing the movie dataset.

Scikit-learn: For building the TF-IDF vectorizer and calculating cosine similarity between movies.

OMDb API: To fetch movie posters and other metadata for the recommended movies.


HOW IT WORKS

Dataset: The system uses a CSV file movies for project.csv that contains movie metadata such as title, genres, keywords, tagline, cast, and director.

Feature Engineering: Various features such as genres, keywords, tagline, cast, and director are combined to create a feature vector.

TF-IDF Vectorization: The combined features are vectorized using TF-IDF Vectorizer, which converts text into numerical data that the system can understand.

Cosine Similarity: Cosine similarity is used to calculate the similarity between movies based on the features.

Recommendation: Based on the input movie, the system fetches the top 10 most similar movies.
