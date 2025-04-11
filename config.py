from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# You can now use OPENAI_API_KEY and NEWS_API_KEY securely in your code
