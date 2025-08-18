from Grabber import api
from fastapi import Body
from Grabber.core.mongo import waifusdb, settingsdb
from fastapi.responses import JSONResponse

# -------------------------- Response Template -------------------------- #
def res(success: bool, message=None, data=None, code=200):
    return JSONResponse(content={
        "success": success,
        "message": message,
        "data": data
    }, status_code=code)



# -------------------------- Server Alive -------------------------- #

@api.get("/")
async def root():
    return res(True, "Server is running successfully.")


# -------------------------- Get All Waifus -------------------------- #

@api.get("/allWaifus")
async def all_waifus():
    waifus = await waifusdb.getAllWaifus()
    if not waifus:
        return res(False, "No waifus found in the database.", code=404)
    return res(True, data=waifus)

# -------------------------- Get Users All Waifu -------------------------- #

@api.get("/userWaifus")
async def user_waifus(user_id: int = None):
    if not user_id:
        return res(False, "Missing required parameter: user_id", code=400)

    waifus = await waifusdb.getUserAllWaifus(user_id)
    if not waifus:
        return res(False, "No waifus found for this user.", code=404)

    return res(True, data={"total": len(waifus), "waifus": waifus})



# -------------------------- Add Users Waifu -------------------------- #

@api.post("/addUserWaifu")
async def add_user_waifu(
    user_id: int = Body(None),
    waifu_id: str = Body(None),
    name: str = Body(None),
    anime: str = Body(None),
    image: str = Body(None),
    rank: str = Body(None),
    price: int = Body(None)
):
    params = {
        "user_id": user_id,
        "waifu_id": waifu_id,
        "name": name,
        "anime": anime,
        "image": image,
        "rank": rank,
        "price": price,
    }

    missing = [k for k, v in params.items() if v is None]
    if missing:
        return res(False, f"Missing fields: {', '.join(missing)}", code=400)

    print("📌 Received params:", params)
    success = await waifusdb.addUser_Waifu(
        user_id, waifu_id, name, anime, image, rank, price
    )

    return res(True, f"Waifu '{name}' from '{anime}' successfully added.", code=201)

    
# -------------------------- Get Users Info -------------------------- #

@api.get("/userInfo")
async def user_info(user_id: int = None):
    if not user_id:
        return res(False, "Missing required parameter: user_id", code=400)

    waifus = await waifusdb.getUserAllWaifus(user_id)
    coins = await settingsdb.get_coins(user_id)
    return res(True, data={"total_waifu": len(waifus), "coins": coins})


