import requests 



# --------------------------- Gemini-Response --------------------------- #         

gemini_key = "AIzaSyB1rjWN0smsStTaakoSNaz9JveYTtDkXPY"

async def gemini_response(query, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": gemini_key
    }

    data = {
        "contents": [{
            "parts": [{"text": f"{prompt}: {query}"}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            res_json = response.json()
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return "Bot API Dead!! Please Contact My Owner."

    except Exception as e:
        print(f"Exception: {e}")
        return "Bot API Dead!! Please Contact My Owner."


# --------------------------- Rank-Definer --------------------------- #         

async def rank_definer(rank: str) -> str:
    rank = rank.lower()
    
    if rank == "common":
        return f"⚪ Common"
    elif rank == "rare":
        return f"🟢 Rare"
    elif rank == "epic":
        return f"🔵 Epic"
    elif rank == "legendary":
        return f"🟡 Legendary"
    elif rank == "mythical":
        return f"🔴 Mythical"
    elif rank == "dark":
        return f"⚫ Dark"
    else:
        return f"🔘 Not Define"



