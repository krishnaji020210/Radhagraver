from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from Grabber import app
from Grabber.core.mongo.waifusdb import getUserAllWaifus, getAllWaifus

PER_PAGE = 10
RARITY_ORDER = ["Common", "Rare", "Epic", "Legendary", "Mythical"]

# -------------------------
# Helpers: build grouped pages (pages contain up to PER_PAGE waifus)
# -------------------------
def build_groups(user_waifus, all_waifus, mode):
    """
    Returns an ordered list of groups:
    [
      (group_key, [waifu_obj, ...], group_meta)
    ]
    group_key: string heading (anime name or rarity or 'All')
    group_meta: dict for additional counts (for anime: total_in_anime, for rarity: total_in_rarity)
    """
    # Prepare mapping for totals from all_waifus
    total_by_anime = {}
    total_by_rarity = {}
    for w in all_waifus:
        total_by_anime.setdefault(w["anime"], 0)
        total_by_anime[w["anime"]] += 1
        total_by_rarity.setdefault(w.get("rank", "Unknown").capitalize(), 0)
        total_by_rarity[w.get("rank", "Unknown").capitalize()] += 1

    groups = []
    if mode == "anime":
        # group user waifus by anime, alphabetical anime order
        anime_map = {}
        for w in user_waifus:
            anime_map.setdefault(w["anime"], []).append(w)
        for anime in sorted(anime_map.keys(), key=lambda s: s.lower()):
            items = sorted(anime_map[anime], key=lambda x: x["name"].lower())
            groups.append((anime, items, {"grabbed": len(items), "total": total_by_anime.get(anime, 0)}))
    elif mode == "rank":
        # group by rarity in RARITY_ORDER
        rank_map = {}
        for w in user_waifus:
            rank_map.setdefault(w.get("rank", "Unknown").capitalize(), []).append(w)
        for r in RARITY_ORDER:
            items = rank_map.get(r, [])
            if items:
                items = sorted(items, key=lambda x: x["name"].lower())
                groups.append((r, items, {"grabbed": len(items), "total": total_by_rarity.get(r, 0)}))
    elif mode == "waifu":
        # alphabetical single "All" group but keep each waifu as simple list
        items = sorted(user_waifus, key=lambda x: x["name"].lower())
        groups.append(("All", items, {"grabbed": len(items), "total": len(user_waifus)}))
    else:  # default (stored order)
        groups.append(("All", list(user_waifus), {"grabbed": len(user_waifus), "total": len(user_waifus)}))

    return groups

def paginate_groups(groups):
    """
    Build pages (list). Each page contains a list of (group_key, waifus_list_for_that_group_on_this_page, group_meta)
    Ensures each page has up to PER_PAGE waifus (headers included only when their group's waifus appear on page).
    """
    pages = []
    current_page = []
    current_count = 0

    for group_key, items, meta in groups:
        idx = 0
        while idx < len(items):
            remaining = PER_PAGE - current_count
            take = min(remaining, len(items) - idx)
            slice_items = items[idx: idx + take]

            # append group chunk to current_page
            current_page.append((group_key, slice_items, meta))

            current_count += take
            idx += take

            # if page full, push and reset
            if current_count >= PER_PAGE:
                pages.append(current_page)
                current_page = []
                current_count = 0

        # continue to next group (group header will be repeated on next page if its items continue)
    # push last page if non-empty
    if current_page:
        pages.append(current_page)

    # Ensure at least one page
    if not pages:
        pages = [[]]

    return pages

# -------------------------
# Render page text as user requested
# -------------------------
def render_page_text(paged_groups, page_index, total_user, total_all, mode):
    """
    paged_groups: list of (group_key, [waifu_objs], meta)
    returns formatted text as requested.
    """
    # Header for Default/Waifu: "Your'Harem (X/Y)"
    if mode in ("default", "waifu"):
        header = f"Your'Harem ({sum(len(chunk[1]) for chunk in paged_groups)}/{total_all})\n\n"
        lines = [header]
        # For each waifu in order within page, print Name: ... Anime: ... Rarity: ...
        for group_key, waifus, meta in paged_groups:
            for w in waifus:
                lines.append(f"Name : {w['name']}\nAnime : {w['anime']}\nRarity : {w.get('rank','Unknown').capitalize()}\n")
        return "\n".join(lines).rstrip()
    elif mode == "anime":
        # For each group: "Attack on Titan (5/10)" then waifus on that anime
        lines = []
        for group_key, waifus, meta in paged_groups:
            lines.append(f"{group_key} ({meta['grabbed']}/{meta['total']})")
            for w in waifus:
                lines.append(f"Name : {w['name']}\nRarity : {w.get('rank','Unknown').capitalize()}\n")
            lines.append("")  # blank between anime groups
        return "\n".join(lines).rstrip()
    else:  # rank
        lines = []
        for group_key, waifus, meta in paged_groups:
            lines.append(f"{group_key} ({meta['grabbed']}/{meta['total']})")
            for w in waifus:
                lines.append(f"Name : {w['name']}\nAnime : {w['anime']}\n")
            lines.append("")
        return "\n".join(lines).rstrip()

