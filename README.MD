# Reddit Chatbot

AI chatbot that answers questions based on subreddit content using Gemini.

## Features
- Reddit data scraping
- Semantic search with FAISS
- Google Gemini integration
- FastAPI web server

# Install dependencies
```bash
pip3 install -r requirements.txt
```
# Set up environment(for linux)
```bash
virtualenv my_env
```
# Edit .env with your credentials
create a .env file and add these contents to it:
```bash
# Reddit API 
REDDIT_CLIENT_ID=clientid
REDDIT_CLIENT_SECRET=clientsecret
REDDIT_USER_AGENT="name"

# Google Gemini API
GEMINI_API_KEY=gemini api key
GEMINI_MODEL=gemini-2.5-flash

# Application Settings
SUBREDDIT_NAME=subredditname
TOP_K_RESULTS=5
MAX_CONTEXT_LENGTH=3000
MAX_TOKENS=1024
TEMPERATURE=0.7
```

# Run data pipeline
python3 src/data_processing/reddit_loader.py
python src/data_processing/embedding_generator.py --input data/raw/yourfile.json

# Start chatbot
python -m src.chatbot.engine