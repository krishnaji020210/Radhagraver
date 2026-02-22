from Grabber.core.mongo import database

# --------------------------- Chats Collection --------------------------- #
chatsdb = database.chats_db
# ------------------------------------------------------------------------ #


async def ensure_indexes():
    await chatsdb.create_index("chat", unique=True)


# --------------------------- Get All Chats --------------------------- #
async def get_all_chats():
    return [
        doc["chat"]
        async for doc in chatsdb.find(
            {"chat": {"$gt": 0}},
            {"_id": 0, "chat": 1}
        )
    ]


# --------------------------- Check Chat Exists --------------------------- #
async def is_chat_exist(chat: int) -> bool:
    return bool(await chatsdb.find_one({"chat": chat}))


# --------------------------- Add Chat --------------------------- #
async def add_chat(chat: int):
    await chatsdb.update_one(
        {"chat": chat},
        {"$setOnInsert": {"chat": chat}},
        upsert=True
    )


# --------------------------- Delete Chat --------------------------- #
async def del_chat(chat: int):
    await chatsdb.delete_one({"chat": chat})

