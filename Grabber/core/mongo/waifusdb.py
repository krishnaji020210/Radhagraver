from Grabber.core.mongo import database

# --------------------------- Waifu Collection --------------------------- #
waifu_collection = database.waifus_db  
user_collection = database.user_waifus
# --------------------------- Core --------------------------- #


# ------------------------ Add New Waifu ------------------------ #

async def addWaifu(name: str, image: str, anime: str, rank: str, price: int) -> dict:
    last = await waifu_collection.find().sort("_id", -1).limit(1).to_list(1)
    new_id = str(int(last[0]['_id']) + 1).zfill(3) if last else "001"

    waifu_data = {
        "_id": new_id,
        "name": name,
        "image": image,
        "anime": anime,
        "rank": rank,
        "price": price    
    }

    await waifu_collection.insert_one(waifu_data)
    print(waifu_data)
    return waifu_data


# ------------------------ Get Waifu ------------------------ #

async def getWaifu(waifu_id: str = None) -> dict | None:
    if waifu_id:
        return await waifu_collection.find_one({"_id": waifu_id})
    waifu = await waifu_collection.aggregate([{ "$sample": { "size": 1 } }]).to_list(1)
    return waifu[0] if waifu else None


# ------------------------ Get All Waifus ------------------------ # 

async def getAllWaifus() -> list:
    cursor = waifu_collection.find({})
    waifus = await cursor.to_list(length=1000000)
    return waifus

# ------------------------ Remove a Waifu by ID ------------------------ #

async def removeWaifu(waifu_id: str) -> bool:
    result = await waifu_collection.delete_one({"_id": waifu_id})
    return result.deleted_count > 0


# ------------------------ Remove All Waifus ------------------------ # 

async def removeAllWaifus() -> int:
    result = await waifu_collection.delete_many({})
    return result.deleted_count


# --------------------------------------------------------------- #

# ------------------------ Add User Waifu  ------------------------ #

async def addUser_Waifu(user_id: int, waifu_id: str, name: str, anime: str, image: str, rank: str, price: int):
    query = {"_id": str(user_id), "waifus.waifu_id": waifu_id}
    existing = await user_collection.find_one(query)
    if existing:
        await user_collection.update_one(
            {"_id": str(user_id), "waifus.waifu_id": waifu_id},
            {"$inc": {"waifus.$.grab_count": 1}}
        )
    else:
        waifu_entry = {
            "waifu_id": waifu_id,
            "name": name,
            "anime": anime,
            "image": image,
            "rank": rank,
            "price": price, 
            "grab_count": 1
        }
        await user_collection.update_one(
            {"_id": str(user_id)},
            {"$push": {"waifus": waifu_entry}},
            upsert=True
        )

# ------------------------ Get User All Waifu  ------------------------ #

async def getUserAllWaifus(user_id: int) -> list:
    data = await user_collection.find_one({"_id": str(user_id)})
    return data.get("waifus", []) if data else []

# ------------------------ Get User Waifu by ID  ------------------------ #

async def getUserWaifu(user_id: int, waifu_id: str) -> dict | None:
    data = await user_collection.find_one({"_id": str(user_id)})
    if not data:
        return None
    for w in data.get("waifus", []):
        if w["waifu_id"] == waifu_id:
            return w
    return None


# ------------------------ Remove User Waifu  ------------------------ #

async def removeUserWaifu(user_id: int, waifu_id: str) -> str:
    data = await user_collection.find_one({"_id": str(user_id)})
    if not data:
        return False

    waifus = data.get("waifus", [])
    updated_waifus = []
    removed = False

    for w in waifus:
        if w["waifu_id"] == waifu_id:
            if w["grab_count"] > 1:
                w["grab_count"] -= 1
                updated_waifus.append(w)
            removed = True
        else:
            updated_waifus.append(w)

    if removed:
        await user_collection.update_one(
            {"_id": str(user_id)},
            {"$set": {"waifus": updated_waifus}}
        )
        return True
    return False


# ------------------------ Remove All User Waifu  ------------------------ #

async def removeAllUserWaifus(user_id: int) -> bool:
    result = await user_collection.update_one(
        {"_id": str(user_id)},
        {"$set": {"waifus": []}}
    )
    return result.modified_count > 0











