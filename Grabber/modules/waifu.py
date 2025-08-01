import requests, os, asyncio 
from pyrogram import filters, enums
from Grabber import app
from Grabber.core.mongo import waifusdb

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




@app.on_message(filters.command("addwaifu"))
async def add_waifus(_, message):
    user_id = message.from_user.id
    if message.chat.type != enums.ChatType.PRIVATE:
        return await message.reply_text("This command work in private.")
    msg = await message.reply_text("📸 Please send a waifu photo within 30 seconds...")

    try:
        input1 = await app.listen(user_id=user_id, timeout=30)
    except:
        return await msg.edit_text("❌ Timeout! You didn't send a photo in time.")

    if input1.photo:
        file_name = f"{user_id}_waifu_thumb.jpg"
        photo_path = await asyncio.create_task(app.download_media(input1.photo.file_id, file_name=file_name))

        url = upload_photo(photo_path)
        await input1.delete()

        if not url:
            return await msg.edit_text("⚠️ Failed to upload the photo. Please try again.")

        await msg.edit_text("📝 Now send your waifu's **name**...")

        try:
            input2 = await app.listen(user_id=user_id, timeout=30)
        except:
            return await msg.edit_text("❌ Timeout! You didn't send the name in time.")

        name = input2.text.strip()
        await input2.delete()

        await msg.edit_text("🎬 Now send the **anime name** she is from...")

        try:
            input3 = await app.listen(user_id=user_id, timeout=30)
        except:
            return await msg.edit_text("❌ Timeout! You didn't send the anime name in time.")

        anime = input3.text.strip()
        await input3.delete()

        await msg.edit_text("💠 Now send the **waifu level**.\n\nExamples:\n`Common`, `Rare`, `Epic`, `Legendary`, `Mythic`")

        try:
            input4 = await app.listen(user_id=user_id, timeout=30)
        except:
            return await msg.edit_text("❌ Timeout! You didn't send the level in time.")

        level = input4.text.strip()
        await input4.delete()

        await waifusdb.addWaifu(name, image, anime, rank)
        await msg.delete()
        await message.reply_photo(photo=image,
            caption=f"""
✅ Waifu added successfully!

📸 Photo: [Hosted Link]({url})
👧 Name: {name}
🎬 Anime: {anime}
💠 Rank: {level}
        """, disable_web_page_preview=True)

    else:
        await msg.edit_text("❌ That wasn't a valid photo. Please start again and send a proper waifu image.")



spawn = {}

@app.on_message(filters.group, group=11)
async def _watcher(client, message):
    chat_id = message.chat.id
    if not message.from_user:
        return
        
    if chat_id not in spawn:
        spawn[chat_id] = {"count": 0, "_id": None, "name": None,  "image": None,  "anime": None,  "rank": None}
    spawn[chat_id]["count"] += 1

    if spawn[chat_id]["count"] == 10:
        waifus = await waifusdb.getAllWaifus()
        if not waifus:
            return 
        waifu_data = random.choice(waifus)
        await message.reply_text(waifu_data)
        spawn[chat_id]["count"] = 0
        














