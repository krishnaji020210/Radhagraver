from Grabber import app
from pyrogram import filters, enums
from Grabber.core import script, main_func
from Grabber.core.mongo import waifusdb
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ------------------------ Gift Command ------------------------ #

@app.on_message(filters.command("gift"))
async def gift_waifu(_, message):
    sender_id = message.from_user.id
    parts = message.text.split()

    if message.reply_to_message:
        if len(parts) != 2:
            return await message.reply_text("💡 <b>Reply with:</b>\n<code>/gift waifu_id</code>")

        waifu_id = parts[1]
        receiver = message.reply_to_message.from_user
        receiver_id = receiver.id
        name = receiver.mention

    else:
        if len(parts) != 3:
            return await message.reply_text("💡 <b>Usage:</b>\n<code>/gift user_id waifu_id</code>")

        receiver_id = parts[1]
        waifu_id = parts[2]
        try:
            receiver = await app.get_users(receiver_id)
            receiver_id = receiver.id
            name = receiver.mention
        except Exception:
            return await message.reply_text("🛑 User ID Not Found!")

    if sender_id == receiver_id:
        return await message.reply_text("🛑 You can't gift to yourself.")

    waifu_data = await waifusdb.getUserWaifu(sender_id, str(waifu_id))
    if not waifu_data:
        return await message.reply_text("🛑 <b>This waifu is not in your collection.</b>")

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🟢 Accept",
                    callback_data=f"gift_accept:{sender_id}:{receiver_id}:{waifu_id}",
                ),
                InlineKeyboardButton(
                    "🔴 Decline",
                    callback_data=f"gift_reject:{sender_id}:{receiver_id}:{waifu_id}",
                ),
            ]
        ]
    )

    caption = f"""
<b>OwO, {name} received a Waifu gift!</b>

<b>⬤ Waifu</b> : <code>{waifu_data['name']}</code>
<b>⬤ Anime</b> : <code>{waifu_data['anime']}</code>
<b>⬤ Rarity</b> : <code>{(await main_func.rank_definer(waifu_data['rank']))}</code>
<b>⬤ From</b> : {message.from_user.mention}

<i>Do you want to accept this gift?</i>
"""

    try:
        if message.chat.type == enums.ChatType.PRIVATE:
            await app.send_photo(receiver_id, photo=script.PHOTOS["GIFT_IMG"], caption=caption, reply_markup=buttons)
            await message.reply_text("✅ Gift request sent successfully.")
        else:
            await message.reply_photo(photo=script.PHOTOS["GIFT_IMG"], caption=caption, reply_markup=buttons)
    except Exception:
        await message.reply_text("🛑 <b>Couldn’t send gift. User may have privacy settings enabled.</b>")



# ------------------------ Gift Regex Callback ------------------------ #

@app.on_callback_query(filters.regex(r"gift_(accept|reject):(\d+):(\d+):(.+)"))
async def gift_confirm(_, query):
    click_id = query.from_user.id
    action, sender_id, receiver_id, waifu_id = query.data.split("_")[1].split(":")
    
    if click_id != int(receiver_id):
        return await query.answer("This is not for you", show_alert=True)
    
    if action == "accept":
        waifu_data = await waifusdb.getUserWaifu(int(sender_id), waifu_id)
        if not waifu_data:
            return await query.answer("🛑 Waifu no longer exists!", show_alert=True)

        await waifusdb.addUser_Waifu(receiver_id, waifu_data["waifu_id"], waifu_data["name"], waifu_data["anime"], waifu_data["image"], waifu_data["rank"], waifu_data["price"])
        await waifusdb.removeUserWaifu(int(sender_id), waifu_id)

        await query.message.edit_text(
            f"🎉 <b>Gift Accepted!</b>\n\n"
            f"<i>Now {waifu_data['name']} belongs to {query.from_user.first_name}</i> ❤️"
        )
    elif action == "reject":
        await query.message.edit_text(f"{query.from_user.first_name} does not want to accept your gift. They are not interested in receiving your gift.")



