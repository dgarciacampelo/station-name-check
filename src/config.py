import os
from dotenv import load_dotenv

service_name: str = "Station name check"

# Load environment variables from .env file and assign to variables
load_dotenv()

port = int(os.getenv("API_PORT"))
version = os.getenv("API_VERSION")
app_default_user = os.getenv("APP_DEFAULT_USER")
app_default_token = os.getenv("APP_DEFAULT_TOKEN")

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_notices_chat_id = os.getenv("TELEGRAM_NOTICES_CHAT_ID")
telegram_backups_chat_id = os.getenv("TELEGRAM_BACKUPS_CHAT_ID")
