from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from config import MONGO_DB

mongo = MongoCli(MONGO_DB)
db = mongo.settingsdb

waifu_collection = db.waifus_db
user_collection = db.user_waifus


async def addWaifu(name: str, image: str, anime: str, level: str):
    last = await waifu_collection.find().sort("_id", -1).limit(1).to_list(1)
    new_id = str(int(last[0]['_id']) + 1).zfill(3) if last else "001"
    waifu_data = {
        "_id": new_id,
        "name": name,
        "image": image,
        "anime": anime,
        "level": level
    }
    await waifu_collection.insert_one(waifu_data)
    return waifu_data


async def getWaifu(waifu_id: str = None):
    if waifu_id:
        return await waifu_collection.find_one({"_id": waifu_id})
    else:
        cursor = waifu_collection.aggregate([{ "$sample": { "size": 1 } }])
        waifu = await cursor.to_list(1)
        return waifu[0] if waifu else None


async def addUser_Waifu(user_id: int, waifu_id: str, name: str, anime: str, image: str, level: str):
    waifu_entry = {
        "waifu_id": waifu_id,
        "name": name,
        "anime": anime,
        "image": image,
        "level": level
    }
    await user_collection.update_one(
        {"_id": str(user_id)},
        {"$push": {"waifus": waifu_entry}},
        upsert=True
    )
    return waifu_entry


async def getUser_Waifus(user_id: int):
    user_data = await user_collection.find_one({"_id": str(user_id)})
    return user_data.get("waifus", []) if user_data else []


async def removeUser_Waifu(user_id: int, waifu_data: dict):
    await user_collection.update_one(
        {"_id": str(user_id)},
        {"$pull": {"waifus": waifu_data}}
    )


async def removeWaifu(waifu_id: str):
    result = await waifu_collection.delete_one({"_id": waifu_id})
    return result.deleted_count > 0
  
