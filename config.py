# config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

# Application Settings
APP_TITLE = "JobPulse - Labor Market Insights"
APP_ICON = "📊"
DEFAULT_LAYOUT = "wide"

# Data Cache Settings
CACHE_TTL = 600  # Time to live for cached data in seconds (10 minutes)

# Debug Mode
DEBUG = False  # Set to True to enable debug messages