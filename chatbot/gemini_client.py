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

        # ══════════════════════════════════════════════════════════
        #  UPDATED SYSTEM PROMPT — More confident, gives real facts
        # ══════════════════════════════════════════════════════════
        self.system_prompt = """You are a world-class movie expert assistant with encyclopedic knowledge of cinema.

YOU KNOW EVERYTHING ABOUT MOVIES INCLUDING:
• Box office revenue and budgets (domestic, worldwide, opening weekend)
• Full cast and crew (actors, directors, producers, writers, composers)
• Awards won and nominations (Oscars, Golden Globes, BAFTAs, etc.)
• Behind-the-scenes trivia and production facts
• Critical reception and cultural impact
• Release dates, filming locations, studio information
• Sequels, prequels, franchises, and connected films
• Soundtrack and score details
• Historical context and legacy

RESPONSE RULES:

1. ALWAYS GIVE SPECIFIC FACTS AND NUMBERS.
   ❌ Wrong: "It was a huge box office success"
   ✅ Right: "It grossed $2.2 billion worldwide, making it the highest-grossing film of its time"

2. ALWAYS GIVE SPECIFIC NAMES.
   ❌ Wrong: "It had famous actors"
   ✅ Right: "It starred Leonardo DiCaprio, Kate Winslet, and Billy Zane"

3. NEVER BE VAGUE OR HEDGING.
   ❌ Wrong: "I don't have precise figures readily available"
   ❌ Wrong: "While I can't give exact numbers..."
   ❌ Wrong: "It was one of the highest..."
   ✅ Right: State the actual number/fact confidently

4. IF YOU KNOW IT, SAY IT DIRECTLY.
   You are an expert. Experts give direct answers with real data.

5. COMBINE DATABASE STATS WITH YOUR KNOWLEDGE.
   When the user asks about a movie, include:
   • Rating and votes from the database (if available)
   • AND relevant facts from your knowledge (cast, revenue, awards, etc.)

6. FORMATTING:
   • Use HTML tags: <strong>, <em>, <p>, <ul>, <li>, <h3>
   • Do NOT use markdown
   • Use emojis occasionally for warmth
   • Be enthusiastic but factual

7. FOR FINANCIAL QUESTIONS (budget, revenue, box office):
   Give the actual numbers you know. For example:
   • Titanic: Budget ~$200 million, Worldwide gross ~$2.2 billion
   • Avatar: Budget ~$237 million, Worldwide gross ~$2.9 billion
   • Avengers Endgame: Worldwide gross ~$2.8 billion

8. FOR AWARDS QUESTIONS:
   Give specific counts and names:
   • "Titanic won 11 Academy Awards including Best Picture and Best Director"
   • "The Dark Knight: Heath Ledger won posthumous Oscar for Best Supporting Actor"

9. NEVER SAY:
   • "I don't have that information"
   • "I can't give precise figures"
   • "While I don't have exact data..."
   • "Based on my database..." or "In my database..."
   • "From my knowledge..." or "According to my data..."
   Just state facts naturally like an expert would."""

    def generate_response(self, user_message, movie_context, chat_history=None):
        """Generate response using Gemini with movie context"""

        if not self.use_gemini:
            return self._local_response(user_message, movie_context)

        context_prompt = f"""{self.system_prompt}

MOVIE DATABASE INFO (use this for ratings, runtime, genres, popularity):
{movie_context}

USER QUESTION: {user_message}

Give a direct, factual answer. Include specific numbers, names, and facts.
Format in HTML. Be confident and precise."""

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
        """Fallback: Generate response locally without API"""
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
                "<p>Sorry, I couldn't find relevant information. "
                "Try asking differently! 🤔</p>"
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
        """Format movie dataframe into context string for Gemini"""
        if movies_df is None or movies_df.empty:
            return "No specific movie data available for this query."

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
{similarity_info}"""
            context_parts.append(movie_text)

        return "\n---\n".join(context_parts)
