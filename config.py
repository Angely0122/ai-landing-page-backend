import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
    AZURE_DEPLOYMENT_ID = os.getenv("AZURE_DEPLOYMENT_ID")
    MONGODB_URI = os.getenv("MONGODB_URI")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

settings = Settings()