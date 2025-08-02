from pyrogram import filters 
from Grabber import app
from Grabber.core import main_func
from Grabber.core.brain impot instructions



@app.on_message(filters.command("chatwaifu"))
async def waifu_chat(_, message):
    user_id = message.chat.id
    name = message.from_user.first_name

    if len(message.command) < 2:
        return await message.reply_text("hey baby if you want talk to me then give this /chatwaifu query")
      
    query = int(message.text.split(maxsplit=1)[1])
    char_prompt = await instructions.generate_char(user_id, "Hinata", name)
    answer = await main_func.gemini_response(query, char_prompt)
    await instructions.chat_conversation(user_id, query, answer)