# -------------------------
# Buttons builder
# -------------------------
def build_keyboard(mode, page_idx, total_pages, uid):
    # Top mode buttons (so user can switch anytime)
    top = [
        InlineKeyboardButton("📜 Default", callback_data=f"harem|default|0|{uid}"),
        InlineKeyboardButton("💖 Waifu", callback_data=f"harem|waifu|0|{uid}"),
        InlineKeyboardButton("🎬 Anime", callback_data=f"harem|anime|0|{uid}"),
        InlineKeyboardButton("🏅 Rarity", callback_data=f"harem|rank|0|{uid}"),
    ]
    # Nav
    nav = []
    if page_idx > 0:
        nav.append(InlineKeyboardButton("⬅ Prev", callback_data=f"harem|{mode}|{page_idx-1}|{uid}"))
    # show page indicator (disabled style)
    nav.append(InlineKeyboardButton(f"Page {page_idx+1}/{total_pages}", callback_data=f"noop|{uid}"))
    if page_idx < total_pages - 1:
        nav.append(InlineKeyboardButton("Next ➡", callback_data=f"harem|{mode}|{page_idx+1}|{uid}"))
    # Close
    bottom = [InlineKeyboardButton("❌ Close", callback_data=f"harem_close|{uid}")]
    # Build rows
    rows = [top, nav, [bottom[0]]]
    return InlineKeyboardMarkup(rows)

# -------------------------
# Entry: initial "choose" message creation (button-only)
# -------------------------
@app.on_callback_query(filters.regex(r"^open_harem\|(\d+)$"))
async def open_harem_cb(_, cq):
    uid = int(cq.data.split("|")[1])
    # Only allow owner or the clicking user? We'll require same user to interact.
    if cq.from_user.id != uid:
        return await cq.answer("This button is for a different user.", show_alert=True)

    choose_text = "**ᴄʜᴏᴏsᴇ ᴏɴᴇ ᴏғ ᴡᴀʏs ᴛᴏ sᴏʀᴛ ʏᴏᴜʀ ʜᴀʀᴇᴍ**"
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📜 Default", callback_data=f"harem|default|0|{uid}"),
            InlineKeyboardButton("💖 Waifu", callback_data=f"harem|waifu|0|{uid}")
        ],
        [
            InlineKeyboardButton("🎬 Anime", callback_data=f"harem|anime|0|{uid}"),
            InlineKeyboardButton("🏅 Rarity", callback_data=f"harem|rank|0|{uid}")
        ],
        [InlineKeyboardButton("❌ Close", callback_data=f"harem_close|{uid}")]
    ])
    await cq.message.edit(choose_text, reply_markup=kb)
    await cq.answer()

# -------------------------
# Main harem handler (mode/page switching)
# -------------------------
@app.on_callback_query(filters.regex(r"^harem\|(\w+)\|(\d+)\|(\d+)$"))
async def harem_handler(_, cq):
    # data: harem|mode|page|uid
    parts = cq.data.split("|")
    mode = parts[1]        # default / waifu / anime / rank
    page_idx = int(parts[2])
    uid = int(parts[3])

    # interaction guard
    if cq.from_user.id != uid:
        return await cq.answer("This Harem view isn't yours.", show_alert=True)

    # fetch data
    user_waifus = await getUserAllWaifus(uid)   # list of dicts: {name, anime, rank, image?, waifu_id?}
    all_waifus = await getAllWaifus()

    if not user_waifus:
        return await cq.message.edit("❌ You don't have any waifus yet.")

    # build groups depending on mode
    groups = build_groups(user_waifus, all_waifus, mode)

    # convert groups to paged groups with PER_PAGE waifus each
    pages = paginate_groups(groups)
    total_pages = len(pages)

    # clamp page_idx
    if page_idx < 0:
        page_idx = 0
    if page_idx >= total_pages:
        page_idx = total_pages - 1

    paged_groups = pages[page_idx]  # list of (group_key, [waifu_objs], meta)
    # render text
    text = render_page_text(paged_groups, page_idx, len(user_waifus), len(all_waifus), mode)

    # Build keyboard
    kb = build_keyboard(mode, page_idx, total_pages, uid)

    # show top image: use first waifu of page if exists and if has image key
    first_waifu = None
    for gk, wlist, meta in paged_groups:
        if wlist:
            first_waifu = wlist[0]
            break

    # If message currently is "choose" state or text, edit it to show formatted text + keyboard
    # We'll prefer editing as text; if you want photo preview, you can replace edit with edit_media
    try:
        # include header overall for Default/Waifu at very top as they wanted:
        if mode in ("default", "waifu"):
            header_line = f"Your'Harem ({len(user_waifus)}/{len(all_waifus)})\n\n"
            final_text = header_line + text
        else:
            final_text = text

        # If first_waifu has image and we want to show as photo with caption:
        if first_waifu and first_waifu.get("image"):
            # try editing media if previous message is a photo; otherwise edit text to caption
            # We'll attempt edit_media; if fails (not a photo message), fallback to edit_text
            from pyrogram.types import InputMediaPhoto
            try:
                await cq.message.edit_media(
                    media=InputMediaPhoto(media=first_waifu["image"], caption=final_text),
                    reply_markup=kb
                )
            except Exception:
                await cq.message.edit(final_text, reply_markup=kb)
        else:
            await cq.message.edit(final_text, reply_markup=kb)

    except Exception:
        # Fallback: edit text only
        await cq.message.edit(text, reply_markup=kb)

    await cq.answer()

# -------------------------
# Close handler
# -------------------------
@app.on_callback_query(filters.regex(r"^harem_close\|(\d+)$"))
async def harem_close(_, cq):
    uid = int(cq.data.split("|")[1])
    if cq.from_user.id != uid:
        return await cq.answer("Not yours.", show_alert=True)
    try:
        await cq.message.delete()
    except:
        try:
            await cq.message.edit("Closed.", reply_markup=None)
        except:
            pass
    await cq.answer()


