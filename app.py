# app.py
import os
import uuid
from flask import Flask, render_template, request, jsonify, session
from chatbot import ChatbotEngine

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "movie-chatbot-secret-key")

bot = ChatbotEngine(csv_path="data/movies.csv")


@app.route("/")
def home():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    session_id = session.get("session_id", "default")
    response = bot.process(user_message, session_id=session_id)
    return jsonify({"response": response})


@app.route("/clear", methods=["POST"])
def clear():
    session_id = session.get("session_id", "default")
    bot.clear_history(session_id)
    return jsonify({"status": "cleared"})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "movies": len(bot.data.df)})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV") != "production"
    app.run(debug=debug, host="0.0.0.0", port=port)