import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    """Centralized configuration class for managing environment variables and system settings"""
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Model designations
    CHECKER_MODEL = "llama-3.3-70b-versatile"
    EXPLAINER_MODEL = "llama-3.3-70b-versatile"
    CHAT_PARTNER_MODEL = "llama-3.1-8b-instant"

    @classmethod
    def validate_config(cls):
        """Validate that all required API keys are present"""
        if not cls.GROQ_API_KEY:
            raise ValueError("Configuration Error: Missing GROQ_API_KEY in the environment/.env file.")