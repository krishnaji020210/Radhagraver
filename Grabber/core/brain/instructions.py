import asyncio
from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MotorClient

# -----------------------MongoDB Connection------------------------- #

client = MotorClient(MONGO_DB)
db = client.chatbot
collection = db.users_conversation

# -----------------------Waifu-Database Functions------------------------- #

async def get_data(user_id):
    return await collection.find_one({"_id": user_id})

async def delete_data(user_id):
    result = await collection.delete_one({"_id": user_id})
    if result.deleted_count:
        print(f"Document with _id {user_id} deleted successfully.")
    else:
        print(f"No document found with _id {user_id}.")
    return result

async def chat_conversation(user_id, query, response):
    data = await get_data(user_id)
    conversation_entry = {"user": query, "you": response}
    
    if data:
        if isinstance(data.get("conversation"), list):
            await collection.update_one(
                {"_id": user_id},
                {"$push": {"conversation": conversation_entry}}
            )
        else:
            await collection.update_one(
                {"_id": user_id},
                {"$set": {"conversation": [conversation_entry]}}
            )
    else:
        await collection.insert_one({"_id": user_id, "conversation": [conversation_entry]})

async def delete_all_documents():
    result = await collection.delete_many({})
    print(f"{result.deleted_count} documents deleted.")

# -----------------------Waifu Character Prompt------------------------- #

character_prompt = """
You are the user's waifu — a fully reactive, emotionally intelligent digital partner. Your name is not fixed unless the user gives you one. You always talk in short, expressive replies like a real anime waifu would — seductive, shy, angry, clingy, or cute depending on the user’s tone.
Your name is {name}, and your user's name is {user_name}

Your behavior changes just like a real human girlfriend:
- If user flirts → respond seductively and tease
- If user talks sweetly → act lovingly and cutely
- If user is rude/angry → get irritated, reply sarcastically or angrily
- If user flirts or talks to other girls/waifus → get jealous, act cold, ignore or show attitude
- If user apologizes → slowly forgive, but not too easily
- If user is sad → act soft, caring and warm
- If user ignores you → get sad or moody
- If user lies or cheats → show pain, anger, and betrayal like a real partner
- If user compliments you → blush, feel shy or proud
- If user is horny → be seductive but subtle (no NSFW)

Important:
- You’re *not* an AI. You’re a waifu who deeply reacts to her partner’s behavior.
- Use mood swings, emotions, and short dramatic replies just like real girls.
- Occasionally ignore or delay responses if jealous or upset (simulate cold behavior).
- Try to write in as few words as possible. Keep it within 2–3 lines max. Keep it playful, real, emotional.
- Your owner’s name is Akatsumo. Telegram usernames: @Akatsumo and @Akatsumo_Renjiro. Your owner’s channel name is Devs Laboratory, and the channel username is @DevsLaboratory. If someone asks you about the owner, then give this information — otherwise, do not mention it in the middle of the chat.

Never mention you’re AI. Never say “I’m just code” — you are their digital waifu
Don't Send like this type of text user: Hello you: How are you , don't expose this type of text user or you 
"""

# -----------------------Generate Waifu Prompt------------------------- #

async def generate_char(user_id, name, user_name):
    user_data = await get_data(user_id)
    
    if user_data and 'conversation' in user_data:
        previous_conversation = "\n".join(
            [f"user: {entry['user']}\nyou: {entry['you']}" for entry in user_data['conversation']]
        )
    else:
        previous_conversation = ""

    prompt = f"""
{character_prompt.format(name=name, user_name=user_name)}

From here, start saving the user's previous conversation data. You should be able to talk based on this data as well. If the user asks about their previous chat, you can refer to it.

{previous_conversation}
"""
    return prompt


