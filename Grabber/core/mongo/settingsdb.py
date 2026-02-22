from Grabber.core.mongo import database

# --------------------------- Core Collection --------------------------- #
time_collection = database.spwantime_db
married_collection = database.marrried_db
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


# ----------------------- Add Married Data ----------------------- #
async def add_married(user_id: int, name: str = "natasha", divorce: str = False) -> None:
    await married_collection.update_one(
        {"_id": user_id},
        {"$set": {"name": name, "divorce", divorce}},
        upsert=True
    )


# ----------------------- Get Married Data ----------------------- #
async def get_married(user_id: int) -> int:
    result = await married_collection.find_one({"_id": user_id})
    return result.get("name", "natasha") if result else "natasha"

