<h1 align="center" style="color:#6A0DAD;">Waifu Grabber Bot</h1>

<p align="center">
  <img src="https://media.animerealms.org/image/AgACAgUAAx0EboWBewAC0BtplqHQCOjxeRga-VXIGOSD1pkNkwACEw5rG1zpuVSZRvn7c_fYRgEAAwIAA3kAAzoE" width="260"/>
</p>

<p align="center">
A fun and competitive Telegram anime game where you grab random waifus, grow your collection, trade strategically, and rise through the global leaderboard.<br>
Collect rare characters, build your ultimate harem, and dominate the multiverse — all for pure fun.
</p>


<h2 align="center">Deploy on Heroku</h2>

<p align="center">
<a href="https://heroku.com/deploy?template=https://github.com/Akatsumo/WaifuGrabberBot">
  <img src="https://img.shields.io/badge/Deploy%20to%20Heroku-000000?style=for-the-badge&logo=heroku&logoColor=white" alt="Deploy to Heroku">
</a>
</p>


<h2 align="center">Deploy on VPS Server</h2>

<p align="center">
<a href="#vps-deployment">
  <img src="https://img.shields.io/badge/Deploy%20on%20VPS-000000?style=for-the-badge&logo=linux&logoColor=white" alt="Deploy on VPS">
</a>
</p>

---

<h3 align="center" id="vps-deployment">VPS Deployment Guide</h3>

### Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### Install Required Packages
```bash
sudo apt install python3 python3-pip git -y
```

### Clone Repository
```bash
git clone https://github.com/Akatsumo/WaifuGrabberBot.git
cd WaifuGrabberBot
```

### Install Dependencies
```bash
pip3 install -r requirements.txt
```

### Configure Environment
Create a `.env` file inside the project folder:

```
BOT_TOKEN=your_bot_token
MONGO_URI=your_mongodb_uri
API_ID=your_api_id
API_HASH=your_api_hash
```

### Start The Bot
```bash
python3 -m Grabber
```

For 24/7 uptime:
```bash
screen -S waifu
```
or
```bash
tmux
```

<h2 align="center">User Commands</h2>

<p align="center">

| Command | Description |
|---------|------------|
| `/grab` | Grab a random waifu from the multiverse |
| `/animes` | View available anime collections |
| `/mywaifus` | Check your collected waifus |
| `/gift` | Gift one of your waifus to another user |
| `/trade` | Trade waifus securely with another user |
| `/harem` | View your selected waifu lineup |
| `/leaderboard` | See the global top collectors ranking |
| `/changetime` | Set the waifu spawn cooldown |

</p>


<h2 align="center">Master Commands</h2>

<p align="center">

| Command | Description |
|---------|------------|
| `/addwaifu` | Add a waifu to the multiverse |
| `/stats` | View complete bot statistics |
| `/broadcast` / `/announce` | Send a global announcement to all users |
| `/delete` | Remove a waifu from the system |

</p>

<h2 align="center">Final Note</h2>

<p align="center">
Waifu Grabber Bot isn’t just a project — it’s a growing anime game ecosystem built for communities who love collecting, competing, and creating memorable moments together.<br><br>
If you enjoy the concept, feel free to fork the repository, improve it, and contribute. Every pull request helps shape a better and stronger multiverse for everyone.
</p>
