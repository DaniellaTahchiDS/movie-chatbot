# 🎬 AI Movie Chatbot

<div align="center">

![Movie Chatbot Banner](https://img.shields.io/badge/🎬_Movie-Chatbot-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.1-000000?style=for-the-badge&logo=flask&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Render](https://img.shields.io/badge/Hosted_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

**An AI-powered movie chatbot that answers anything about movies —
cast, ratings, recommendations, comparisons, trivia, and more!**

[🚀 Live Demo](#) • [📖 Documentation](#how-it-works) • [🛠️ Installation](#getting-started) • [🤝 Contributing](#contributing)

</div>

---

## 📸 Preview


👤 Who are the main actors in Inception?

🤖 Inception (2010) features a stellar cast! ⭐ 8.364/10
   • 🎭 Leonardo DiCaprio — Dom Cobb
   • 🎭 Joseph Gordon-Levitt — Arthur  
   • 🎭 Elliot Page — Ariadne
   • 🎭 Tom Hardy — Eames
   • 🎭 Ken Watanabe — Saito
   Directed by Christopher Nolan, it's one of the most
   mind-bending films ever made!

👤 Compare The Dark Knight and Joker

🤖 Two incredible takes on Gotham's most iconic villain! 🃏

   🦇 The Dark Knight (2008) — ⭐ 8.512/10
   A large-scale crime epic where the Joker is an unstoppable
   agent of chaos against Batman and Gotham City...

   🃏 Joker (2019) — ⭐ 8.168/10  
   An intimate psychological character study following
   Arthur Fleck's descent into madness...

   Verdict: Dark Knight wins on rating and scale,
   Joker wins on raw character depth!


## ✨ Features

- 🤖 **AI Conversations** — Natural language powered by Google Gemini
- 🔍 **Smart Search** — Find movies by title, genre, year, or keyword
- 🎯 **Recommendations** — Get personalized movie suggestions
- 🎭 **Full Movie Knowledge** — Actors, directors, awards, box office, trivia
- 📊 **Rich Dataset** — Ratings, runtime, genres, popularity scores
- 💬 **Conversation Memory** — Remembers context within a session
- 🌐 **Web Interface** — Clean, responsive dark-themed chat UI
- ⚡ **RAG Architecture** — Retrieval-Augmented Generation for accurate answers
- 🆓 **100% Free** — Built entirely on free tiers (no paid APIs)

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML5, CSS3, JavaScript | Chat user interface |
| **Backend** | Python 3.11, Flask 3.1 | Web server & API routes |
| **AI Model** | Google Gemini 2.5 Flash Lite | Natural language generation |
| **Data Layer** | Pandas, CSV | Movie data storage & querying |
| **Search** | Sentence-Transformers / Keyword | Movie retrieval |
| **Architecture** | RAG (Retrieval-Augmented Generation) | Accurate AI responses |
| **Hosting** | Render (Free Tier) | Cloud deployment |
| **Storage** | GitHub + Git LFS | Code & large file storage |

---

## 📁 Project Structure

```
movie-chatbot/
│
├── 📄 app.py                      # Flask app — routes & server
├── 📄 Procfile                    # Render deployment config
├── 📄 runtime.txt                 # Python version spec
├── 📄 requirements.txt            # Python dependencies
├── 📄 build_embeddings.py         # One-time embedding builder
├── 📄 .gitignore                  # Git ignore rules
├── 📄 .gitattributes              # Git LFS tracking rules
│
├── 📂 chatbot/
│   ├── 📄 __init__.py             # Package init
│   ├── 📄 engine.py               # Core chatbot logic & RAG pipeline
│   ├── 📄 data_handler.py         # Full mode — sentence-transformers
│   ├── 📄 data_handler_lite.py    # Lite mode — keyword search (Render)
│   └── 📄 gemini_client.py        # Google Gemini API integration
│
├── 📂 data/
│   └── 📄 movies.csv              # Movie dataset (Git LFS tracked)
│
├── 📂 static/
│   ├── 📂 css/
│   │   └── 📄 style.css           # Dark theme UI styles
│   └── 📂 js/
│       └── 📄 chat.js             # Chat interface & API calls
│
└── 📂 templates/
    └── 📄 index.html              # Main chat page

```
---

## ⚙️ How It Works

The chatbot uses a **RAG (Retrieval-Augmented Generation)** architecture:
```

                        User sends a message
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Flask Backend      │
                    └──────────┬───────────┘
                               │
               ┌───────────────┴────────────────┐
               │                                │
               ▼                                ▼
   ┌───────────────────────┐      ┌─────────────────────────┐
   │   STEP 1: RETRIEVE    │      │      Movie Dataset       │
   │                       │◀────▶│      (movies.csv)        │
   │  • Title search       │      │                         │
   │  • Genre detection    │      │  Ratings, overviews,    │
   │  • Year extraction    │      │  genres, keywords,      │
   │  • Keyword matching   │      │  runtime, popularity    │
   │  • Semantic search    │      └─────────────────────────┘
   └───────────┬───────────┘
               │
               │  Top relevant movies as context
               ▼
   ┌───────────────────────┐      ┌─────────────────────────┐
   │   STEP 2: GENERATE    │      │   Google Gemini API     │
   │                       │─────▶│   (Free Tier)           │
   │  • CSV data facts     │      │                         │
   │  • Gemini's own know. │      │  gemini-2.5-flash-lite  │
   │  • Conversation hist. │      └─────────────────────────┘
   │  • System prompt      │
   └───────────┬───────────┘
               │
               ▼
        HTML Response
      displayed in chat UI

```
### Why RAG?

| Approach | Problem |
|---|---|
| Gemini alone | Doesn't know your specific dataset ratings/data |
| CSV alone | Can't have natural conversations |
| **RAG (Both)** ✅ | Accurate data + natural AI conversations |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Google Gemini API Key** — Free at [Google AI Studio](https://aistudio.google.com/apikey)
- **Hugging Face Token** — Free at [HuggingFace](https://huggingface.co/settings/tokens) *(optional)*
- **Git LFS** — For large CSV file — [git-lfs.com](https://git-lfs.com)

---

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/movie-chatbot.git
cd movie-chatbot
```

**2. Create a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the root folder:

```env
GEMINI_API_KEY=your_gemini_api_key_here
HF_TOKEN=your_huggingface_token_here
SECRET_KEY=your_random_secret_key_here
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

**5. Build semantic embeddings** *(first time only — skip in LITE_MODE)*

```bash
python build_embeddings.py
```

**6. Start the application**

```bash
python app.py
```

**7. Open in your browser**

```
http://localhost:5000
```

---

## 💬 What You Can Ask

| Category | Example Questions |
|---|---|
| 🎬 **Movie Info** | "Tell me about Inception" |
| 👥 **Cast** | "Who acts in The Dark Knight?" |
| 🎬 **Director** | "Who directed Interstellar?" |
| ⭐ **Ratings** | "What's the rating of Fight Club?" |
| 🕐 **Runtime** | "How long is Titanic?" |
| 🏆 **Awards** | "What awards did Titanic win?" |
| 🎯 **Recommendations** | "Movies similar to The Matrix" |
| 🔍 **Genre Search** | "Best sci-fi movies" |
| 📅 **Year Search** | "Top movies from 2014" |
| 📅 **Year Range** | "Best movies between 2010 and 2015" |
| 🔎 **Topic Search** | "Movies about time travel" |
| 📊 **Comparison** | "Compare Inception and Interstellar" |
| 🎵 **Trivia** | "Who composed the music for Interstellar?" |
| 💰 **Box Office** | "How much did Avatar make?" |
| 🏆 **Top Lists** | "Best rated movies of all time" |
| 🔥 **Popular** | "Most popular movies right now" |

---

## 🔑 Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | — | Google Gemini API key |
| `HF_TOKEN` | ⚠️ Optional | — | Hugging Face token for faster downloads |
| `SECRET_KEY` | ✅ Yes | fallback string | Flask session encryption key |
| `LITE_MODE` | ⚠️ Optional | `false` | Set `true` for low-RAM environments |
| `FLASK_ENV` | ⚠️ Optional | `development` | Set `production` when deployed |
| `PORT` | ⚠️ Optional | `5000` | Port number (auto-set by Render) |

---

## 🌐 Deployment on Render

### Step 1 — Push to GitHub with Git LFS

```bash
# Install and initialize Git LFS
git lfs install
git lfs track "data/movies.csv"

# Push to GitHub
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/movie-chatbot.git
git push -u origin main
```

### Step 2 — Create Web Service on Render

```
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select your "movie-chatbot" repository
5. Configure:
```

| Setting | Value |
|---|---|
| **Name** | `movie-chatbot` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120` |
| **Instance Type** | `Free` |

### Step 3 — Add Environment Variables on Render

```
GEMINI_API_KEY  →  your_gemini_api_key
HF_TOKEN        →  your_hf_token
SECRET_KEY      →  your_secret_key
LITE_MODE       →  true
FLASK_ENV       →  production
```

### Step 4 — Deploy 🚀

Click **"Create Web Service"** and wait ~5 minutes.

Your app will be live at:
```
https://movie-chatbot.onrender.com
```

### Auto-Deploy on Push

Every time you push to GitHub, Render automatically rebuilds:

```bash
git add .
git commit -m "Update feature"
git push
# Render rebuilds automatically ✅
```

---

## ⚠️ Known Limitations

| Limitation | Details |
|---|---|
| 😴 **Cold Start** | Free Render tier sleeps after 15 min inactivity. First request takes ~30-60s |
| 🔢 **API Rate Limits** | Gemini free tier: 15 requests/min, 1,500 requests/day |
| 💾 **RAM** | Free tier has 512MB RAM — runs in lite mode (keyword search) |
| 🎬 **Dataset Scope** | Movie coverage depends on your CSV dataset |
| 🔒 **Sessions** | Chat history is lost when the server restarts |

---

## 🔮 Future Improvements

- [ ] Stream Gemini responses in real-time (typing effect)
- [ ] Display movie poster images inside the chat
- [ ] Add user login and saved watchlists
- [ ] Expand dataset with more movies
- [ ] Add voice input support
- [ ] Implement response caching for common queries
- [ ] Support multiple languages
- [ ] Add a movie trailer preview feature
- [ ] Dark/Light theme toggle

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 DT
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Acknowledgments

- [Google Gemini](https://deepmind.google/technologies/gemini/) — Free AI API
- [TMDB](https://www.themoviedb.org/) — Movie database & poster images
- [Sentence Transformers](https://www.sbert.net/) — Semantic search model
- [Hugging Face](https://huggingface.co/) — Model hosting
- [Render](https://render.com) — Free cloud hosting
- [Flask](https://flask.palletsprojects.com/) — Python web framework

---

<div align="center">

**Built with ❤️ for movie lovers**

⭐ Star this repo if you found it helpful!

</div>
