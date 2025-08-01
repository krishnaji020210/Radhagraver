from pyrogram import filters, enums
from Grabner import app
from Grabber.core.mongo import settingsdb


@app.on_message(filters.command("changetime"))
async def change_time(_, message):
    chat_id = message.chat.id

    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("🚫 This command only works in groups.")

    if len(message.command) < 2:
        return await message.reply_text(
            "❗️Usage:\n<b>/changetime [count]</b>\nExample: <code>/changetime 100</code>"
        )

    try:
        count = int(message.text.split(maxsplit=1)[1])
    except ValueError:
        return await message.reply_text("⚠️ Please enter a valid number. Example: <code>/changetime 100</code>")

    await settingsdb.change_spawn_time(chat_id, count)
    await message.reply_text(f"✅ Spawn time successfully set to <b>{count}</b> messages.")


