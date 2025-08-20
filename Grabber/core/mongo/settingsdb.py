from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from config import MONGO_DB

mongo = MongoCli(MONGO_DB)
db = mongo.settingsdb
time_collection = db.spwantime_db  
coins_collection = db.users_coins
trial_collection = db.users_trail_time

# ----------------------- Get Spawn Time ----------------------- #

async def change_spawn_time(chat_id: int, count: int = 100) -> None:
    await time_collection.update_one(
        {"_id": chat_id},
        {"$set": {"count": count}},
        upsert=True
    )


# ----------------------- Change Spawn Time ----------------------- #

async def get_spawn_time(chat_id: int) -> int:
    result = await time_collection.find_one({"_id": chat_id})
    return result["count"] if result else 100



# ----------------------- Add Coins ----------------------- #

async def add_coins(user_id, coins):
    await coins_collection.update_one(
        {"_id": user_id},
        {"$set": {"coins": coins}},
        upsert=True
    )


# ----------------------- Get Coins ----------------------- #

async def get_coins(user_id: int) -> int:
    result = await coins_collection.find_one({"_id": user_id})
    return result["coins"] if result else 0




# ----------------------- Add Trial Time ----------------------- #

async def addTime_expired(user_id, count, time):
    await trial_collection.update_one(
        {"_id": user_id},
        {"$set": {"coins": coins, "time": time}},
        upsert=True
    )


# ----------------------- Get Trial Time ----------------------- #

async def getTime_expired(user_id: int) -> int:
    result = await trial_collection.find_one({"_id": user_id})
    return result["count"], result["time"] if result else 0, 0



