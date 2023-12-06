import os

from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.environ.get("BOT_TOKEN")

ADMIN_ID = os.environ.get("ADMIN_ID")
MODERATOR_ID = os.environ.get("MODERATOR_ID")
TECH_SUPPORT_ID = os.environ.get("TECH_SUPPORT_ID")

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

POSTS_CHANNEL_ID = int(os.environ.get("POSTS_CHANNEL_ID"))
USERNAME_USER_BOT = os.environ.get("USERNAME_USER_BOT")

SUPER_ADMIN_PASSWORD = os.environ.get("ADMIN_PASS")


