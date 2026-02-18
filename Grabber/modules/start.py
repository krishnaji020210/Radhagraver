from Grabber import app
from pyrogram import filters

@app.on_message(filters.command("start"))
async def start_(_, message):
  await message.reply_text("Started !!")


