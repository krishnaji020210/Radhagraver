import asyncio
import logging
from pyrogram import Client
from pyromod import listen
from config import API_ID, API_HASH, BOT_TOKEN


loop = asyncio.get_event_loop()


app = Client(":Grabber:", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def Info_Grabber():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await app.start()
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name


loop.run_until_complete(Info_Grabber())