# ------------------------ Trade Command ------------------------ #

@app.on_message(filters.command("trade"))
async def gift_waifu(_, message):
    sender_id = message.from_user.id
    parts = message.text.split()

    if message.reply_to_message:
        if len(parts) != 2:
            return await message.reply_text("💡 <b>Reply with:</b>\n<code>/trade waifu_id</code>")

        waifu_id = parts[1]
        receiver = message.reply_to_message.from_user
        receiver_id = receiver.id
        name = receiver.mention

    else:
        if len(parts) != 3:
            return await message.reply_text("💡 <b>Usage:</b>\n<code>/trade user_id waifu_id</code>")

        receiver_id = parts[1]
        waifu_id = parts[2]
        try:
            receiver = await app.get_users(receiver_id)
            receiver_id = receiver.id
            name = receiver.mention
        except Exception:
            return await message.reply_text("🛑 User ID Not Found!")

    if sender_id == receiver_id:
        return await message.reply_text("🛑 You can't trade to yourself.")

    waifu_data = await waifusdb.getUserWaifu(sender_id, str(waifu_id))
    if not waifu_data:
        return await message.reply_text("🛑 <b>This waifu is not in your collection.</b>")

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🟢 Accept",
                    callback_data=f"trade_accept:{sender_id}:{receiver_id}:{waifu_id}",
                ),
                InlineKeyboardButton(
                    "🔴 Decline",
                    callback_data=f"trade_reject:{sender_id}:{receiver_id}:{waifu_id}",
                ),
            ]
        ]
    )

    caption = f"""
<b>🔄 Trade Offer Received!</b>

<b>✦ Waifu:</b> <code>{waifu_name}</code>
<b>✦ Anime:</b> <code>{waifu_anime}</code>
<b>✦ Rarity:</b> <code>{(await main_func.rank_definer(waifu_rank))}</code>
<b>✦ From:</b> {message.from_user.mention}

<i>{name}, do you accept this trade?</i>
"""

    try:
        if message.chat.type == enums.ChatType.PRIVATE:
            await app.send_photo(receiver_id, photo=script.PHOTOS["TRADE_IMG"], caption=caption, reply_markup=buttons)
            await message.reply_text("✅ Trade request has been sent to the user.")
        else:
            await message.reply_photo(photo=script.PHOTOS["TRADE_IMG"], caption=caption, reply_markup=buttons)
    except Exception:
        await message.reply_text("🛑 <b>Couldn’t send gift. User may have privacy settings enabled.</b>")


# ------------------------ Trade Regex Callback ------------------------ #

@app.on_callback_query(filters.regex(r"trade_(accept|reject):(\d+):(\d+):(.+)"))
async def gift_confirm(_, query):
    click_id = query.from_user.id
    action, sender_id, receiver_id, waifu_id = query.data.split("_")[1].split(":")
    
    if click_id != int(receiver_id):
        return await query.answer("This is not for you", show_alert=True)
    
    if action == "accept":
        waifu_data = await waifusdb.getUserWaifu(int(sender_id), waifu_id)
        if not waifu_data:
            return await query.answer("🛑 Waifu no longer exists!", show_alert=True)

        await waifusdb.addUser_Waifu(receiver_id, waifu_data["waifu_id"], waifu_data["name"], waifu_data["anime"], waifu_data["image"], waifu_data["rank"], waifu_data["price"])
        await waifusdb.removeUserWaifu(int(sender_id), waifu_id)

        await query.message.edit_text(
            f"✅ <b>Trade Accepted!</b>\n\n"
            f"<i>{waifu_data['name']} has now been traded to {query.from_user.first_name}.</i> 🤝"
        )
    elif action == "reject":
        await query.message.edit_text(f"🛑 <b>Trade Declined!</b>\n\n<i>{query.from_user.first_name} is not interested in this trade offer.</i>")
