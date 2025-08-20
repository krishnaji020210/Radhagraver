from Grabber import api
from config import BOT_TOKEN
from fastapi import Body, Request, HTTPException, Depends
from Grabber.core.mongo import waifusdb, settingsdb
from fastapi.responses import JSONResponse
import hmac, hashlib, time, urllib.parse




# -------------------------- Response Template -------------------------- #
def res(success: bool, message=None, data=None, code=200):
    return JSONResponse(content={
        "success": success,
        "message": message,
        "data": data
    }, status_code=code)


# -------------------------- Validation Helper -------------------------- #
def validate_telegram_data(init_data: str):
    parsed_data = dict(urllib.parse.parse_qsl(init_data))
    received_hash = parsed_data.pop("hash", None)

    if not received_hash:
        raise HTTPException(status_code=400, detail="Missing hash in initData")

    # create data-check-string
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items()))

    # secret_key = HMAC_SHA256(bot_token, "WebAppData")
    secret_key = hmac.new(
        key=b"WebAppData", msg=BOT_TOKEN.encode(), digestmod=hashlib.sha256
    ).digest()

    expected_hash = hmac.new(
        key=secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()

    if expected_hash != received_hash:
        raise HTTPException(status_code=403, detail="Invalid Telegram initData")

    # check expiry
    auth_date = int(parsed_data.get("auth_date", 0))
    if time.time() - auth_date > 60 * 5:
        raise HTTPException(status_code=403, detail="Expired initData")

    return parsed_data


async def get_current_user(request: Request):
    init_data = request.headers.get("X-Telegram-InitData")
    if not init_data:
        raise HTTPException(status_code=400, detail="Missing X-Telegram-InitData header")
    return validate_telegram_data(init_data)


# -------------------------- Server Alive -------------------------- #
@api.get("/")
async def root():
    return res(True, "Server is running successfully.")


# -------------------------- Get All Waifus -------------------------- #
@api.get("/allWaifus")
async def all_waifus(user=Depends(get_current_user)):
    waifus = await waifusdb.getAllWaifus()
    if not waifus:
        return res(False, "No waifus found in the database.", code=404)
    return res(True, data=waifus)


# -------------------------- Get User's All Waifu -------------------------- #
@api.get("/userWaifus")
async def user_waifus(user=Depends(get_current_user)):
    user_id = user["user"]["id"]  # Telegram se direct user id
    waifus = await waifusdb.getUserAllWaifus(user_id)
    if not waifus:
        return res(False, "No waifus found for this user.", code=404)
    return res(True, data={"total": len(waifus), "waifus": waifus})


# -------------------------- Add User's Waifu -------------------------- #
@api.post("/addUserWaifu")
async def add_user_waifu(
    user=Depends(get_current_user),
    waifu_id: str = Body(None),
    name: str = Body(None),
    anime: str = Body(None),
    image: str = Body(None),
    rank: str = Body(None),
    price: int = Body(None)
):
    user_id = user["user"]["id"]

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

    success = await waifusdb.addUser_Waifu(
        user_id, waifu_id, name, anime, image, rank, price
    )

    return res(True, f"Waifu '{name}' from '{anime}' successfully added.", code=201)


# -------------------------- Get User Info -------------------------- #
@api.get("/userInfo")
async def user_info(user=Depends(get_current_user)):
    user_id = user["user"]["id"]
    waifus = await waifusdb.getUserAllWaifus(user_id)
    coins = await settingsdb.get_coins(user_id)
    return res(True, data={"total_waifu": len(waifus), "coins": coins})


# -------------------------- Add User Coins -------------------------- #
@api.get("/addUserCoins")
async def add_user_coins(user=Depends(get_current_user), coins: int = None):
    if coins is None:
        return res(False, "Missing required parameter: coins", code=400)

    user_id = user["user"]["id"]
    coins = await settingsdb.add_coins(user_id, coins)
    return res(True, f"Successfully added coins {coins}")



from fastapi import Body, Request, HTTPException, Depends
from fastapi.responses import JSONResponse, HTMLResponse
# ... baaki imports & code upar jaise ke waise ...

# -------------------------- Home (Protected HTML) -------------------------- #
@api.get("/home", response_class=HTMLResponse)
async def home(request: Request, user=Depends(get_current_user)):
    # Custom headers (client se bhejna hoga)
    hdr_name = request.headers.get("X-User-Name")
    hdr_id = request.headers.get("X-User-Id")

    if not hdr_name or not hdr_id:
        raise HTTPException(
            status_code=400,
            detail="Missing headers: X-User-Name and/or X-User-Id"
        )

    # X-User-Id integer hona chahiye
    try:
        hdr_id_int = int(hdr_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="X-User-Id must be an integer")

    # Protection: header ka id Telegram-verified user se match hona chahiye
    if hdr_id_int != user["user"]["id"]:
        raise HTTPException(status_code=403, detail="User ID mismatch")

    # XSS से बचने के लिए escape
    import html
    safe_name = html.escape(hdr_name)
    safe_id = html.escape(hdr_id)

    html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Home</title>
  <style>
    :root {{ --bg:#0b1020; --card:#131a2a; --fg:#ffffff; --muted:#a9b1c6; }}
    body {{
      margin:0; background:var(--bg); color:var(--fg);
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Arial, sans-serif;
      padding: 2rem;
    }}
    .card {{
      max-width: 560px; margin: 0 auto; background: var(--card);
      border-radius: 16px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,.35);
    }}
    h1 {{ margin: 0 0 12px; font-size: 1.5rem; }}
    .row {{ display:flex; justify-content:space-between; padding: 10px 0; border-top: 1px solid rgba(255,255,255,.06); }}
    .row:first-of-type {{ border-top: none; }}
    .label {{ color: var(--muted); }}
    strong {{ letter-spacing: .2px; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Welcome 👋</h1>
    <div class="row"><span class="label">Name</span><strong>{safe_name}</strong></div>
    <div class="row"><span class="label">ID</span><strong>{safe_id}</strong></div>
  </div>
</body>
</html>"""

    return HTMLResponse(content=html_body, status_code=200)












