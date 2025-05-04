"""
Configuration settings for the JobPulse application
"""

# MongoDB Configuration
#password need to be written in the connection string
# Replace 'password' with the actual password for the MongoDB user
MONGO_CONNECTION_STRING = "mongodb+srv://Phase2_ADT:password2504@phase2cluster.svnfuwt.mongodb.net/"
MONGO_DB_NAME = "h1b_db"
MONGO_COLLECTION_NAME = "applications"

# Application Settings
APP_TITLE = "JobPulse - Labor Market Insights"
APP_ICON = "📊"
DEFAULT_LAYOUT = "wide"

# Data Cache Settings
CACHE_TTL = 600  # Time to live for cached data in seconds (10 minutes)

# Debug Mode
DEBUG = False  # Set to True to enable debug messages