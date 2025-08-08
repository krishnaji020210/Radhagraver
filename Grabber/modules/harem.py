from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from Grabber import app
from Grabber.core.mongo.waifusdb import getUserAllWaifus

PER_PAGE = 10

def build_menu_buttons(user_id):
    buttons = [
        [
            InlineKeyboardButton("📜 Default", callback_data=f"harem_sort:default:{user_id}:0"),
            InlineKeyboardButton("🔠 Waifus (A-Z)", callback_data=f"harem_sort:waifus:{user_id}:0"),
            InlineKeyboardButton("🎬 Anime", callback_data=f"harem_sort:anime:{user_id}:0"),
            InlineKeyboardButton("💎 Rarity", callback_data=f"harem_sort:rarity:{user_id}:0")
        ],
        [
            InlineKeyboardButton("❌ Close", callback_data=f"harem_close:{user_id}")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def build_nav_buttons(sort_type, user_id, page):
    buttons = [
        [
            InlineKeyboardButton("⬅️ Prev", callback_data=f"harem_prev:{sort_type}:{user_id}:{page}"),
            InlineKeyboardButton("Next ➡️", callback_data=f"harem_next:{sort_type}:{user_id}:{page}")
        ],
        [
            InlineKeyboardButton("❌ Close", callback_data=f"harem_close:{user_id}")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

@app.on_message(filters.command("harem"))
async def harem_menu(_, message):
    user_id = message.from_user.id
    await message.reply(
        "✨ **Select how you want to view your harem:**",
        reply_markup=build_menu_buttons(user_id)
    )

async def send_harem_page(query, user_id, page, waifus, sort_type):
    total = len(waifus)
    start = page * PER_PAGE
    end = start + PER_PAGE
    page_waifus = waifus[start:end]
    shown_count = min(end, total)

    if sort_type == "anime":
        grouped = {}
        for w in waifus:
            anime_name = w.get("anime", "Unknown")
            grouped.setdefault(anime_name, []).append(w)
        grouped = dict(sorted(grouped.items(), key=lambda x: x[0].lower()))
        text = f"🎬 **Your Harem by Anime** ({shown_count}/{total})\n" + "─" * 30 + "\n"
        for anime, waifu_list in grouped.items():
            text += f"**{anime}** ({len(waifu_list)})\n"
            for w in waifu_list:
                text += (
                    f"🆔 **ID:** {w.get('_id', 'N/A')}\n"
                    f"👩 **Name:** {w.get('name', 'Unknown')}\n"
                    f"💎 **Rarity:** {w.get('rarity', 'Unknown')}\n"
                    + "─" * 20 + "\n"
                )
        photo_url = waifus[0].get('image', "https://via.placeholder.com/300") if waifus else "https://via.placeholder.com/300"
    else:
        text = f"💖 **Your Harem** ({shown_count}/{total})\n" + "─" * 30 + "\n"
        for w in page_waifus:
            text += (
                f"🆔 **ID:** {w.get('_id', 'N/A')}\n"
                f"👩 **Name:** {w.get('name', 'Unknown')}\n"
                f"🎬 **Anime:** {w.get('anime', 'Unknown')}\n"
                f"💎 **Rarity:** {w.get('rarity', 'Unknown')}\n"
                + "─" * 20 + "\n"
            )
        photo_url = page_waifus[0].get('image', "https://via.placeholder.com/300") if page_waifus else "https://via.placeholder.com/300"

    await query.message.edit_media(
        InputMediaPhoto(media=photo_url, caption=text),
        reply_markup=build_nav_buttons(sort_type, user_id, page)
    )

@app.on_callback_query(filters.regex(r"^harem_sort"))
async def harem_sort_handler(_, query):
    _, sort_type, user_id, page = query.data.split(":")
    user_id = int(user_id)
    page = int(page)
    waifus = await getUserAllWaifus(user_id)
    if not waifus:
        return await query.answer("❌ You don't have any waifus!", show_alert=True)
    if sort_type == "waifus":
        waifus = sorted(waifus, key=lambda x: x.get("name", "").lower())
    elif sort_type == "anime":
        waifus = sorted(waifus, key=lambda x: x.get("anime", "").lower())
    await send_harem_page(query, user_id, page, waifus, sort_type)

@app.on_callback_query(filters.regex(r"^harem_next"))
async def harem_next_handler(_, query):
    _, sort_type, user_id, page = query.data.split(":")
    user_id = int(user_id)
    page = int(page) + 1
    waifus = await getUserAllWaifus(user_id)
    if sort_type == "waifus":
        waifus = sorted(waifus, key=lambda x: x.get("name", "").lower())
    elif sort_type == "anime":
        waifus = sorted(waifus, key=lambda x: x.get("anime", "").lower())
    if page * PER_PAGE >= len(waifus):
        return await query.answer("🚫 No more pages!", show_alert=True)
    await send_harem_page(query, user_id, page, waifus, sort_type)

@app.on_callback_query(filters.regex(r"^harem_prev"))
async def harem_prev_handler(_, query):
    _, sort_type, user_id, page = query.data.split(":")
    user_id = int(user_id)
    page = int(page) - 1
    if page < 0:
        return await query.answer("⚠️ You're on the first page!", show_alert=True)
    waifus = await getUserAllWaifus(user_id)
    if sort_type == "waifus":
        waifus = sorted(waifus, key=lambda x: x.get("name", "").lower())
    elif sort_type == "anime":
        waifus = sorted(waifus, key=lambda x: x.get("anime", "").lower())
    await send_harem_page(query, user_id, page, waifus, sort_type)

@app.on_callback_query(filters.regex(r"^harem_close"))
async def harem_close_handler(_, query):
    await query.message.delete()


