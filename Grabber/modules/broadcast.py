import asyncio, traceback
from Grabber import app
from config import OWNER_ID
from pyrogram import filters
from Grabber.core.mongo import usersdb, chatsdb
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid


async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        return False, f"{user_id} : deactivated"
    except UserIsBlocked:
        return False, f"{user_id} : blocked the bot"
    except PeerIdInvalid:
        return False, f"{user_id} : user ID invalid"
    except Exception:
        return False, f"{user_id} : {traceback.format_exc()}"


@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to broadcast it.")

    status_msg = await message.reply("📣 Starting broadcast...")
    chats = await chatsdb.get_all_chats() or []
    users = await usersdb.get_all_users() or []

    stats = {"chats": {"success": 0, "fail": 0}, "users": {"success": 0, "fail": 0}}

    for chat_id in chats:
        success, _ = await send_msg(chat_id, message.reply_to_message)
        if success:
            stats["chats"]["success"] += 1
        else:
            stats["chats"]["fail"] += 1
        await asyncio.sleep(0.05)

    for user_id in users:
        success, _ = await send_msg(user_id, message.reply_to_message)
        if success:
            stats["users"]["success"] += 1
        else:
            stats["users"]["fail"] += 1
        await asyncio.sleep(0.05)

    text = (
        "**✅ Broadcast Completed**\n\n"
        f"📨 Sent to **{stats['chats']['success']} chats** and **{stats['users']['success']} users**.\n"
    )
    if stats["chats"]["fail"] or stats["users"]["fail"]:
        text += (
            f"⚠️ Failed to send to **{stats['chats']['fail']} chats** "
            f"and **{stats['users']['fail']} users**."
        )

    await status_msg.edit_text(text)


@app.on_message(filters.command("announce") & filters.user(OWNER_ID))
async def announce(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a post/message to announce it.")

    to_forward_id = message.reply_to_message.id
    from_chat_id = message.chat.id

    chats = await chatsdb.get_all_chats() or []
    users = await usersdb.get_all_users() or []

    failed_chats = 0
    failed_users = 0

    for chat_id in chats:
        try:
            await _.forward_messages(chat_id=chat_id, from_chat_id=from_chat_id, message_ids=to_forward_id)
            await asyncio.sleep(0.05)
        except Exception:
            failed_chats += 1

    for user_id in users:
        try:
            await _.forward_messages(chat_id=user_id, from_chat_id=from_chat_id, message_ids=to_forward_id)
            await asyncio.sleep(0.05)
        except Exception:
            failed_users += 1

    await message.reply_text(
        f"📢 Announcement complete!\n\n"
        f"✅ Delivered to {len(chats) - failed_chats} chats & {len(users) - failed_users} users.\n"
        f"❌ Failed in {failed_chats} chats & {failed_users} users."
    )

