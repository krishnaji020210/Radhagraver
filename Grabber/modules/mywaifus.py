from Grabber import app
from pyrogram import filters
from Grabber.core import main_func
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from Grabber.core.mongo.waifusdb import getUserAllWaifus



async def format_waifus_list(waifus, page=0, per_page=5):
    total = len(waifus)
    start = page * per_page
    end = start + per_page
    page_waifus = waifus[start:end]

    text = f"🏵 <b>Waifu Grab</b> - ({min(end, total)}/{total})\n━━━━━━━━━━━━━━━━━━\n"
    for w in page_waifus:
        text += (
            f"📑 <b>ID</b>: <code>{w['waifu_id']}</code>\n"
            f"🧽️ <b>Name</b>: {w['name']}\n"
            f"🧩 <b>Anime</b>: {w['anime']} - {w['grab_count']}x\n"
            f"🎭 <b>Rarity</b>: {(await main_func.rank_definer(w['rank']))}\n"
            f"┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈\n"
        )
    return text

def get_buttons(page, total, per_page=5):
    max_pages = (total - 1) // per_page
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton("﹤ Prev", callback_data=f"waifus_prev_{page-1}"))
    if page < max_pages:
        buttons.append(InlineKeyboardButton("Next ﹥", callback_data=f"waifus_next_{page+1}"))
    buttons.append(InlineKeyboardButton("☌ Close", callback_data="waifus_close"))
    return InlineKeyboardMarkup([buttons])

@app.on_message(filters.command("mywaifus"))
async def mywaifus_handler(client, message):
    user_id = message.from_user.id
    waifus = await getUserAllWaifus(user_id)
    if not waifus:
        return await message.reply("You don't own any waifus yet.")

    page = 0
    text = await format_waifus_list(waifus, page=page)  # ✅ await the async function
    buttons = get_buttons(page, len(waifus))
    top_image = waifus[0]["image"]

    await message.reply_photo(photo=top_image, caption=text, reply_markup=buttons)



@app.on_callback_query(filters.regex(r"waifus_(next|prev)_(\d+)"))
async def paginate_waifus(client, callback_query):
    direction, page = callback_query.data.split("_")[1:]
    page = int(page)
    user_id = callback_query.from_user.id
    waifus = await getUserAllWaifus(user_id)

    if not waifus:
        return await callback_query.answer("No waifus found.", show_alert=True)

    text = await format_waifus_list(waifus, page=page)  # ✅ await the async function
    buttons = get_buttons(page, len(waifus))
    top_image = waifus[page * 5]["image"] if len(waifus) > page * 5 else waifus[-1]["image"]

    try:
        await callback_query.message.edit_media(
            media=InputMediaPhoto(media=top_image, caption=text),
            reply_markup=buttons
        )
    except Exception as e:
        await callback_query.answer("Failed to update page.", show_alert=True)

@app.on_callback_query(filters.regex("waifus_close"))
async def close_waifus(client, callback_query):
    await callback_query.message.delete()

    
