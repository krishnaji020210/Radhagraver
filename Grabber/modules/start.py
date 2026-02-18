from Grabber import app
from pyrogram import filters

@app.on_message(filters.command("start"))
async def start_(_, message):
  await messsage.reply_text("Started !!")


