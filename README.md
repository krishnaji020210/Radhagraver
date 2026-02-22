<p align="center">
  <img src="https://media.animerealms.org/image/AgACAgUAAx0EboWBewAC0BtplqHQCOjxeRga-VXIGOSD1pkNkwACEw5rG1zpuVSZRvn7c_fYRgEAAwIAA3kAAzoE" width="300"/>
</p>

<h1 align="center">Waifu Grabber Bot</h1>

<p align="center">
An interactive Anime Waifu Collecting Game Bot built for fun, competition, and pure entertainment.
</p>

<p align="center">
<a href="https://github.com/Akatsumo/WaifuGrabberBot"><strong>🔗 View Official Repository</strong></a>
</p>

---

## 🎮 About The Bot

<p align="center">
Waifu Grabber Bot is a Telegram-based anime collection game where users can grab random anime characters from across the multiverse, collect them, trade them, gift them, and compete with others to become the ultimate waifu master.
<br><br>
Built purely for entertainment and enjoyment, this bot transforms your group into an engaging anime collector battlefield.
</p>

---

# 👥 User Commands

<p align="center">

| Command | Description |
|---------|------------|
| `/grab` | Grab a random waifu from the anime multiverse |
| `/animes` | View all available anime collections |
| `/mywaifus` | Check your collected waifus |
| `/gift` | Send one of your waifus to another user |
| `/trade` | Trade waifus securely with another user |
| `/harem` | View your selected waifu lineup |
| `/leaderboard` | See the global top collectors ranking |
| `/changetime` | Set the waifu spawn cooldown |

</p>

---

# 🛠 Master Commands

<p align="center">

| Command | Description |
|---------|------------|
| `/addwaifu` | Add a waifu into the multiverse |
| `/stats` | View full bot statistics |
| `/broadcast` or `/announce` | Send global announcement |
| `/delete` | Remove a waifu from database |

</p>

---

# 🚀 Deployment Guide

---

## 🟣 Deploy on Heroku

<p align="center">

1. Fork this repository  
2. Create a new Heroku App  
3. Go to **Settings → Config Vars**  
4. Add required environment variables:
   - `BOT_TOKEN`
   - `MONGO_URI`
   - `API_ID`
   - `API_HASH`
5. Connect your GitHub repository  
6. Enable Worker Dyno  
7. Deploy  

</p>

---

## 🖥 Deploy on VPS

<p align="center">

Repository:  
<a href="https://github.com/Akatsumo/WaifuGrabberBot"><strong>https://github.com/Akatsumo/WaifuGrabberBot</strong></a>

</p>

### Step 1: Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install Requirements
```bash
sudo apt install python3 python3-pip git -y
```

### Step 3: Clone Repository
```bash
git clone https://github.com/Akatsumo/WaifuGrabberBot.git
cd WaifuGrabberBot
```

### Step 4: Install Dependencies
```bash
pip3 install -r requirements.txt
```

### Step 5: Create .env File
```
BOT_TOKEN=your_bot_token
MONGO_URI=your_mongo_uri
API_ID=your_api_id
API_HASH=your_api_hash
```

### Step 6: Run Bot
```bash
python3 -m main
```

For 24/7 uptime use:
```
screen -S waifu
```
or
```
tmux
```

---

# 🗄 Database

<p align="center">
Uses MongoDB to manage users, chats, waifus, trades, and leaderboard data securely and efficiently.
</p>

---

# ⚔ Features

<p align="center">
✔ Random anime waifu spawning  
✔ Collection system  
✔ Secure trading  
✔ Gift system  
✔ Global leaderboard  
✔ Harem customization  
✔ Cooldown control  
✔ Master broadcast system  
</p>

---

<p align="center">
Built for anime lovers. Play, collect, dominate.
</p>
