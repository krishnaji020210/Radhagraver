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
async def paginate_waifus(client, query):
    replie_id = query.message.reply_to_message.from_user.id
    user_id = query.from_user.id
    
    if user_id != replie_id:
        return await query.answer("This is not for you!!", show_alert=True)
        
    direction, page = query.data.split("_")[1:]
    page = int(page)
    waifus = await getUserAllWaifus(user_id)

    if not waifus:
        return await query.answer("No waifus found.", show_alert=True)

    text = await format_waifus_list(waifus, page=page)  # ✅ await the async function
    buttons = get_buttons(page, len(waifus))
    top_image = waifus[page * 5]["image"] if len(waifus) > page * 5 else waifus[-1]["image"]

    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=top_image, caption=text),
            reply_markup=buttons
        )
    except Exception as e:
        await query.answer("Failed to update page.", show_alert=True)

                                                                                 
@app.on_callback_query(filters.regex("waifus_close"))
async def close_waifus(client, query):
    replie_id = query.message.reply_to_message.from_user.id
    click_id = query.from_user.id
    
    if click_id != replie_id:
        return await query.answer("This is not for you!!", show_alert=True)
        
    await query.message.delete()

    
