import config
from Grabber import app, BOT_USERNAME, BOT_NAME
from pyrogram import filters, enums
from Grabber.core import script
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# -------------------------- Buttons -------------------------- #

buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Add to Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
    ],
    [
        InlineKeyboardButton("Support", url=config.SUPPORT_CHANNEL),
        InlineKeyboardButton("Guide", callback_data="guide_")
    ]
])

group_buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Add to Group", url=f"https://t.me/{BOT_USERNAME}?start=true")
    ]
])


# -------------------------- Start -------------------------- #

@app.on_message(filters.command("start"))
async def start_(_, message):
    name = message.from_user.mention
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply_photo(photo=script.PHOTOS["START_IMG"],                         
            caption=script.START_TEXT.format(name, BOT_NAME),
            reply_markup=buttons
        )
    else:
        await message.reply_photo(photo="https://graph.org/file/ffbaa6d0fe89bdf98886b-9760febe78f97be25e.jpg",
            caption=f"Hello everyone! I’m **{BOT_NAME}**, your anime collector companion, here to summon waifus from different universes. Add me to your group and let the collecting, trading, and competition begin!",
            reply_markup=group_buttons
        )

            
