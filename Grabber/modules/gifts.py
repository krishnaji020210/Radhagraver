from Grabber import app
from pyrogram import filters, enums
from Grabber.core import script, main_func
from Grabber.core.mongo import waifusdb
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ------------------------ Gift Command ------------------------ #

@app.on_message(filters.command("gift"))
async def gift_waifu(_, message):
    sender_id = message.from_user.id

    if message.reply_to_message:
        try:
            waifu_id = message.text.split(None, 1)[1]
        except IndexError:
            return await message.reply_text("💡 <b>Reply to someone's message with:</b>\n<code>/gift waifu_id</code>")
        receiver_id = message.reply_to_message.from_user.id
        name = message.reply_to_message.from_user.mention
    else:
        try:
            _, receiver_id, waifu_id = message.text.split(None, 2)
            try:
                user_data = await app.get_users(receiver_id)
                name = user_data.mention()
                receiver_id = user_data.id
            except:
                await message.reply_text("User ID Not Found!!")
        except ValueError:
            return await message.reply_text(
                "💡 <b>Correct usage:</b>\n<code>/gift receiver_id waifu_id</code>\n"
                "OR reply to the user with:\n<code>/gift waifu_id</code>"
            )

    waifu_data = await waifusdb.getUserWaifu(sender_id, str(waifu_id))
    if not waifu_data or waifu_data["waifu_id"] != str(waifu_id):
        return await message.reply_text("❌ <b>This waifu is not in your collection.</b>")

    waifu_name = waifu_data["name"]
    waifu_anime = waifu_data["anime"]
    waifu_rank = waifu_data["rank"] 
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🟢 Accept", callback_data=f"gift_yes:{sender_id}:{receiver_id}:{waifu_id}"),
            InlineKeyboardButton("🔴 Decline", callback_data=f"gift_no:{receiver_id}")
        ]
    ])

    caption = f"""
**OwO, {name} received a Waifu gift!**\n
**⬤ Waifu** : <code>{waifu_name}</code>
**⬤ Anime** : <code>{waifu_anime}</code>
**⬤ Rarity** : <code>{(await main_func.rank_definer(waifu_rank))}</code>
**⬤ From** : {message.from_user.mention()}\n
<i>Do you want to accept this gift?</i>
"""

    try:
        if message.chat.type == enums.ChatType.PRIVATE:
            await app.send_message(receiver_id, caption, reply_markup=buttons)
            await message.reply_text("Your gift request has been sent to the receiver.")
        else:
            await message.reply_photo(photo=script.PHOTOS["GIFT_IMG"], caption=caption, reply_markup=buttons)
    except Exception:
        await message.reply_text("⚠️ <b>Couldn’t send gift. The user may have privacy settings enabled.</b>")

    
    
# ------------------------ Gift Regex Callback ------------------------ #

@app.on_callback_query(filters.regex(r"gift_yes:(\d+):(.+)"))
async def gift_confirm(_, query):
    click_id = query.from_user.id
    sender_id, receiver_id, waifu_id = query.data.split(":")[1:]
    if click_id != int(receiver_id):
        return await query.answer("This is not for you", show_alert=True)
        
    waifu_data = await waifusdb.getUserWaifu(int(sender_id), waifu_id)
    if not waifu_data:
        return await query.answer("🛑 Waifu no longer exists!", show_alert=True)

    await waifusdb.addUser_Waifu(receiver_id, waifu_data["waifu_id"], waifu_data["name"], waifu_data["anime"], waifu_data["image"], waifu_data["rank"])
    await waifusdb.removeUserWaifu(int(sender_id), waifu_id)

    await query.message.edit_text(
        f"🎉 <b>Gift Accepted!</b>\n\n"
        f"<i>Now {waifu_data['name']} belongs to {query.from_user.first_name}</i> ❤️"
    )


@app.on_callback_query(filters.regex(r"gift_no:(\d+):(.+):(.+)"))
async def gift_confirm(_, query):
    click_id = query.from_user.id
    receiver_id = query.data.split(":")[1:]
    if click_id != int(receiver_id):
        return await query.answer("This is not for you", show_alert=True)
    await query.message.edit_text(f"{name} does not want to accept your gift. They are not interested in receiving your gift.")



