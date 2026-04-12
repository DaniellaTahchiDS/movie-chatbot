# chatbot/engine.py
import os

# Auto-detect: use lite if sentence-transformers not available
try:
    if os.getenv("LITE_MODE", "false").lower() == "true":
        raise ImportError("Forced lite mode")
    from chatbot.data_handler import MovieDataHandler
    print("📦 Running in FULL mode (sentence-transformers)")
except ImportError:
    from chatbot.data_handler_lite import MovieDataHandler
    print("📦 Running in LITE mode (keyword search)")

from chatbot.gemini_client import GeminiClient


class ChatbotEngine:
    def __init__(self, csv_path="data/movies.csv"):
        print("Initializing chatbot engine...")
        self.data = MovieDataHandler(csv_path)
        self.gemini = GeminiClient()
        self.chat_histories = {}
        print("🚀 Chatbot ready!")

    def process(self, user_input, session_id="default"):
        if not user_input or not user_input.strip():
            return "<p>Please type a message! 😊</p>"

        if session_id not in self.chat_histories:
            self.chat_histories[session_id] = []

        movie_context = self._retrieve_context(user_input)

        response = self.gemini.generate_response(
            user_message=user_input,
            movie_context=movie_context,
            chat_history=self.chat_histories[session_id],
        )

        response = self._clean_response(response)

        self.chat_histories[session_id].append(
            {"user": user_input, "bot": response}
        )

        if len(self.chat_histories[session_id]) > 20:
            self.chat_histories[session_id] = self.chat_histories[session_id][-20:]

        return response

    def _retrieve_context(self, user_input):
        text = user_input.lower().strip()
        all_results = []

        import pandas as pd

        title_results = self._try_title_search(text)
        if not title_results.empty:
            all_results.append(title_results)

        genre_results = self._try_genre_search(text)
        if genre_results is not None and not genre_results.empty:
            all_results.append(genre_results)

        year_results = self._try_year_search(text)
        if year_results is not None and not year_results.empty:
            all_results.append(year_results)

        semantic_results = self.data.semantic_search(user_input, top_k=8)
        if semantic_results is not None and not semantic_results.empty:
            all_results.append(semantic_results)

        if all_results:
            combined = pd.concat(all_results).drop_duplicates(subset=["id"])
            combined = combined.head(15)
        else:
            combined = semantic_results

        general_keywords = [
            "best", "top", "recommend", "suggest",
            "favorite", "popular", "greatest",
        ]
        if any(kw in text for kw in general_keywords):
            top_rated = self.data.get_top_rated(10)
            combined = (
                pd.concat([combined, top_rated])
                .drop_duplicates(subset=["id"])
                .head(15)
            )

        return self.gemini.format_movie_context(combined)

    def _try_title_search(self, text):
        import pandas as pd
        results = pd.DataFrame()

        for _, movie in self.data.df.iterrows():
            title_lower = movie["title"].lower()
            if title_lower in text or text in title_lower:
                results = pd.concat([results, movie.to_frame().T])

                rec_keywords = ["similar", "like", "recommend", "suggest"]
                if any(kw in text for kw in rec_keywords):
                    similar = self.data.get_recommendations(movie["title"], 5)
                    if similar is not None:
                        results = pd.concat([results, similar])

        return results

    def _try_genre_search(self, text):
        genres = [
            "action", "adventure", "comedy", "crime", "drama",
            "fantasy", "horror", "mystery", "romance", "thriller",
            "science fiction", "sci-fi", "western", "animation",
            "documentary", "family", "war", "history",
        ]
        for genre in genres:
            if genre in text:
                search_genre = "science fiction" if genre == "sci-fi" else genre
                return self.data.search_by_genre(search_genre, top_k=10)
        return None

    def _try_year_search(self, text):
        import re
        range_match = re.search(r"(\d{4})\s*(?:to|and|-)\s*(\d{4})", text)
        if range_match:
            return self.data.search_by_year_range(
                int(range_match.group(1)), int(range_match.group(2))
            )
        year_match = re.search(r"\b(19\d{2}|20[0-2]\d)\b", text)
        if year_match:
            return self.data.search_by_year(int(year_match.group(1)))
        return None

    def _clean_response(self, response):
        if not response:
            return "<p>I couldn't generate a response. Please try again.</p>"
        response = response.strip()
        if response.startswith("```html"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        return response.strip()

    def clear_history(self, session_id="default"):
        if session_id in self.chat_histories:
            self.chat_histories[session_id] = []