from Grabber.core.mongo import database

# --------------------------- Spawn Collection --------------------------- #
time_collection = database.spwantime_db
# --------------------------- Core --------------------------- #


# ----------------------- Change Spawn Time ----------------------- #
async def change_spawn_time(chat_id: int, count: int = 100) -> None:
    await time_collection.update_one(
        {"_id": chat_id},
        {"$set": {"count": count}},
        upsert=True
    )


# ----------------------- Get Spawn Time ----------------------- #
async def get_spawn_time(chat_id: int) -> int:
    result = await time_collection.find_one({"_id": chat_id})
    return result.get("count", 100) if result else 100