# ------------------------ Trade Command ------------------------ #

@app.on_message(filters.command("trade"))
async def trade_waifu(_, message):
    sender_id = message.from_user.id

    if message.reply_to_message:
        try:
            waifu_id = message.text.split(None, 1)[1]
        except IndexError:
            return await message.reply_text("💡 <b>Reply to someone's message with:</b>\n<code>/trade waifu_id</code>")
        receiver_id = message.reply_to_message.from_user.id
        name = message.reply_to_message.from_user.mention
    else:
        try:
            _, receiver_id, waifu_id = message.text.split(None, 2)
            try:
                user_data = await app.get_users(receiver_id)
                name = user_data.mention()
                receiver_id = user_data.id
            except:
                await message.reply_text("User ID Not Found!!")
        except ValueError:
            return await message.reply_text(
                "💡 <b>Correct usage:</b>\n<code>/trade receiver_id waifu_id</code>\n"
                "OR reply to the user with:\n<code>/trade waifu_id</code>"
            )

    waifu_data = await waifusdb.getUserWaifu(sender_id, str(waifu_id))
    if not waifu_data or waifu_data["waifu_id"] != str(waifu_id):
        return await message.reply_text("🛑 <b>This waifu is not in your collection.</b>")

    waifu_name = waifu_data["name"]
    waifu_anime = waifu_data["anime"]
    waifu_rank = waifu_data["rank"] 
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🟢 Accept", callback_data=f"trade_yes:{sender_id}:{receiver_id}:{waifu_id}"),
            InlineKeyboardButton("🔴 Decline", callback_data=f"trade_no:{receiver_id}")
        ]
    ])

    caption = f"""
**OwO, {name} received a trade offer!**\n
**⬤ Waifu** : <code>{waifu_name}</code>
**⬤ Anime** : <code>{waifu_anime}</code>
**⬤ Rarity** : <code>{(await main_func.rank_definer(waifu_rank))}</code>
**⬤ From** : {message.from_user.mention()}\n
<i>Do you want to accept this trade offer?</i>
"""
   
    try:
        if message.chat.type == enums.ChatType.PRIVATE:
            await app.send_message(receiver_id, caption=caption, reply_markup=buttons)
            await message.reply_text("✅ Trade request has been sent to the user.")
        else:
            await message.reply_photo(photo=script.PHOTOS["TRADE_IMG"], caption, reply_markup=buttons)
    except Exception:
        await message.reply_text("⚠️ <b>Couldn’t send trade. The user may have privacy settings enabled.</b>")



# ------------------------ Trade Regex Callback ------------------------ #

@app.on_callback_query(filters.regex(r"trade_yes:(\d+):(.+)"))
async def trade_confirm(_, query):
    click_id = query.from_user.id
    sender_id, receiver_id, waifu_id = query.data.split(":")[1:]
    if click_id != int(receiver_id):
        return await query.answer("This is not for you", show_alert=True)
        
    waifu_data = await waifusdb.getUserWaifu(int(sender_id), waifu_id)
    if not waifu_data:
        return await query.answer("🛑 Waifu no longer exists!", show_alert=True)

    await waifusdb.addUser_Waifu(receiver_id, waifu_data["waifu_id"], waifu_data["name"], waifu_data["anime"], waifu_data["image"], waifu_data["rank"])
    await waifusdb.removeUserWaifu(int(sender_id), waifu_id)

    await query.message.edit_text(
        f"✅ <b>Trade Accepted!</b>\n\n"
        f"<i>{waifu_data['name']} has now been traded to {query.from_user.first_name}.</i> 🤝"
    )


@app.on_callback_query(filters.regex(r"trade_no:(\d+):(.+):(.+)"))
async def trade_decline(_, query):
    click_id = query.from_user.id
    receiver_id = query.data.split(":")[1:]
    if click_id != int(receiver_id):
        return await query.answer("This is not for you", show_alert=True)
        
    await query.message.edit_text(
        f"🛑 <b>Trade Declined!</b>\n\n"
        f"<i>{query.from_user.first_name} is not interested in this trade offer.</i>"
    )


