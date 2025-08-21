from os import getenv

API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_TOKEN = getenv("BOT_TOKEN", "7998796312:AAEsHYM445NTHD8W1qGi-v-yIphz2rjmLFo")
OWNER_ID = list(map(int, getenv("OWNER_ID", "8075872851").split()))
SUDO_ID = list(map(int, getenv("SUDO_ID", "8075872851").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://SugoiRealm:SugoiRealm@cluster0.bsl4idz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "https://t.me/DevsLaboratory")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/DevsHubChat")
