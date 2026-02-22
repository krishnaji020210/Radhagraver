import random
from config import SUDO_IDS
from Grabber.core import script
import requests, os, asyncio 
from pyrogram import filters, enums
from Grabber import app
from Grabber.core.mongo import waifusdb, settingsdb
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ------------------------- Image Host ------------------------- #

def upload_photo(file_path):
    api_url = "https://media.animerealms.org/upload"    
    with open(file_path, "rb") as file:
        files = {
            "image": (file_path.split("/")[-1], file, "image/jpeg"),
        }        
        response = requests.post(api_url, files=files)        
        if response.status_code == 200:
            try:
                data = response.json()
                file_id = data.get("fileId", "Unknown fileId")
                img_url = f"https://media.animerealms.org/image/{file_id}"
                return img_url            
            except Exception as e:
                print("Error parsing JSON response:", e)
                return None
        else:
            print("Failed to upload the image. Status code:", response.status_code)
            return None



# ------------------------- Add Waifu ------------------------- #

@app.on_message(filters.command("addwaifu") & filters.user(SUDO_IDS))
async def add_waifus(_, message):
    user_id = message.from_user.id
    if message.chat.type != enums.ChatType.PRIVATE:
        return await message.reply_text("This command work in private.")
    msg = await message.reply_text("📸 Please send a waifu photo within 30 seconds...")

    try:
        input1 = await app.listen(user_id=user_id, timeout=30)
    except:
        return await msg.edit_text("🛑 Timeout! You didn't send a photo in time.")

    if input1.photo:
        file_name = f"{user_id}_waifu_thumb.jpg"
        photo_path = await asyncio.create_task(app.download_media(input1.photo.file_id, file_name=file_name))

        url = upload_photo(photo_path)
        await input1.delete()

        if not url:
            return await msg.edit_text("🛑 Failed to upload the photo. Please try again.")

        await msg.edit_text("📝 Now send your waifu's **name**...")

        try:
            input2 = await app.listen(user_id=user_id, timeout=30)
        except:
            return await msg.edit_text("🛑 Timeout! You didn't send the name in time.")

        name = input2.text.strip()
        await input2.delete()

        await msg.edit_text("🎬 Now send the **anime name** she is from...")

        try:
            input3 = await app.listen(user_id=user_id, timeout=30)
        except:
            return await msg.edit_text("🛑 Timeout! You didn't send the anime name in time.")

        anime = input3.text.strip()
        await input3.delete()

        await msg.edit_text("💠 Now send the **waifu rank**.\n\nExamples:\n`Common`, `Rare`, `Epic`, `Legendary`, `Mythical`, `Dark`,`Divine`,`Celestial`")

        try:
            input4 = await app.listen(user_id=user_id, timeout=30)
        except:
            return await msg.edit_text("🛑 Timeout! You didn't send the level in time.")

        rank = input4.text.strip()
        await input4.delete()
        
        await msg.edit_text("💠 Now send the **waifu price**.\n\nExample Of Price List:\n`Common: 100-400`\n`Rare: 300-800`\n`Epic: 500-1000`\n`Legendary: 600-1200`\n`Mythical: 800-1600`\n`Dark: 1000-2000`\n`Divine: 1200-2400`\n`Celestial: 1400-3000`")

        try:
            input5 = await app.listen(user_id=user_id, timeout=30)
        except:
            return await msg.edit_text("🛑 Timeout! You didn't send the Price in time.")

        price = int(input5.text.strip())
        await input4.delete()

        waifu_data = await waifusdb.addWaifu(name, url, anime, rank, price)
        await msg.delete()
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🗑 Delete", callback_data=f"delete_waifu:{waifu_data['_id']}")]])
        await message.reply_photo(photo=url,
            caption=f"""
✅ Waifu added successfully!

📸 Photo: [Hosted Link]({url})

🧩 ID: {waifu_data["_id"]}
👧 Name: {name}
🎬 Anime: {anime}
💠 Rank: {rank}
💰 Price: {price}
        """, reply_markup=keyboard)

    else:
        await msg.edit_text("🛑 That wasn't a valid photo. Please start again and send a proper waifu image.")



# ------------------------- Delete Waifu ------------------------- #

