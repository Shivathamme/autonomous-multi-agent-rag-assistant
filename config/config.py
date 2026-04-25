import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model
GROQ_MODEL = "llama-3.1-8b-instant"

# Validation
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")