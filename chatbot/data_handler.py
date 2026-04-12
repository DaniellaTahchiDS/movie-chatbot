# chatbot/data_handler.py

import os
import pandas as pd
import numpy as np
import pickle
from dotenv import load_dotenv

load_dotenv()

# Set HF token before importing sentence_transformers
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    os.environ["HF_TOKEN"] = hf_token
    print("✅ Hugging Face token loaded")
else:
    print("⚠️  No HF_TOKEN found (optional, will still work)")

from sentence_transformers import SentenceTransformer

class MovieDataHandler:
    def __init__(self, csv_path='data/movies.csv', embeddings_path='data/embeddings.pkl'):
        self.df = pd.read_csv(csv_path)
        self.df['release_year'] = self.df['release_year'].astype(int)
        self.df['vote_average'] = self.df['vote_average'].astype(float)
        self.df['runtime'] = self.df['runtime'].astype(int)
        self.df['vote_count'] = self.df['vote_count'].astype(int)
        self.df['popularity'] = self.df['popularity'].astype(float)

        # Clean string columns - fill NaN
        str_cols = ['title', 'overview', 'tagline', 'keywords', 'genres',
                    'overview_clean', 'tagline_clean', 'keywords_clean_str',
                    'genres_clean_str']
        for col in str_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna('')

        # Build a combined text field for semantic search
        self.df['search_text'] = (
            self.df['title'] + ' ' +
            self.df['overview'] + ' ' +
            self.df['tagline'].fillna('') + ' ' +
            self.df['genres'].fillna('') + ' ' +
            self.df['keywords'].fillna('')
        )

        # Load or build embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # ~80MB, fast
        if os.path.exists(embeddings_path):
            with open(embeddings_path, 'rb') as f:
                self.embeddings = pickle.load(f)
        else:
            self.embeddings = self._build_embeddings(embeddings_path)

    def _build_embeddings(self, save_path):
        print("Building embeddings (one-time)...")
        embeddings = self.model.encode(
            self.df['search_text'].tolist(),
            show_progress_bar=True,
            normalize_embeddings=True
        )
        with open(save_path, 'wb') as f:
            pickle.dump(embeddings, f)
        print("Embeddings saved!")
        return embeddings

    # ──────────── SEARCH METHODS ────────────

    def semantic_search(self, query, top_k=5):
        """Find movies most similar to a natural language query"""
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        top_indices = similarities.argsort()[-top_k:][::-1]
        results = self.df.iloc[top_indices].copy()
        results['similarity'] = similarities[top_indices]
        return results

    def search_by_title(self, title):
        """Exact or fuzzy title search"""
        # Exact match first
        exact = self.df[self.df['title'].str.lower() == title.lower()]
        if not exact.empty:
            return exact

        # Partial match
        partial = self.df[self.df['title'].str.lower().str.contains(
            title.lower(), na=False
        )]
        return partial

    def search_by_genre(self, genre, top_k=10):
        """Find movies by genre"""
        mask = self.df['genres'].str.lower().str.contains(genre.lower(), na=False)
        return self.df[mask].sort_values('vote_average', ascending=False).head(top_k)

    def search_by_year(self, year, top_k=10):
        """Find movies from a specific year"""
        return self.df[self.df['release_year'] == year].sort_values(
            'vote_average', ascending=False
        ).head(top_k)

    def search_by_year_range(self, start_year, end_year, top_k=10):
        """Find movies within a year range"""
        mask = (self.df['release_year'] >= start_year) & (self.df['release_year'] <= end_year)
        return self.df[mask].sort_values('vote_average', ascending=False).head(top_k)

    def get_top_rated(self, top_k=10, min_votes=1000):
        """Get top rated movies with minimum vote threshold"""
        filtered = self.df[self.df['vote_count'] >= min_votes]
        return filtered.sort_values('vote_average', ascending=False).head(top_k)

    def get_most_popular(self, top_k=10):
        """Get most popular movies"""
        return self.df.sort_values('popularity', ascending=False).head(top_k)

    def search_by_keyword(self, keyword, top_k=10):
        """Search movies by keyword"""
        mask = self.df['keywords'].str.lower().str.contains(keyword.lower(), na=False)
        return self.df[mask].sort_values('vote_average', ascending=False).head(top_k)

    def get_movie_details(self, title):
        """Get full details for a specific movie"""
        movie = self.search_by_title(title)
        if movie.empty:
            return None
        return movie.iloc[0]

    def get_recommendations(self, title, top_k=5):
        """Get similar movies based on a given movie"""
        movie = self.search_by_title(title)
        if movie.empty:
            return None

        idx = movie.index[0]
        movie_embedding = self.embeddings[self.df.index.get_loc(idx)].reshape(1, -1)
        similarities = np.dot(self.embeddings, movie_embedding.T).flatten()

        # Exclude the movie itself
        loc = self.df.index.get_loc(idx)
        similarities[loc] = -1

        top_indices = similarities.argsort()[-top_k:][::-1]
        results = self.df.iloc[top_indices].copy()
        results['similarity'] = similarities[top_indices]
        return results

    def get_stats(self):
        """Get dataset statistics"""
        return {
            'total_movies': len(self.df),
            'year_range': f"{self.df['release_year'].min()}-{self.df['release_year'].max()}",
            'avg_rating': round(self.df['vote_average'].mean(), 2),
            'genres': sorted(set(
                g.strip()
                for genres in self.df['genres'].dropna()
                for g in genres.split(',')
            ))
        }

    def filter_movies(self, genre=None, min_rating=None, max_rating=None,
                      year=None, min_year=None, max_year=None, top_k=10):
        """Flexible multi-criteria filter"""
        result = self.df.copy()

        if genre:
            result = result[result['genres'].str.lower().str.contains(
                genre.lower(), na=False
            )]
        if min_rating is not None:
            result = result[result['vote_average'] >= min_rating]
        if max_rating is not None:
            result = result[result['vote_average'] <= max_rating]
        if year is not None:
            result = result[result['release_year'] == year]
        if min_year is not None:
            result = result[result['release_year'] >= min_year]
        if max_year is not None:
            result = result[result['release_year'] <= max_year]

        return result.sort_values('vote_average', ascending=False).head(top_k)