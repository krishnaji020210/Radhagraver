import motor, sys, time
from Grabber import app
from config import OWNER_ID
from pyrogram import filters
from Grabber.core.mongo import usersdb, waifusdb, chatsdb


# --------------------------------------- Chat Watcher --------------------------------------- #

start_time = time.time()

@app.on_message(group=10)
async def chat_watcher_func(_, message):
    try:
        # ---------------- User Save ---------------- #
        if message.from_user:
            user_id = message.from_user.id
            if not await usersdb.is_user_exist(user_id):
                await usersdb.add_user(user_id)

        # ---------------- Chat Save ---------------- #
        if message.chat:
            chat_id = message.chat.id
            if not await chatsdb.is_chat_exist(chat_id):
                await chatsdb.add_chat(chat_id)
    except Exception:
        pass


# --------------------------------------- Bot Running Time --------------------------------------- #

def time_formatter():
    minutes, seconds = divmod(int(time.time() - start_time), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w:") if weeks else "")
        + ((str(days) + "d:") if days else "")
        + ((str(hours) + "h:") if hours else "")
        + ((str(minutes) + "m:") if minutes else "")
        + ((str(seconds) + "s") if seconds else "")
    )
    if tmp != "":
        if tmp.endswith(":"):
            return tmp[:-1]
        else:
            return tmp
    else:
        return "0 s"

# --------------------------------------- Stats Command --------------------------------------- #

@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message):
    start = time.time()
    users = len(await usersdb.get_all_users())
    chats = len(await chatsdb.get_all_chats())
    waifus = len(await waifusdb.getAllWaifus())
    ping = round((time.time() - start) * 1000)
    await message.reply_text(f"""
**Stats of** {(await client.get_me()).mention} :

🏓 **Ping Pong**: {ping}ms
📊 **Total Users** : `{users}`
🌼 **Total Chats**: `{chats}`
💮 **Total Waifus**: `{waifus}`
⚙️ **Bot Uptime** : `{time_formatter()}`
    
🎨 **Python Version**: `{sys.version.split()[0]}`
📑 **Mongo Version**: `{motor.version}`
""")


