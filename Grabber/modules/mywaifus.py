from telethon import events, Button
from Grabber.core.mongo.waifusdb import getUser_Waifus
from collections import Counter


# Group waifus by ID, name, etc.
def group_waifus(waifus):
    grouped = {}
    for w in waifus:
        key = (w["waifu_id"], w["name"], w["anime"], w["level"], w["image"])
        if key in grouped:
            grouped[key] += 1
        else:
            grouped[key] = 1
    return grouped


# Format waifus list for display
def format_waifus(grouped, page=0, per_page=10):
    grouped_items = list(grouped.items())
    total = len(grouped_items)
    start = page * per_page
    end = start + per_page
    page_items = grouped_items[start:end]

    text = f"\ud83d\udce6 <b>Your Waifus</b>\n\n<b>Showing</b>: {min(end, total)}/{total}\n\n"

    for (waifu_id, name, anime, level, image), count in page_items:
        text += f"\ud83d\udc64 <b>{name} \u00d7 {count}</b>\n\ud83d\udcbc <b>Anime</b>: {anime}\n\u2b50 <b>Level</b>: {level}\n\ud83c\udd1a <code>{waifu_id}</code>\n"
        text += "- - - - - - - - - - - -\n"

    return text


# Create inline buttons for pagination
def waifu_buttons(page, total, per_page=10):
    max_pages = (total - 1) // per_page
    buttons = []

    if page > 0:
        buttons.append(Button.inline("\u2b05\ufe0f Prev", f"waifus_prev_{page-1}"))
    if page < max_pages:
        buttons.append(Button.inline("Next \u27a1\ufe0f", f"waifus_next_{page+1}"))

    buttons.append(Button.inline("\u274c Close", "waifus_close"))
    return buttons


# Command: /mywaifus
@bot.on(events.NewMessage(pattern="/mywaifus"))
async def show_mywaifus(event):
    user_id = event.sender_id
    waifus = await getUser_Waifus(user_id)

    if not waifus:
        return await event.reply("\ud83d\ude97 You don't own any waifus yet.")

    grouped = group_waifus(waifus)
    text = format_waifus(grouped, page=0)
    total = len(grouped)
    buttons = waifu_buttons(0, total)
    top_image = list(grouped.keys())[0][4]

    await event.reply(text, file=top_image, buttons=buttons)


# Callback: next/prev
@bot.on(events.CallbackQuery(pattern=r"waifus_(next|prev)_(\d+)"))
async def paginate_waifus(event):
    _, direction, page = event.pattern_match.string.split("_")
    page = int(page)
    user_id = event.sender_id
    waifus = await getUser_Waifus(user_id)

    grouped = group_waifus(waifus)
    total = len(grouped)
    text = format_waifus(grouped, page=page)
    buttons = waifu_buttons(page, total)
    image = list(grouped.keys())[page * 10][4] if total > page * 10 else None

    await event.edit(text, file=image, buttons=buttons)


# Callback: close
@bot.on(events.CallbackQuery(pattern="waifus_close"))
async def close(event):
    await event.delete()
