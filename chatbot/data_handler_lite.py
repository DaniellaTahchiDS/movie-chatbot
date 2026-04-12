# chatbot/data_handler_lite.py
import pandas as pd
import numpy as np


class MovieDataHandler:
    def __init__(self, csv_path='data/movies.csv', embeddings_path=None):
        self.df = pd.read_csv(csv_path)
        self.df['release_year'] = self.df['release_year'].astype(int)
        self.df['vote_average'] = self.df['vote_average'].astype(float)
        self.df['runtime'] = self.df['runtime'].astype(int)
        self.df['vote_count'] = self.df['vote_count'].astype(int)
        self.df['popularity'] = self.df['popularity'].astype(float)

        str_cols = ['title', 'overview', 'tagline', 'keywords', 'genres',
                    'overview_clean', 'tagline_clean', 'keywords_clean_str',
                    'genres_clean_str']
        for col in str_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna('')

        self.df['search_text'] = (
            self.df['title'] + ' ' +
            self.df['overview'] + ' ' +
            self.df['tagline'].fillna('') + ' ' +
            self.df['genres'].fillna('') + ' ' +
            self.df['keywords'].fillna('')
        ).str.lower()

        print(f"✅ Loaded {len(self.df)} movies (lightweight mode)")

    def semantic_search(self, query, top_k=5):
        """Keyword-based search — no ML model needed"""
        query_words = set(query.lower().split())
        scores = []

        for _, row in self.df.iterrows():
            text = row['search_text']
            score = sum(1 for word in query_words if word in text)
            if query.lower() in row['title'].lower():
                score += 10
            scores.append(score)

        self.df['similarity'] = np.array(scores) / max(max(scores), 1)
        results = self.df.nlargest(top_k, 'similarity').copy()
        return results[results['similarity'] > 0]

    def search_by_title(self, title):
        exact = self.df[self.df['title'].str.lower() == title.lower()]
        if not exact.empty:
            return exact
        return self.df[self.df['title'].str.lower().str.contains(
            title.lower(), na=False
        )]

    def search_by_genre(self, genre, top_k=10):
        mask = self.df['genres'].str.lower().str.contains(genre.lower(), na=False)
        return self.df[mask].sort_values('vote_average', ascending=False).head(top_k)

    def search_by_year(self, year, top_k=10):
        return self.df[self.df['release_year'] == year].sort_values(
            'vote_average', ascending=False
        ).head(top_k)

    def search_by_year_range(self, start_year, end_year, top_k=10):
        mask = (self.df['release_year'] >= start_year) & (self.df['release_year'] <= end_year)
        return self.df[mask].sort_values('vote_average', ascending=False).head(top_k)

    def get_top_rated(self, top_k=10, min_votes=1000):
        filtered = self.df[self.df['vote_count'] >= min_votes]
        return filtered.sort_values('vote_average', ascending=False).head(top_k)

    def get_most_popular(self, top_k=10):
        return self.df.sort_values('popularity', ascending=False).head(top_k)

    def search_by_keyword(self, keyword, top_k=10):
        mask = self.df['keywords'].str.lower().str.contains(keyword.lower(), na=False)
        return self.df[mask].sort_values('vote_average', ascending=False).head(top_k)

    def get_movie_details(self, title):
        movie = self.search_by_title(title)
        if movie.empty:
            return None
        return movie.iloc[0]

    def get_recommendations(self, title, top_k=5):
        movie = self.search_by_title(title)
        if movie.empty:
            return None
        genres = movie.iloc[0]['genres'].lower()
        keywords = movie.iloc[0]['keywords'].lower()
        search_query = f"{genres} {keywords}"
        results = self.semantic_search(search_query, top_k + 1)
        # Remove the original movie from results
        results = results[results['title'].str.lower() != title.lower()]
        return results.head(top_k)

    def get_stats(self):
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