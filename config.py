from os import getenv

API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_TOKEN = getenv("BOT_TOKEN", "8066896805:AAFH6UekFrbDcdhAYbYV71mBepTQ-GtAgOk")
OWNER_ID = list(map(int, getenv("OWNER_ID", "8462359928").split()))
SUDO_IDS = list(map(int, getenv("SUDO_IDS", "8462359928").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://uploader:g3UouNkbo1kZXCEL@cluster0.wzsxgoy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/DevsHubChat")
