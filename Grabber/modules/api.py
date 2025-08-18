from Grabber import api
from fastapi import Body
from Grabber.core.mongo import waifusdb
from fastapi.responses import JSONResponse


def res(success: bool, message=None, data=None, code=200):
    return JSONResponse(content={
        "success": success,
        "message": message,
        "data": data
    }, status_code=code)


@api.get("/")
async def root():
    return res(True, "Server is running successfully.")


@api.get("/allWaifus")
async def all_waifus():
    waifus = await waifusdb.getAllWaifus()
    if not waifus:
        return res(False, "No waifus found in the database.", code=404)
    return res(True, data=waifus)


@api.get("/userWaifus")
async def user_waifus(user_id: int = None):
    if not user_id:
        return res(False, "Missing required parameter: user_id", code=400)

    waifus = await waifusdb.getUserAllWaifus(user_id)
    if not waifus:
        return res(False, "No waifus found for this user.", code=404)

    return res(True, data={"total": len(waifus), "waifus": waifus})




@api.post("/addUserWaifu")
async def add_user_waifu(
    user_id: int = Body(...),
    waifu_id: str = Body(...),
    name: str = Body(...),
    anime: str = Body(...),
    image: str = Body(...),
    rank: str = Body(...),
    price: int = Body(...)
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

    success = await waifusdb.addUser_Waifu(**params)
    if success:
        return res(True, f"Waifu '{name}' from '{anime}' successfully added.", code=201)

    return res(False, "Failed to add waifu. Please check the provided details.", code=400)









