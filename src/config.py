import os
from dotenv import load_dotenv

# Load environment variables from .env file and assign to variables
load_dotenv()

port = int(os.getenv("API_PORT"))
version = os.getenv("API_VERSION")
app_default_user = os.getenv("APP_DEFAULT_USER")
app_default_token = os.getenv("APP_DEFAULT_TOKEN")
