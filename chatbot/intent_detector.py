# chatbot/intent_detector.py
import re

class IntentDetector:
    """
    Rule-based intent detection using keyword patterns.
    No API needed - runs entirely locally.
    """

    def __init__(self):
        self.patterns = {
            'recommend_similar': [
                r'(?:similar|like|recommend.*(?:based|like)|movies?\s*like)\s+(.+)',
                r'(?:if\s+i\s+liked?|i\s+(?:love|enjoy)(?:ed)?)\s+(.+?)[\.,\?]?\s*(?:what|which|recommend|suggest)',
                r'(?:suggest|recommend)\s+(?:something|movies?)\s+(?:similar|like)\s+(?:to\s+)?(.+)',
            ],
            'movie_details': [
                r'(?:tell\s+me\s+about|what\s+is|info(?:rmation)?\s+(?:about|on)|details?\s+(?:about|on|for)|describe)\s+(.+)',
                r'(?:what\'?s?|who\'?s?)\s+(.+?)(?:\s+about|\s+movie)?\??$',
            ],
            'search_genre': [
                r'(?:best|top|good|great|show|find|list|suggest|recommend)\s+(\w+)\s+(?:movies?|films?)',
                r'(\w+)\s+(?:movies?|films?)\s*\??$',
                r'(?:movies?|films?)\s+(?:in|of)\s+(?:the\s+)?(\w+)\s+(?:genre|category)',
            ],
            'search_year': [
                r'(?:movies?|films?)\s+(?:from|in|of)\s+(\d{4})',
                r'(?:best|top|good)\s+(?:movies?|films?)\s+(?:from|in|of)\s+(\d{4})',
                r'(\d{4})\s+(?:movies?|films?)',
            ],
            'search_year_range': [
                r'(?:movies?|films?)\s+(?:from|between)\s+(\d{4})\s+(?:to|and|-)\s+(\d{4})',
                r'(?:best|top)\s+(?:movies?|films?)\s+(?:from|between)\s+(\d{4})\s+(?:to|and|-)\s+(\d{4})',
            ],
            'top_rated': [
                r'(?:top|best|highest)\s*(?:rated|rating)',
                r'(?:best|greatest|top)\s+(?:movies?|films?)\s*(?:ever|of\s+all\s+time)?',
                r'highest\s+(?:rated|score)',
            ],
            'most_popular': [
                r'(?:most|very)\s+popular',
                r'popular\s+(?:movies?|films?)',
                r'trending',
            ],
            'search_keyword': [
                r'(?:movies?|films?)\s+(?:about|with|featuring|involving|related\s+to)\s+(.+)',
                r'(?:find|search|show|get)\s+(?:movies?|films?)\s+(?:about|with|featuring)\s+(.+)',
            ],
            'greeting': [
                r'^(?:hi|hello|hey|howdy|greetings|good\s+(?:morning|afternoon|evening)|yo|sup)\b',
            ],
            'help': [
                r'^(?:help|what\s+can\s+you\s+do|how\s+(?:do|does)\s+this\s+work|commands?|options?)',
                r'(?:what|how)\s+(?:can|do)\s+(?:you|i)',
            ],
            'stats': [
                r'(?:how\s+many|total|count|number\s+of)\s+(?:movies?|films?)',
                r'(?:stats?|statistics|dataset\s+info)',
            ],
            'rating_query': [
                r'(?:what(?:\'?s|\s+is))\s+(?:the\s+)?rating\s+(?:of|for)\s+(.+)',
                r'(?:how\s+(?:good|well)\s+(?:is|was))\s+(.+?)(?:\s+rated)?\??$',
                r'(?:rate|rating|score)\s+(?:of|for)\s+(.+)',
            ],
            'runtime_query': [
                r'(?:how\s+long\s+is|runtime\s+(?:of|for)|duration\s+(?:of|for)|length\s+(?:of|for))\s+(.+)',
            ],
        }

    def detect(self, user_input):
        """
        Returns: (intent, extracted_entities)
        """
        text = user_input.strip().lower()
        text = re.sub(r'["\']', '', text)  # Remove quotes

        # Check each intent pattern
        # Order matters - more specific first

        # Greeting
        for pattern in self.patterns['greeting']:
            if re.search(pattern, text, re.IGNORECASE):
                return 'greeting', {}

        # Help
        for pattern in self.patterns['help']:
            if re.search(pattern, text, re.IGNORECASE):
                return 'help', {}

        # Stats
        for pattern in self.patterns['stats']:
            if re.search(pattern, text, re.IGNORECASE):
                return 'stats', {}

        # Year range (check before single year)
        for pattern in self.patterns['search_year_range']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return 'search_year_range', {
                    'start_year': int(match.group(1)),
                    'end_year': int(match.group(2))
                }

        # Recommend similar
        for pattern in self.patterns['recommend_similar']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(1).strip().rstrip('?.!')
                return 'recommend_similar', {'title': title}

        # Rating query
        for pattern in self.patterns['rating_query']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(1).strip().rstrip('?.!')
                return 'rating_query', {'title': title}

        # Runtime query
        for pattern in self.patterns['runtime_query']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(1).strip().rstrip('?.!')
                return 'runtime_query', {'title': title}

        # Movie details
        for pattern in self.patterns['movie_details']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(1).strip().rstrip('?.!')
                # Filter out generic words that aren't titles
                if title not in ['a movie', 'this', 'that', 'it', 'the movie',
                                 'your favorite', 'the best']:
                    return 'movie_details', {'title': title}

        # Search by year
        for pattern in self.patterns['search_year']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return 'search_year', {'year': int(match.group(1))}

        # Top rated
        for pattern in self.patterns['top_rated']:
            if re.search(pattern, text, re.IGNORECASE):
                return 'top_rated', {}

        # Most popular
        for pattern in self.patterns['most_popular']:
            if re.search(pattern, text, re.IGNORECASE):
                return 'most_popular', {}

        # Search by genre
        for pattern in self.patterns['search_genre']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                genre = match.group(1).strip()
                valid_genres = ['action', 'adventure', 'comedy', 'crime', 'drama',
                               'fantasy', 'horror', 'mystery', 'romance', 'thriller',
                               'science fiction', 'sci-fi', 'western', 'animation',
                               'documentary', 'family', 'war', 'history', 'music']
                if genre.lower() in valid_genres:
                    if genre.lower() == 'sci-fi':
                        genre = 'science fiction'
                    return 'search_genre', {'genre': genre}

        # Search by keyword (broad catch)
        for pattern in self.patterns['search_keyword']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                keyword = match.group(1).strip().rstrip('?.!')
                return 'search_keyword', {'keyword': keyword}

        # Fallback: semantic search
        return 'semantic_search', {'query': text}