@app.on_message(filters.command("delete") & filters.private & filters.user(SUDO_IDS))
async def delete_waifu(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage:\n<code>/delete waifu_id</code>")

    waifu_id = message.command[1].strip()
    waifu = await waifusdb.getWaifu(waifu_id)
    if not waifu:
        return await message.reply_text("🛑 Waifu not found.")
        
    deleted = await waifusdb.removeWaifu(waifu_id)

    if deleted:
        await message.reply_text(
            f"🗑️ Successfully deleted waifu:\n"
            f"🆔 <code>{waifu_id}</code>\n"
            f"👧 Name: {waifu.get('name', 'Unknown')}",
        )
    else:
        await message.reply_text("🛑 Failed to delete waifu.")

# ------------------------- Delete Waifu Regex ------------------------- #

@app.on_callback_query(filters.regex(r"^delete_waifu:(\d+)$"))
async def delete_waifu_callback(_, query):
    user_id = query.from_user.id
    
    if user_id not in SUDO_IDS:
        return await query.answer("🛑 You are not allowed to delete waifus.", show_alert=True)

    waifu_id = query.matches[0].group(1)

    waifu = await waifusdb.getWaifu(waifu_id)
    if not waifu:
        return await query.answer("🛑 Waifu not found.", show_alert=True)

    deleted = await waifusdb.removeWaifu(waifu_id)

    if deleted:
        await query.answer("🗑 Waifu deleted successfully!", show_alert=True)

        await query.message.edit_caption(
            caption=f"""
🗑️ <b>Waifu Deleted</b>

🆔 <code>{waifu_id}</code>
👧 Name: {waifu.get('name', 'Unknown')}
"""
        )
    else:
        await query.answer("🛑 Failed to delete waifu.", show_alert=True)


# ------------------------- Waifu Watcher ------------------------- #

spawn = {}


@app.on_message(filters.group & filters.text, group=11)
async def watcher(client, message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    spawn_count = await settingsdb.get_spawn_time(chat_id)

    if chat_id not in spawn:
        spawn[chat_id] = {
            "count": 0,
            "_id": None,
            "name": None,
            "image": None,
            "anime": None,
            "rank": None,
            "price": None,
            "spawned": False,
            "grabbed": False,
            "task": None
        }

    if spawn[chat_id]["spawned"]:
        return

    spawn[chat_id]["count"] += 1

   
    if spawn[chat_id]["count"] >= spawn_count:
        spawn[chat_id]["count"] = 0  
        waifus = await waifusdb.getAllWaifus()
        if not waifus:
            return

        waifu_data = random.choice(waifus)

        spawn[chat_id].update({
            "_id": waifu_data["_id"],
            "name": waifu_data["name"],
            "image": waifu_data["image"],
            "anime": waifu_data["anime"],
            "rank": waifu_data["rank"],
            "price": waifu_data["price"],
            "spawned": True,
            "grabbed": False
        })

        msg = await message.reply_photo(photo=waifu_data["image"], caption=random.choice(script.SPAWN_TEXT).format(rank=waifu_data["rank"]))

        async def timeout():
            await asyncio.sleep(15)

            if chat_id in spawn and spawn[chat_id]["spawned"] and not spawn[chat_id]["grabbed"]:
                try:
                    await msg.delete()
                except:
                    pass

                await message.reply_text(
                    random.choice(script.MISSED_GRAB_TEXT).format(
                        name=spawn[chat_id]["name"]
                    )
                )

                spawn[chat_id]["spawned"] = False
                spawn[chat_id]["grabbed"] = False

        if spawn[chat_id]["task"]:
            spawn[chat_id]["task"].cancel()

        spawn[chat_id]["task"] = asyncio.create_task(timeout())


# ------------------------- Waifu Grab ------------------------- #

@app.on_message(filters.command("grab") & filters.group)
async def grab_waifu(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if len(message.command) < 2:
        return await message.reply_text("<b>Use it like this:</b> <code>/grab WaifuName</code>")

    name = message.text.split(" ", 1)[1].strip()

    if chat_id not in spawn or not spawn[chat_id]["spawned"]:
        return await message.reply_text("No waifu has spawned in this group yet~ Wait for her appearance~ 😚")

    if spawn[chat_id]["grabbed"]:
        return await message.reply_text("Already grabbed! Try again next time 😏")

    await waifusdb.addUser_Waifu(
        user_id=user_id,
        waifu_id=spawn[chat_id]["_id"],
        name=spawn[chat_id]["name"],
        anime=spawn[chat_id]["anime"],
        image=spawn[chat_id]["image"],
        rank=spawn[chat_id]["rank"],
        price=spawn[chat_id]["price"]
    )

    await message.reply_text(random.choice(script.GRAB_TEXT).format(name=name))
    spawn[chat_id]["grabbed"] = True
    spawn[chat_id]["spawned"] = False

    if spawn[chat_id]["task"]:
        spawn[chat_id]["task"].cancel()
        spawn[chat_id]["task"] = None

    


