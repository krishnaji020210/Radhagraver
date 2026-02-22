<p align="center">
  <img src="https://media.animerealms.org/image/AgACAgUAAx0EboWBewAC0BtplqHQCOjxeRga-VXIGOSD1pkNkwACEw5rG1zpuVSZRvn7c_fYRgEAAwIAA3kAAzoE" width="260"/>
</p>

<h1 align="center" style="color:#6A0DAD;">Waifu Grabber Bot</h1>

<p align="center">
<b>A Royal Anime Collecting Experience</b><br>
An interactive Telegram game where you collect, trade and dominate the anime multiverse.
</p>

<p align="center">
<a href="https://github.com/Akatsumo/WaifuGrabberBot">
<img src="https://img.shields.io/badge/GitHub-WaifuGrabberBot-6A0DAD?style=for-the-badge&logo=github&logoColor=white">
</a>
<a href="#-deploy-on-vps">
<img src="https://img.shields.io/badge/Deploy-VPS-4B0082?style=for-the-badge">
</a>
</p>

---

<h2 align="center">About The Project</h2>

<p align="center">
Waifu Grabber Bot is a competitive anime collection game designed for entertainment and community engagement.
Users can grab random waifus, build their collection, trade securely, gift strategically, and compete globally to rise as the ultimate collector.
<br><br>
Crafted with performance, scalability, and gameplay balance in mind.
</p>

---

<h2 align="center">User Commands</h2>

<p align="center">

| Command | Description |
|---------|------------|
| `/grab` | Grab a random waifu |
| `/animes` | View all available anime collections |
| `/mywaifus` | View your collection |
| `/gift` | Gift a waifu to another user |
| `/trade` | Securely trade waifus |
| `/harem` | View your selected lineup |
| `/leaderboard` | Global collectors ranking |
| `/changetime` | Adjust spawn cooldown |

</p>

---

<h2 align="center">Master Commands</h2>

<p align="center">

| Command | Description |
|---------|------------|
| `/addwaifu` | Add waifu to the multiverse |
| `/stats` | View full bot statistics |
| `/broadcast` / `/announce` | Send global announcements |
| `/delete` | Remove waifu from system |

</p>

---

<h2 align="center">Deployment</h2>

---

<h3 align="center">Deploy on Heroku</h3>

<p align="center">

1. Fork this repository  
2. Create Heroku App  
3. Add Config Vars:
   - `BOT_TOKEN`
   - `MONGO_URI`
   - `API_ID`
   - `API_HASH`
4. Enable Worker Dyno  
5. Deploy  

</p>

---

<h3 align="center" id="-deploy-on-vps">Deploy on VPS</h3>

<p align="center">
<a href="https://github.com/Akatsumo/WaifuGrabberBot">
<strong>Click Here to Open Repository for VPS Deployment</strong>
</a>
</p>

### 1️⃣ Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 2️⃣ Install Dependencies
```bash
sudo apt install python3 python3-pip git -y
```

### 3️⃣ Clone Repository
```bash
git clone https://github.com/Akatsumo/WaifuGrabberBot.git
cd WaifuGrabberBot
```

### 4️⃣ Install Python Requirements
```bash
pip3 install -r requirements.txt
```

### 5️⃣ Configure Environment
Create `.env` file:

```
BOT_TOKEN=your_bot_token
MONGO_URI=your_mongodb_url
API_ID=your_api_id
API_HASH=your_api_hash
```

### 6️⃣ Run The Bot
```bash
python3 -m Grabber
```

For 24/7 uptime use:

```bash
screen -S waifu
```
or
```bash
tmux
```

---

<h2 align="center">Core Features</h2>

<p align="center">
✔ Random anime character spawning<br>
✔ Collection & inventory system<br>
✔ Secure trading engine<br>
✔ Gift mechanics<br>
✔ Global leaderboard ranking<br>
✔ Harem customization<br>
✔ Cooldown management<br>
✔ Broadcast system<br>
</p>

---

<h2 align="center">Database</h2>

<p align="center">
Powered by MongoDB for scalable and efficient storage of users, chats, trades and leaderboard data.
</p>

---

<p align="center" style="color:#4B0082;">
Built with precision for anime communities.
Collect. Trade. Conquer.
</p>
