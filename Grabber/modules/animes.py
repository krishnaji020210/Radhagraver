import uuid
from pyrogram import filters
from Grabber import app
from Grabber.core import script
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQueryResultPhoto
from Grabber.core.mongo.waifusdb import getAllWaifus

# ------------------------- Animes List ------------------------- #

@app.on_message(filters.command("animes"))
async def anime_list(_, message):
    row1 = [InlineKeyboardButton(str(i), callback_data=f"anime_letter_{i}") for i in range(1, 6)]
    row2 = [InlineKeyboardButton(str(i), callback_data=f"anime_letter_{i}") for i in range(6, 10)]

    alpha_rows = [
        ["A", "B", "C", "D"],
        ["E", "F", "G", "H"],
        ["I", "J", "K", "L"],
        ["M", "N", "O", "P"],
        ["Q", "R", "S", "T"],
        ["U", "V", "W", "X"],
        ["Y", "Z"]
    ]
    alpha_buttons = [[InlineKeyboardButton(letter, callback_data=f"anime_letter_{letter}") for letter in row] for row in alpha_rows]
    close_btn = [InlineKeyboardButton("☌ ᴄʟᴏsᴇ", callback_data="close_data")]

    keyboard = [row1, row2] + alpha_buttons + [close_btn]

    await message.reply_photo(script.PHOTOS["ANIMED_IMG"],
        caption="**📚 Choose starting number or letter of anime name:**",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ------------------------- Regex Callbacks  ------------------------- #

@app.on_callback_query(filters.regex(r"anime_letter_(.+)"))
async def handle_letter_click(_, query: CallbackQuery):
    letter = query.data.split("_")[2].upper()
    await show_anime_page(query, letter, 0)

@app.on_callback_query(filters.regex(r"anime_list_(.+)_(\d+)"))
async def handle_anime_page(_, query: CallbackQuery):
    letter = query.data.split("_")[2].upper()
    page = int(query.data.split("_")[3])
    await show_anime_page(query, letter, page)

# ------------------------- Show Anime Page Func ------------------------- #

async def show_anime_page(query: CallbackQuery, letter: str, page: int):
    await query.answer()
    all_waifus = await getAllWaifus()

    anime_names = sorted(set(
        w["anime"] for w in all_waifus if w["anime"].upper().startswith(letter)
    ))

    if not anime_names:
        return await query.answer(f"😵 No anime found for `{letter}`. ", show_alert=True)

    per_page = 10
    start = page * per_page
    end = start + per_page
    total = len(anime_names)
    total_pages = (total - 1) // per_page + 1

    shown_animes = anime_names[start:end]

    buttons = [[InlineKeyboardButton(anime, callback_data=f"anime_click_{anime}")]
               for anime in shown_animes]

    nav_row = []

    if page > 0:
        nav_row.append(InlineKeyboardButton("﹤ ᴘʀᴇᴠ", callback_data=f"anime_list_{letter}_{page - 1}"))

    if end < total:
        nav_row.append(InlineKeyboardButton("ɴᴇxᴛ ﹥", callback_data=f"anime_list_{letter}_{page + 1}"))

    nav_row.append(InlineKeyboardButton("☌ ᴄʟᴏsᴇ ☌", callback_data="close_data"))

    if nav_row:
        buttons.append(nav_row)

    await query.message.edit(
        f"📺 **Animes starting with `{letter}`**\n"
        f"Showing: {start + 1} - {min(end, total)} of {total} ({len(shown_animes)}/{total})",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ------------------------- Animes Click Regex ------------------------- #

@app.on_callback_query(filters.regex(r"anime_click_(.+)"))
async def inline_hint_anime(_, query):
    anime = query.data.split("_", 2)[2]
    bot_username = (await app.get_me()).username
    await query.answer()

    await query.message.edit(
        f"🔍 Tap below to search waifus from **{anime}**:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🔎 ᴀʟʟ ᴡᴀɪғᴜs", switch_inline_query_current_chat=anime)],
            [InlineKeyboardButton("↺ ʙᴀᴄᴋ ↻", callback_data=f"anime_list_{anime[0].upper()}_0")]
        ])
    )


# ------------------------- Inline Photo Result ------------------------- #


@app.on_inline_query()
async def inline_search_anime(_, inline_query):
    query = inline_query.query.strip().lower()
    all_waifus = await getAllWaifus()

    if query:
        waifus_to_show = [
            w for w in all_waifus
            if query in w["anime"].lower()
        ]
    else:
        waifus_to_show = all_waifus[:50]

    if not waifus_to_show:
        await inline_query.answer(
            results=[
                InlineQueryResultPhoto(
                    id=str(uuid.uuid4()),
                    photo_url="https://i.ibb.co/YfZzMx4/sad-anime.jpg",
                    thumb_url="https://i.ibb.co/YfZzMx4/sad-anime.jpg",
                    title="No Waifus Found 💔",
                    caption=f"😢 No waifus found for \"{query}\".\nTry another anime name!"
                )
            ],
            cache_time=1
        )
        return

    results = []

    for waifu in waifus_to_show[:50]:
        results.append(
            InlineQueryResultPhoto(
                id=str(uuid.uuid4()), 
                photo_url=waifu["image"],
                thumb_url=waifu["image"],
                title=waifu["name"],   
                caption=(
                    f"👩🏻 Name: {waifu['name']}\n"
                    f"📺 Anime: {waifu['anime']}\n"
                    f"🏷️ Rank: {waifu['rank'].capitalize()}"
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("☌ ᴄʟᴏsᴇ ☌", callback_data="close_data")]
                ])
            )
        )

    await inline_query.answer(
        results=results,
        cache_time=1,
        is_gallery=True 
    )



