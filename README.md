```markdown
# 🎬 Movie Chatbot

An AI-powered movie chatbot built with **Flask**, **Google Gemini AI**, and **Pandas**. Ask anything about movies — cast, ratings, recommendations, comparisons, trivia, and more!

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1.1-black?logo=flask)
![Gemini](https://img.shields.io/badge/Google_Gemini-AI-orange?logo=google)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Demo

> Ask me anything about movies!

| Question | Answer |
|---|---|
| "Who directed Inception?" | Christopher Nolan |
| "Best sci-fi movies?" | Top rated sci-fi from database |
| "Compare Dark Knight vs Joker" | Detailed AI comparison |
| "Movies like Interstellar?" | Similar movie recommendations |
| "Who acts in Fight Club?" | Brad Pitt, Edward Norton... |

---

## ✨ Features

- 🤖 **AI-Powered** — Natural conversations using Google Gemini
- 🔍 **Smart Search** — Find movies by title, genre, year, keyword
- 🎯 **Recommendations** — Get similar movie suggestions
- 📊 **Rich Data** — Ratings, runtime, genres, vote counts
- 💬 **Conversation Memory** — Remembers context within a session
- 🎭 **General Knowledge** — Actors, directors, awards, trivia
- 📱 **Responsive UI** — Works on desktop and mobile
- ⚡ **Fast** — Lightweight keyword search for retrieval

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML, CSS, JavaScript (Vanilla) |
| **Backend** | Python, Flask |
| **AI Model** | Google Gemini 2.5 Flash Lite (Free Tier) |
| **Data** | Pandas, CSV Dataset |
| **Search** | Keyword-based + Semantic Search |
| **Embeddings** | Sentence-Transformers (local) |
| **Hosting** | Render (Free Tier) |
| **Version Control** | GitHub + Git LFS |

---

## 📁 Project Structure

```
movie-chatbot/
│
├── app.py                      # Flask application & routes
├── Procfile                    # Render deployment config
├── runtime.txt                 # Python version
├── requirements.txt            # Dependencies
├── build_embeddings.py         # One-time embedding generation
├── .gitignore
│
├── chatbot/
│   ├── __init__.py
│   ├── engine.py               # Main chatbot logic (RAG)
│   ├── data_handler.py         # Full mode (sentence-transformers)
│   ├── data_handler_lite.py    # Lite mode (keyword search)
│   └── gemini_client.py        # Google Gemini API integration
│
├── data/
│   └── movies.csv              # Movie dataset (tracked via Git LFS)
│
├── static/
│   ├── css/
│   │   └── style.css           # Dark theme UI styles
│   └── js/
│       └── chat.js             # Chat interface logic
│
└── templates/
    └── index.html              # Chat web interface
```

---

## ⚙️ How It Works

```
User Message
     │
     ▼
┌────────────────────┐
│   Flask Backend    │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐     ┌─────────────────────┐
│  Data Retrieval    │────▶│  Movie Dataset CSV   │
│  - Title search    │     │  (Pandas)            │
│  - Genre search    │     └─────────────────────┘
│  - Year search     │
│  - Keyword search  │
└────────┬───────────┘
         │
         │ Relevant movies as context
         ▼
┌────────────────────┐     ┌─────────────────────┐
│  Gemini AI         │────▶│  Google Gemini API   │
│  RAG Generation    │     │  (Free Tier)         │
│  - Uses CSV data   │     └─────────────────────┘
│  - Uses own know.  │
│  - Conversation    │
│    history         │
└────────┬───────────┘
         │
         ▼
    HTML Response
     (Displayed in Chat UI)
```

### RAG (Retrieval-Augmented Generation)

1. **Retrieve** — Find relevant movies from CSV using keyword/semantic search
2. **Augment** — Pass those movies as context to Gemini
3. **Generate** — Gemini answers using both the retrieved data and its own knowledge

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Google Gemini API Key (free at [Google AI Studio](https://aistudio.google.com/apikey))
- Hugging Face Token (free at [HuggingFace](https://huggingface.co/settings/tokens)) *(optional)*

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/movie-chatbot.git
cd movie-chatbot
```

