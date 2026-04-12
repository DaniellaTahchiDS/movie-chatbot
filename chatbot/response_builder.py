# chatbot/response_builder.py
import pandas as pd

TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w200"

class ResponseBuilder:

    @staticmethod
    def movie_card(movie, show_similarity=False):
        """Build HTML card for a single movie"""
        if isinstance(movie, pd.Series):
            movie = movie.to_dict()

        poster_url = ""
        if movie.get('poster_path'):
            poster_url = f"{TMDB_IMAGE_BASE}{movie['poster_path']}"

        similarity_badge = ""
        if show_similarity and 'similarity' in movie:
            pct = round(movie['similarity'] * 100)
            similarity_badge = f'<span class="badge similarity">{pct}% match</span>'

        tagline_html = ""
        if movie.get('tagline'):
            tagline_html = f'<p class="tagline">"{movie["tagline"]}"</p>'

        genres_html = ""
        if movie.get('genres'):
            genres = [g.strip() for g in movie['genres'].split(',')]
            genres_html = ''.join(f'<span class="badge genre">{g}</span>' for g in genres)

        return f'''
        <div class="movie-card">
            {"<img src='" + poster_url + "' alt='poster' class='poster'/>" if poster_url else ""}
            <div class="movie-info">
                <h3>{movie.get('title', 'Unknown')} <span class="year">({movie.get('release_year', 'N/A')})</span></h3>
                {tagline_html}
                {similarity_badge}
                <div class="genres">{genres_html}</div>
                <p class="overview">{movie.get('overview', 'No description available.')[:200]}{'...' if len(str(movie.get('overview', ''))) > 200 else ''}</p>
                <div class="meta">
                    <span>⭐ {movie.get('vote_average', 'N/A')}/10</span>
                    <span>🕐 {movie.get('runtime', 'N/A')} min</span>
                    <span>👥 {movie.get('vote_count', 0):,} votes</span>
                </div>
            </div>
        </div>
        '''

    @staticmethod
    def movie_list(movies_df, title="Results", show_similarity=False):
        """Build HTML for a list of movies"""
        if movies_df.empty:
            return "<p>No movies found matching your criteria. 😔</p>"

        cards = ""
        for _, movie in movies_df.iterrows():
            cards += ResponseBuilder.movie_card(movie, show_similarity)

        return f"<p class='result-title'>{title}</p>{cards}"

    @staticmethod
    def movie_detail(movie):
        """Build detailed HTML for a single movie"""
        if movie is None:
            return "<p>Sorry, I couldn't find that movie. 🤔</p>"

        if isinstance(movie, pd.Series):
            movie = movie.to_dict()

        poster_url = ""
        if movie.get('poster_path'):
            poster_url = f"{TMDB_IMAGE_BASE}{movie['poster_path']}"

        keywords_html = ""
        if movie.get('keywords'):
            kws = [k.strip() for k in movie['keywords'].split(',')]
            keywords_html = '<div class="keywords"><strong>Keywords:</strong> ' + \
                ''.join(f'<span class="badge keyword">{k}</span>' for k in kws[:15]) + '</div>'

        genres_html = ""
        if movie.get('genres'):
            genres = [g.strip() for g in movie['genres'].split(',')]
            genres_html = ''.join(f'<span class="badge genre">{g}</span>' for g in genres)

        return f'''
        <div class="movie-detail">
            {"<img src='" + poster_url + "' alt='poster' class='poster-large'/>" if poster_url else ""}
            <div class="movie-info">
                <h2>{movie.get('title', 'Unknown')} <span class="year">({movie.get('release_year', 'N/A')})</span></h2>
                {f'<p class="tagline">"{movie.get("tagline")}"</p>' if movie.get('tagline') else ''}
                <div class="genres">{genres_html}</div>
                <p class="overview-full">{movie.get('overview', 'No description available.')}</p>
                <div class="meta-detail">
                    <div>⭐ <strong>{movie.get('vote_average', 'N/A')}</strong>/10 ({movie.get('vote_count', 0):,} votes)</div>
                    <div>🕐 <strong>{movie.get('runtime', 'N/A')}</strong> minutes</div>
                    <div>📈 Popularity: <strong>{movie.get('popularity', 'N/A')}</strong></div>
                </div>
                {keywords_html}
            </div>
        </div>
        '''

    @staticmethod
    def greeting():
        return '''
        <p>👋 Hello! I'm your <strong>Movie Chatbot</strong>! I can help you with:</p>
        <ul>
            <li>🔍 <strong>Find movies</strong> - "action movies", "movies from 2010"</li>
            <li>📖 <strong>Movie details</strong> - "tell me about Inception"</li>
            <li>🎯 <strong>Recommendations</strong> - "movies similar to The Matrix"</li>
            <li>⭐ <strong>Ratings</strong> - "what's the rating of Interstellar"</li>
            <li>🏆 <strong>Top lists</strong> - "best rated movies", "most popular"</li>
            <li>🔎 <strong>Search by topic</strong> - "movies about time travel"</li>
        </ul>
        <p>Try asking me something! 😊</p>
        '''

    @staticmethod
    def help_text():
        return '''
        <p>📚 Here's what I can do:</p>
        <table class="help-table">
            <tr><td><strong>Movie Info</strong></td><td>"Tell me about Inception"</td></tr>
            <tr><td><strong>Similar Movies</strong></td><td>"Movies like The Matrix"</td></tr>
            <tr><td><strong>Genre Search</strong></td><td>"Best action movies"</td></tr>
            <tr><td><strong>Year Search</strong></td><td>"Movies from 2014"</td></tr>
            <tr><td><strong>Year Range</strong></td><td>"Movies from 2010 to 2015"</td></tr>
            <tr><td><strong>Rating</strong></td><td>"Rating of Fight Club"</td></tr>
            <tr><td><strong>Runtime</strong></td><td>"How long is Titanic"</td></tr>
            <tr><td><strong>Top Rated</strong></td><td>"Best rated movies"</td></tr>
            <tr><td><strong>Popular</strong></td><td>"Most popular movies"</td></tr>
            <tr><td><strong>Topic Search</strong></td><td>"Movies about space travel"</td></tr>
            <tr><td><strong>Stats</strong></td><td>"How many movies"</td></tr>
        </table>
        '''

    @staticmethod
    def stats(stats_dict):
        genres_html = ', '.join(stats_dict['genres'][:20])
        return f'''
        <p>📊 <strong>Dataset Statistics:</strong></p>
        <ul>
            <li>🎬 Total movies: <strong>{stats_dict['total_movies']:,}</strong></li>
            <li>📅 Year range: <strong>{stats_dict['year_range']}</strong></li>
            <li>⭐ Average rating: <strong>{stats_dict['avg_rating']}</strong></li>
            <li>🎭 Genres: {genres_html}</li>
        </ul>
        '''