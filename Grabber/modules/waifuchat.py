from pyrogram import filters
from Grabber import app
from Grabber.core import main_func
from Grabber.core.brain import instructions

@app.on_message(filters.command("aifu", prefixes=["W", "w"]))
@app.on_message(filters.command("chatwaifu"))
async def waifu_chat(_, message):
    user_id = message.chat.id
    name = message.from_user.first_name or "Anon"

    if not message.text or len(message.command) < 2:
        return await message.reply_text("Hmm? You forgot to add what you wanted to say!\n\nTry again like:\n`/chatwaifu Hi, how are you?`")
    query = message.text.split(None, 1)[1]

    char_prompt = await instructions.generate_char(user_id, "Hinata", name)
    answer = await main_func.gemini_response(query, char_prompt)
    await instructions.chat_conversation(user_id, query, answer)
    await message.reply_text(answer)




@app.on_message(filters.command("clear"))
async def delete_chathistory(_, message):
    user_id = message.from_user.id
    database = await instructions.delete_data(user_id)
    if database.deleted_count:
        await message.reply_text(f"{message.from_user.first_name} your chat history database deleted successfully.")
    else:
        await message.reply_text(f"{message.from_user.first_name} not save any database!!")
