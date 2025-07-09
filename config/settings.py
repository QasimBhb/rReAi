import os
from dotenv import load_dotenv

load_dotenv()

# Reddit API Configuration
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest")

# Application Parameters
SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME", "askreddit")
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 5))
MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", 3000))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 1024))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))

# Path Configuration
DATA_RAW_PATH = "data/raw"
DATA_PROCESSED_PATH = "data/processed"
EMBEDDINGS_PATH = os.path.join(DATA_PROCESSED_PATH, "embeddings")