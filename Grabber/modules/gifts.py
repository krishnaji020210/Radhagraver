from pyrogram import filters, Client, enums, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Grabber import app
from Grabber.core.mongo import waifusdb


@app.on_message(filters.command("gift"))
async def gift_waifu(_, message: types.Message):
    sender_id = message.from_user.id

    if message.reply_to_message:
        try:
            waifu_id = message.text.split(None, 1)[1]
        except IndexError:
            return await message.reply_text("💡 <b>Reply to someone's message with:</b>\n<code>/gift waifu_id</code>")
        receiver_id = message.reply_to_message.from_user.id
    else:
        try:
            _, receiver_id, waifu_id = message.text.split(None, 2)
            receiver_id = int(receiver_id)
        except ValueError:
            return await message.reply_text(
                "💡 <b>Correct usage:</b>\n<code>/gift receiver_id waifu_id</code>\n"
                "OR reply to the user with:\n<code>/gift waifu_id</code>"
            )

    waifu_data = await waifusdb.getUserWaifu(sender_id, str(waifu_id))
    if not waifu_data or waifu_data["waifu_id"] != str(waifu_id):
        return await message.reply_text("❌ <b>This waifu is not in your collection.</b>")

    waifu_name = waifu_data["name"]
    waifu_anime = waifu_data.get("anime", "Unknown Anime")

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🟢 Accept", callback_data=f"gift_yes:{sender_id}:{waifu_id}"),
            InlineKeyboardButton("🔴 Decline", callback_data="gift_no")
        ]
    ])

    caption = f"""
**You received a Waifu gift!**\n
**⬤ Waifu** : <code>{waifu_name}</code>
**⬤ Anime** : <code>{waifu_anime}</code>
**⬤ From** : {message.from_user.mention()}\n\n
Do you want to accept this gift?"
    """

    try:
        if message.chat.type == enums.ChatType.PRIVATE:
            await app.send_message(receiver_id, caption, reply_markup=butt ons)
        else:
            await message.reply_text(caption, reply_markup=buttons)
    except Exception:
        await message.reply_text("⚠️ <b>Couldn’t send gift. The user may have privacy settings enabled.</b>")


    

"""
@app.on_callback_query(filters.regex(r"gift_yes:(\d+):(.+)"))
async def gift_confirm(_, query):
    receiver_id = query.from_user.id
    sender_id, waifu_id = query.data.split(":")[1:]

    # Re-fetch waifu to confirm ownership
    waifu_data = await waifusdb.getUserWaifu(int(sender_id), waifu_id)
    if not waifu_data:
        return await query.answer("❌ Waifu no longer exists!", show_alert=True)

    await waifusdb.addUser_Waifu(receiver_id, waifu_data["waifu_id"], waifu_data["name"], waifu_data["anime"], waifu_data["image"], waifu_data["rank"])
    await waifusdb.removeUserWaifu(int(sender_id), waifu_id)

    await query.message.edit_text(
        f"🎉 <b>Gift accepted!</b>\n\n"
        f"Now <b>{waifu_data['name']}</b> belongs to <b>{query.from_user.first_name}</b> ❤️"
    )







@app.on_callback_query(filters.regex(r"trade_yes:(\d+):(.+):(.+)"))
async def trade_confirm(_, query):
    receiver_id = query.from_user.id
    sender_id, sender_waifu_id, receiver_waifu_id = query.data.split(":")[1:]

    sender_waifu = await waifusdb.getUserWaifu(int(sender_id), sender_waifu_id)
    receiver_waifu = await waifusdb.getUserWaifu(receiver_id, receiver_waifu_id)

    if not sender_waifu or not receiver_waifu:
        return await query.answer("❌ Trade failed: One or both waifus missing!", show_alert=True)

    await waifusdb.addUser_Waifu(receiver_id, sender_waifu["_id"], sender_waifu["name"], sender_waifu["anime"], sender_waifu["image"], sender_waifu["rank"])
    await waifusdb.addUser_Waifu(int(sender_id), receiver_waifu["_id"], receiver_waifu["name"], receiver_waifu["anime"], receiver_waifu["image"], receiver_waifu["rank"])

    await waifusdb.removeUserWaifu(int(sender_id), sender_waifu_id)
    await waifusdb.removeUserWaifu(receiver_id, receiver_waifu_id)

    await query.message.edit_text("🔁 <b>Trade completed successfully!</b> 🎉")


@app.on_callback_query(filters.regex("trade_no"))
async def trade_decline(_, query):
    await query.message.edit_text("❌ <b>Trade declined.</b>")

"""
