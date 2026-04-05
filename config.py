from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_BASE_URL = os.getenv("GITHUB_API_BASE_URL", "https://api.github.com")

if not GITHUB_TOKEN:
    raise EnvironmentError(
        "GITHUB_TOKEN is not set. Please copy .env.example to .env and add your token."
    )
