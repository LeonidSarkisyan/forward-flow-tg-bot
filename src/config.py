import os

from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.environ.get("BOT_TOKEN")

ADMIN_ID = os.environ.get("ADMIN_ID")
MODERATOR_ID = os.environ.get("MODERATOR_ID")
TECH_SUPPORT_ID = os.environ.get("TECH_SUPPORT_ID")

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
