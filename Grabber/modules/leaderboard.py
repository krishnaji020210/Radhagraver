from pyrogram import filters
from Grabber import app
from Grabber.core import script
from Grabber.core.mongo import waifusdb
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close_data")]])

@app.on_message(filters.command("leaderboard"))
async def leaderboard_handler(client, message):
    data = await waifusdb.getLeaderboard(10)
    if not data:
        await message.reply_text("No leaderboard data available yet.")
        return

    msg = await message.reply_photo(photo=script.PHOTOS["LEADERBOARD_IMG"], caption="Please Wait...")

    text = "🏆 Top 10 Waifu Hunters\n\n"
    for index, user in enumerate(data, start=1):
        medal = (
            "🥇" if index == 1 else
            "🥈" if index == 2 else
            "🥉" if index == 3 else
            "▫️"
        )

        try:
            tg_user = await client.get_users(int(user["user_id"]))
            name = tg_user.mention
        except:
            name = f"`{user['user_id']}`"

        text += f"{medal} {name} — {user['total_grabs']} grabs\n"
    await msg.edit_text(text, reply_markup=buttons)