**2. Create and activate virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
HF_TOKEN=your_huggingface_token_here
SECRET_KEY=your_secret_key_here
```

**5. Build embeddings** *(first time only — for full mode)*

```bash
python build_embeddings.py
```

**6. Run the app**

```bash
python app.py
```

**7. Open in browser**

```
http://localhost:5000
```

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | Google Gemini API key |
| `HF_TOKEN` | ⚠️ Optional | Hugging Face token (faster downloads) |
| `SECRET_KEY` | ✅ Yes | Flask session secret key |
| `LITE_MODE` | ⚠️ Optional | Set `true` for low-RAM hosting |
| `FLASK_ENV` | ⚠️ Optional | Set `production` for deployment |

---

## 💬 Example Conversations

```
👤 Who are the main actors in Inception?
🤖 Inception features an incredible ensemble cast:
    • Leonardo DiCaprio as Dom Cobb
    • Joseph Gordon-Levitt as Arthur
    • Elliot Page as Ariadne
    • Tom Hardy as Eames
    • Ken Watanabe as Saito
    It holds an impressive 8.364/10 rating!

👤 Compare The Dark Knight and Joker
🤖 Both are brilliant takes on Gotham's iconic villain:
    🦇 The Dark Knight (2008) — ⭐ 8.512/10
       An action-packed crime epic...
    🃏 Joker (2019) — ⭐ 8.168/10
       A psychological character study...

👤 Recommend something like Interstellar
🤖 Since you love Interstellar, try these:
    1. Inception (2010) — ⭐ 8.364
    2. The Matrix (1999) — ⭐ 8.206
    3. Gravity (2013) — mind-bending space adventure
```

---

## 🌐 Deployment

### Deploy to Render (Free)

**1. Push to GitHub**

```bash
git init
git lfs install
git lfs track "data/movies.csv"
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/movie-chatbot.git
git push -u origin main
```

**2. Create Web Service on Render**

- Go to [render.com](https://render.com) → New → Web Service
- Connect your GitHub repository
- Configure:

| Setting | Value |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120` |
| Instance Type | Free |

**3. Add Environment Variables on Render**

```
GEMINI_API_KEY  = your_key
HF_TOKEN        = your_token  
SECRET_KEY      = your_secret
LITE_MODE       = true
FLASK_ENV       = production
```

**4. Deploy** — Render auto-deploys on every `git push` 🚀

---

## 📊 Dataset

The movie dataset includes:

| Column | Description |
|---|---|
| `id` | Unique movie ID |
| `title` | Movie title |
| `release_year` | Year of release |
| `vote_average` | Average rating (0-10) |
| `vote_count` | Number of votes |
| `runtime` | Duration in minutes |
| `popularity` | Popularity score |
| `overview` | Plot summary |
| `tagline` | Movie tagline |
| `keywords` | Associated keywords |
| `genres` | Movie genres |
| `poster_path` | TMDB poster path |

> Dataset sourced from [TMDB](https://www.themoviedb.org/).

---

## ⚠️ Limitations

- 🔢 **Free Tier Rate Limits** — Gemini API: 15 requests/min, 1,500/day
- 😴 **Render Free Tier** — App sleeps after 15 min inactivity (first load ~30-60s)
- 💾 **RAM** — Lite mode uses keyword search instead of semantic embeddings
- 🎬 **Dataset Scope** — Only answers with high accuracy about movies in the dataset

---

## 🔮 Future Improvements

- [ ] Add more movies to the dataset
- [ ] Implement user authentication
- [ ] Add movie watchlist feature
- [ ] Stream Gemini responses in real-time
- [ ] Add voice input support
- [ ] Implement caching for common queries
- [ ] Add poster image display in chat
- [ ] Support multiple languages

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Google Gemini](https://deepmind.google/technologies/gemini/) — AI responses
- [TMDB](https://www.themoviedb.org/) — Movie data
- [Sentence Transformers](https://www.sbert.net/) — Semantic search
- [Render](https://render.com) — Free hosting
- [Flask](https://flask.palletsprojects.com/) — Web framework

---

<p align="center">
  Built with ❤️ for movie lovers
</p>
```
