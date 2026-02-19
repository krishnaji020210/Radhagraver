import asyncio
import os
from pyromod import listen
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN


# ---------------------------------------------------------------- #

loop = asyncio.get_event_loop()

# ----------------------------- App-Client ----------------------------- #
app = Client(":WaifuGrabber:", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

BOT_ID = BOT_NAME = BOT_USERNAME = None

# ----------------------------Bot-Info---------------------------- #
async def start_app():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await app.start()
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    BOT_NAME = f"{getme.first_name} {getme.last_name}" if getme.last_name else getme.first_name
    print(f"Bot started as @{BOT_USERNAME}")

loop.run_until_complete(start_app())

# ---------------------------------------------------------------- #
