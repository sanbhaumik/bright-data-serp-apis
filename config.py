"""
Configuration file for Competitive Intelligence Agent

Loads credentials from environment variables for security.
Never commit .env file to version control!
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bright Data SERP API Credentials (loaded from environment)
API_KEY = os.getenv('SERP_API_KEY')
ZONE = os.getenv('SERP_ZONE')

# Validate that required credentials are present
if not API_KEY:
    raise ValueError(
        "SERP_API_KEY environment variable is not set. "
        "Please create a .env file with your API credentials. "
        "See .env.example for template."
    )

if not ZONE:
    raise ValueError(
        "SERP_ZONE environment variable is not set. "
        "Please create a .env file with your zone name. "
        "See .env.example for template."
    )

# Default search parameters (can be overridden via environment variables)
DEFAULT_COUNTRY = os.getenv('DEFAULT_COUNTRY', 'us')
DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'en')