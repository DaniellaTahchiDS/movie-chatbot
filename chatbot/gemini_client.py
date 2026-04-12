# chatbot/gemini_client.py
import os
from dotenv import load_dotenv

load_dotenv()


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.use_gemini = False
        self.client = None

        if not api_key:
            print("⚠️  No API key found. Running in LOCAL-ONLY mode.")
            return

        try:
            from google import genai

            self.client = genai.Client(api_key=api_key)
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents="Hi",
            )
            self.use_gemini = True
            self.model = "gemini-2.5-flash-lite"
            print("✅ Gemini API connected successfully!")
        except Exception as e:
            print(f"⚠️  Gemini API failed: {str(e)[:100]}")
            self.use_gemini = False

        # ──────────────────────────────────────────────
        #  UPDATED SYSTEM PROMPT - Allows general 
        #  movie knowledge from Gemini
        # ──────────────────────────────────────────────
        self.system_prompt = """You are a friendly, knowledgeable, and enthusiastic Movie Chatbot assistant.
You have deep knowledge about movies including ratings, overviews, genres, cast, directors,
awards, box office, trivia, behind-the-scenes facts, soundtracks, cultural impact, and more.

RULES:

1. Answer movie questions naturally and confidently.

2. NEVER mention where your information comes from. Do NOT say things like:
   - "based on my database"
   - "according to my data"
   - "from my general knowledge"
   - "in my database"
   - "not in my database"
   - "my curated database"
   - "I don't have that in my data"
   - "the data I have"
   - "the context provided"
   - "based on the information provided"
   - Just answer as a knowledgeable movie expert would.

3. When you have specific stats (rating, runtime, vote count, genres):
   → Include them naturally in your response without mentioning their source.

4. When asked about actors, directors, awards, trivia, box office, etc.:
   → Answer confidently using your knowledge.
   → Never apologize for "not having it in the database".

5. For recommendations:
   → Recommend movies naturally without explaining why certain movies
     are or aren't in any list.

6. If you genuinely don't know something:
   → Say "I'm not sure about that" naturally, like a human would.
   → Do NOT blame it on database limitations.

7. STYLE:
   → Be conversational, warm, and enthusiastic about movies.
   → Use emojis occasionally.
   → Format responses in clean HTML using <strong>, <em>, <p>, <ul>, <li>, <h3> tags.
   → Do NOT use markdown. Use HTML only.
   → Keep responses informative but concise.

8. Always feel free to discuss:
   → Cast and actors
   → Directors and producers
   → Awards and nominations
   → Box office performance
   → Behind the scenes facts
   → Sequels, prequels, franchises
   → Cultural impact and legacy
   → Soundtracks and composers
   → Filming locations
   → Trivia and fun facts
   → Themes and meanings
   → Comparisons between movies"""

    def generate_response(self, user_message, movie_context, chat_history=None):
        """Generate response - uses Gemini if available, local fallback otherwise"""

        if not self.use_gemini:
            return self._local_response(user_message, movie_context)

        context_prompt = f"""{self.system_prompt}

--- MOVIE DATABASE CONTEXT ---
{movie_context}
--- END MOVIE DATABASE CONTEXT ---

User's question: {user_message}

Remember: Use the database for ratings/stats AND your own knowledge for 
actors/directors/awards/trivia/etc. Format response in HTML."""

        contents = []
        if chat_history:
            for exchange in chat_history[-6:]:
                contents.append(
                    {"role": "user", "parts": [{"text": exchange["user"]}]}
                )
                contents.append(
                    {"role": "model", "parts": [{"text": exchange["bot"]}]}
                )
        contents.append({"role": "user", "parts": [{"text": context_prompt}]})

        try:
            from google import genai

            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config={
                    "temperature": 0.7,
                    "max_output_tokens": 1024,
                    "top_p": 0.9,
                },
            )
            return response.text

        except Exception as e:
            error_msg = str(e)
            print(f"Gemini error: {error_msg[:100]}")
            return self._local_response(user_message, movie_context)

    def _local_response(self, user_message, movie_context):
        """Fallback: Generate a response locally without any API."""
        movies = []
        if movie_context and "MOVIE:" in movie_context:
            blocks = movie_context.split("---")
            for block in blocks:
                movie = {}
                for line in block.strip().split("\n"):
                    line = line.strip()
                    if line.startswith("MOVIE:"):
                        movie["title"] = line.replace("MOVIE:", "").strip()
                    elif line.startswith("Year:"):
                        movie["year"] = line.replace("Year:", "").strip()
                    elif line.startswith("Rating:"):
                        movie["rating"] = line.replace("Rating:", "").strip()
                    elif line.startswith("Runtime:"):
                        movie["runtime"] = line.replace("Runtime:", "").strip()
                    elif line.startswith("Genres:"):
                        movie["genres"] = line.replace("Genres:", "").strip()
                    elif line.startswith("Overview:"):
                        movie["overview"] = line.replace("Overview:", "").strip()
                    elif line.startswith("Relevance Score:"):
                        movie["score"] = line.replace("Relevance Score:", "").strip()
                if movie.get("title"):
                    movies.append(movie)

        if not movies:
            return (
                "<p>Sorry, I couldn't find any matching movies. "
                "Try a different question! 🤔</p>"
            )

        html = "<p>🎬 Here's what I found:</p>"
        for movie in movies[:8]:
            genres_badges = ""
            if movie.get("genres") and movie["genres"] != "N/A":
                for g in movie["genres"].split(","):
                    g = g.strip()
                    genres_badges += (
                        f'<span style="background:rgba(0,184,148,0.2);'
                        f"color:#00b894;padding:2px 8px;border-radius:10px;"
                        f'font-size:0.75em;margin-right:4px;">{g}</span>'
                    )

            overview = movie.get("overview", "")
            if len(overview) > 200:
                overview = overview[:200] + "..."

            html += f"""
            <div style="background:rgba(255,255,255,0.05);border:1px solid 
            rgba(255,255,255,0.08);border-radius:12px;padding:12px;margin:8px 0;">
                <strong>{movie.get('title', 'Unknown')}</strong> 
                <span style="color:#a0a0c0;">({movie.get('year', 'N/A')})</span>
                <div style="margin:4px 0;">{genres_badges}</div>
                <p style="font-size:0.85em;color:#a0a0c0;margin:6px 0;">{overview}</p>
                <span style="font-size:0.8em;">⭐ {movie.get('rating', 'N/A')} 
                🕐 {movie.get('runtime', 'N/A')}</span>
            </div>"""

        html += (
            '<p style="font-size:0.75em;color:#666;margin-top:10px;">'
            "ℹ️ Running in local mode</p>"
        )
        return html

    def format_movie_context(self, movies_df):
        """Format movie dataframe into a context string for Gemini"""
        if movies_df is None or movies_df.empty:
            return "No movies found in the database matching the query."

        context_parts = []
        for _, movie in movies_df.iterrows():
            similarity_info = ""
            if "similarity" in movie and movie["similarity"]:
                similarity_info = (
                    f"  Relevance Score: {movie['similarity']:.2f}\n"
                )

            movie_text = f"""
MOVIE: {movie.get('title', 'Unknown')}
  Year: {movie.get('release_year', 'N/A')}
  Rating: {movie.get('vote_average', 'N/A')}/10 ({movie.get('vote_count', 0):,} votes)
  Runtime: {movie.get('runtime', 'N/A')} minutes
  Genres: {movie.get('genres', 'N/A')}
  Popularity: {movie.get('popularity', 'N/A')}
  Overview: {movie.get('overview', 'No description available.')}
  Tagline: {movie.get('tagline', 'N/A')}
  Keywords: {movie.get('keywords', 'N/A')}
  Poster: {movie.get('poster_path', '')}
{similarity_info}"""
            context_parts.append(movie_text)

        return "\n---\n".join(context_parts)