from telethon import events, Button
from Grabber import tele
from collections import Counter
from Grabber.core.mongo import waifusdb  

waifu_per_page = 10

@tele.on(events.NewMessage(pattern="/mywaifus"))
async def my_waifus_handler(event):
    user_id = event.sender_id
    waifus = await waifusdb.getUser_Waifus(user_id)

    if not waifus:
        await event.reply("You don't own any waifus yet.")
        return

    await send_waifu_page(event, waifus, page=0)


def group_waifus(waifu_list):
    grouped = {}
    for w in waifu_list:
        key = (w["waifu_id"], w["name"], w["anime"], w["level"], w["image"])
        if key in grouped:
            grouped[key] += 1
        else:
            grouped[key] = 1
    return grouped


async def send_waifu_page(event, waifus, page=0):
    total = len(waifus)
    start = page * waifu_per_page
    end = start + waifu_per_page
    waifu_slice = waifus[start:end]

    if not waifu_slice:
        await event.reply("No waifus on this page.")
        return

    grouped = group_waifus(waifu_slice)
    caption = f"📦 **Your Waifus**\n**Showing**: {min(end, total)}/{total}\n\n"

    for (waifu_id, name, anime, level, image), count in grouped.items():
        caption += (
            f"👤 **{name} × {count}**\n"
            f"📺 **Anime**: {anime}\n"
            f"⭐ **Level**: {level}\n"
            f"🆔 `{waifu_id}`\n"
            f"- - - - - - - - - - - -\n"
        )

    top_image = list(grouped.keys())[0][4]

    buttons = []
    if page > 0:
        buttons.append(Button.inline("⏪ Prev", data=f"prev_{page}"))
    if end < total:
        buttons.append(Button.inline("⏩ Next", data=f"next_{page}"))
    buttons.append(Button.inline("✖ Close", data="close"))

    await event.respond(
        file=top_image,
        message=caption,
        buttons=[buttons],
        parse_mode="md"
    )


@tele.on(events.CallbackQuery(pattern=r"(next|prev)_(\d+)"))
async def paginate_waifus(event):
    action, page = event.pattern_match.group(1), int(event.pattern_match.group(2))
    user_id = event.sender_id

    waifus = await waifusdb.getUser_Waifus(user_id)
    if not waifus:
        await event.answer("No waifus found.")
        return

    new_page = page + 1 if action == "next" else page - 1
    await event.delete()
    await send_waifu_page(event, waifus, new_page)


@tele.on(events.CallbackQuery(pattern="close"))
async def close_page(event):
    await event.delete()


