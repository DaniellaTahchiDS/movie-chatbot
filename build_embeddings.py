# build_embeddings.py
"""Run this once to pre-compute embeddings before starting the server"""
from chatbot.data_handler import MovieDataHandler

if __name__ == '__main__':
    print("Building movie embeddings...")
    handler = MovieDataHandler('data/movies.csv')
    print(f"Done! Processed {len(handler.df)} movies.")
    print("You can now run: python app.py")