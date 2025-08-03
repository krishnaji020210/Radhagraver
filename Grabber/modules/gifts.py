from pyrogram import filters, Client, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Grabber import app
from Grabber.core.mongo import waifusdb


@app.on_message(filters.command("gift"))
async def gift_waifu(_, message: types.Message):
    sender_id = message.from_user.id

    # Handle two cases: reply OR manual ID entry
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
            return await message.reply_text("💡 <b>Use it like this:</b>\n<code>/gift receiver_id waifu_id</code>")

    # Get waifu data
    waifu_data = await waifusdb.getUserWaifu(sender_id, str(waifu_id))
    if not waifu_data or waifu_data["waifu_id"] != str(waifu_id):
        return await message.reply_text("❌ <b>Waifu not found in your collection.</b>")

    waifu_name = waifu_data["name"]

    # Ask receiver to confirm
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Yes", callback_data=f"gift_yes:{sender_id}:{waifu_id}"),
            InlineKeyboardButton("❌ No", callback_data="gift_no")
        ]
    ])

    await app.send_message(
        receiver_id,
        f"🎁 <b>You have received a Waifu gift!</b>\n\n"
        f"<b>Waifu Name:</b> {waifu_name}\n"
        f"<b>From:</b> {message.from_user.mention()}\n\n"
        f"<i>Do you want to accept this gift?</i>",
        reply_markup=buttons
    )

    await message.reply_text("✅ <b>Gift request sent to the receiver.</b>")


@app.on_callback_query(filters.regex(r"gift_yes:(\d+):(.+)"))
async def gift_confirm(_, query):
    receiver_id = query.from_user.id
    sender_id, waifu_id = query.data.split(":")[1:]

    # Re-fetch waifu to confirm ownership
    waifu_data = await waifusdb.getUserWaifu(int(sender_id), waifu_id)
    if not waifu_data:
        return await query.answer("❌ Waifu no longer exists!", show_alert=True)

    await waifusdb.addUser_Waifu(receiver_id, waifu_data["_id"], waifu_data["name"], waifu_data["anime"], waifu_data["image"], waifu_data["rank"])
    await waifusdb.removeUserWaifu(int(sender_id), waifu_id)

    await query.message.edit_text(
        f"🎉 <b>Gift accepted!</b>\n\n"
        f"Now <b>{waifu_data['name']}</b> belongs to <b>{query.from_user.first_name}</b> ❤️"
    )


@app.on_callback_query(filters.regex("gift_no"))
async def gift_decline(_, query):
    await query.message.edit_text("❌ <b>Gift declined.</b>")


@app.on_message(filters.command("trade"))
async def trade_waifu(_, message: types.Message):
    sender_id = message.from_user.id

    if message.reply_to_message:
        try:
            sender_waifu_id, receiver_waifu_id = message.text.split(None, 2)[1:]
        except ValueError:
            return await message.reply_text("💡 <b>Reply to someone's message and use:</b>\n<code>/trade your_waifu_id their_waifu_id</code>")
        receiver_id = message.reply_to_message.from_user.id
    else:
        try:
            _, receiver_id, sender_waifu_id, receiver_waifu_id = message.text.split(None, 3)
            receiver_id = int(receiver_id)
        except ValueError:
            return await message.reply_text("💡 <b>Use like:</b>\n<code>/trade receiver_id your_waifu_id their_waifu_id</code>")

    your_waifu = await waifusdb.getUserWaifu(sender_id, sender_waifu_id)
    their_waifu = await waifusdb.getUserWaifu(receiver_id, receiver_waifu_id)

    if not your_waifu or not their_waifu:
        return await message.reply_text("❌ <b>Invalid waifu IDs for trade!</b>")

    btns = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔁 Accept Trade", callback_data=f"trade_yes:{sender_id}:{sender_waifu_id}:{receiver_waifu_id}"),
            InlineKeyboardButton("❌ Decline", callback_data="trade_no")
        ]
    ])

    await app.send_message(
        receiver_id,
        f"🔁 <b>Trade request!</b>\n\n"
        f"<b>{message.from_user.first_name}</b> wants to trade:\n"
        f"➡️ <b>{your_waifu['name']}</b>\n"
        f"⬅️ For your <b>{their_waifu['name']}</b>\n\n"
        f"Do you accept?",
        reply_markup=btns
    )

    await message.reply_text("✅ <b>Trade request sent to the user.</b>")


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


