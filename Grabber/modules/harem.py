from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from Grabber import app
from Grabber.core.mongo.waifusdb import getUserAllWaifus

PER_PAGE = 10
RARITY_ORDER = ["Common", "Rare", "Epic", "Legendary", "Mythical"]

def build_menu_buttons(user_id):
    buttons = [
        [
            InlineKeyboardButton("📜 Default", callback_data=f"harem_sort:default:{user_id}:0"),
            InlineKeyboardButton("🔠 Waifus (A-Z)", callback_data=f"harem_sort:waifus:{user_id}:0"),
        ],[
            InlineKeyboardButton("🎬 Anime", callback_data=f"harem_sort:anime:{user_id}:0"),
            InlineKeyboardButton("💎 Rarity", callback_data=f"harem_sort:rarity:{user_id}:0")
        ],[
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

async def send_harem_page(query, user_id, name, page, waifus, sort_type):
    total = len(waifus)
    start = page * PER_PAGE
    end = start + PER_PAGE
    page_waifus = waifus[start:end]
    shown_count = min(end, total)

    if sort_type == "anime":
        grouped = {}
        for w in page_waifus:
            anime_name = w.get("anime", "Unknown")
            grouped.setdefault(anime_name, []).append(w)
        grouped = dict(sorted(grouped.items(), key=lambda x: x[0].lower()))
        text = f"📣 **{name}'s Harem by Anime** ({shown_count}/{total})\n"
        for anime, waifu_list in grouped.items():
            text += f"**{anime}** ({len(waifu_list)})\n" + "─" * 30 + "\n"
            for w in waifu_list:
                text += (
                    f"📑 **ID:** {w.get('waifu_id', 'N/A')}\n"
                    f"🧽️ **Name:** {w.get('name', 'Unknown')}\n"
                    f"🎭 **Rarity:** {w.get('rank', 'Unknown')}\n"
                    f"┈" * 30 + "\n"
                )
        photo_url = page_waifus[0].get('image', "https://via.placeholder.com/300") if page_waifus else "https://via.placeholder.com/300"

    elif sort_type == "rarity":
        grouped = {r: [] for r in RARITY_ORDER}
        for w in page_waifus:
            rarity = w.get("rank", "Unknown")
            if rarity not in grouped:
                grouped[rarity] = []
            grouped[rarity].append(w)
        text = f"🏵 **{name}'s Harem by Rarity** ({shown_count}/{total})\n" + "─" * 30 + "\n"
        for rarity in RARITY_ORDER:
            if grouped.get(rarity):
                text += f"**{rarity}** ({len(grouped[rarity])})\n"
                for w in grouped[rarity]:
                    text += (
                        f"📑 **ID:** {w.get('waifu_id', 'N/A')}\n"
                        f"🧽️ **Name:** {w.get('name', 'Unknown')}\n"
                        f"🧩 **Anime:** {w.get('anime', 'Unknown')}\n"
                        f"🎭 **Rarity:** {rarity}\n"
                        f"┈" * 30 + "\n"
                    )
        photo_url = page_waifus[0].get('image', "https://via.placeholder.com/300") if page_waifus else "https://via.placeholder.com/300"

    else:
        text = f"👒 **{name}'s Harem** ({shown_count}/{total})\n" + "─" * 30 + "\n"
        for w in page_waifus:
            text += (
                f"📑 **ID:** {w.get('waifu_id', 'N/A')}\n"
                f"🧽️ **Name:** {w.get('name', 'Unknown')}\n"
                f"🧩 **Anime:** {w.get('anime', 'Unknown')}\n"
                f"🎭 **Rarity:** {w.get('rank', 'Unknown')}\n"
                + "┈" * 30 + "\n"
            )
        photo_url = page_waifus[0].get('image', "https://via.placeholder.com/300") if page_waifus else "https://via.placeholder.com/300"

    await query.message.edit_media(
        InputMediaPhoto(media=photo_url, caption=text),
        reply_markup=build_nav_buttons(sort_type, user_id, page)
    )

@app.on_callback_query(filters.regex(r"^harem_sort"))
async def harem_sort_handler(_, query):
    await query.answer("⏳ Waito... fetching your waifus")
    _, sort_type, user_id, page = query.data.split(":")
    user_id = int(user_id)
    page = int(page)
    waifus = await getUserAllWaifus(user_id)
    if not waifus:
        return await query.answer("❌ You don't have any waifus!", show_alert=True)
    # Get user info to show name
    user = await app.get_users(user_id)
    display_name = user.first_name
    if user.username:
        display_name += f" (@{user.username})"
    if sort_type == "waifus":
        waifus = sorted(waifus, key=lambda x: x.get("name", "").lower())
    elif sort_type == "anime":
        waifus = sorted(waifus, key=lambda x: x.get("anime", "").lower())
    elif sort_type == "rarity":
        waifus = sorted(waifus, key=lambda x: RARITY_ORDER.index(x.get("rank", "Unknown")) if x.get("rank", "Unknown") in RARITY_ORDER else 999)
    await send_harem_page(query, user_id, display_name, page, waifus, sort_type)

@app.on_callback_query(filters.regex(r"^harem_next"))
async def harem_next_handler(_, query):
    _, sort_type, user_id, page = query.data.split(":")
    user_id = int(user_id)
    page = int(page) + 1
    waifus = await getUserAllWaifus(user_id)
    user = await app.get_users(user_id)
    display_name = user.first_name
    if user.username:
        display_name += f" (@{user.username})"
    if sort_type == "waifus":
        waifus = sorted(waifus, key=lambda x: x.get("name", "").lower())
    elif sort_type == "anime":
        waifus = sorted(waifus, key=lambda x: x.get("anime", "").lower())
    elif sort_type == "rarity":
        waifus = sorted(waifus, key=lambda x: RARITY_ORDER.index(x.get("rank", "Unknown")) if x.get("rank", "Unknown") in RARITY_ORDER else 999)
    if page * PER_PAGE >= len(waifus):
        return await query.answer("🚫 No more pages!", show_alert=True)
    await send_harem_page(query, user_id, display_name, page, waifus, sort_type)

@app.on_callback_query(filters.regex(r"^harem_prev"))
async def harem_prev_handler(_, query):
    _, sort_type, user_id, page = query.data.split(":")
    user_id = int(user_id)
    page = int(page) - 1
    if page < 0:
        return await query.answer("⚠️ You're on the first page!", show_alert=True)
    waifus = await getUserAllWaifus(user_id)
    user = await app.get_users(user_id)
    display_name = user.first_name
    if user.username:
        display_name += f" (@{user.username})"
    if sort_type == "waifus":
        waifus = sorted(waifus, key=lambda x: x.get("name", "").lower())
    elif sort_type == "anime":
        waifus = sorted(waifus, key=lambda x: x.get("anime", "").lower())
    elif sort_type == "rarity":
        waifus = sorted(waifus, key=lambda x: RARITY_ORDER.index(x.get("rank", "Unknown")) if x.get("rank", "Unknown") in RARITY_ORDER else 999)
    await send_harem_page(query, user_id, display_name, page, waifus, sort_type)


    
