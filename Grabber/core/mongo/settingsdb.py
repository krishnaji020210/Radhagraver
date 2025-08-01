from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from config import MONGO_DB

mongo = MongoCli(MONGO_DB)
db = mongo.settingsdb
time_collection = db.spwantime_db  


async def change_spawn_time(chat_id: int, count: int = 100) -> None:
    await time_collection.update_one(
        {"_id": chat_id},
        {"$set": {"count": count}},
        upsert=True
    )


async def get_spawn_time(chat_id: int) -> int:
    result = await time_collection.find_one({"_id": chat_id})
    return result["count"] if result else 100
