# 🕵️ DarkWebIntel

**DarkWebIntel** is an automated dark web intelligence crawler built with Scrapy, routed through the Tor network. It crawls `.onion` websites to search for sensitive keywords (e.g., emails, credentials, PII), logs matches, and stores leak evidence securely.

---

## 📌 Features

- Crawls `.onion` domains over Tor via `socks5h://127.0.0.1:9050`
- Scrapy-based spider with depth-limited exploration
- Target keyword matching using regex (from `targets.txt`)
- Saves matched leak URLs to `leaks.txt` and `leaks.csv`
- HTML dumps saved for offline review in `/logs`
- Automatically deduplicates findings
- Optional proxychains support for CLI routing

---

## ⚙️ Installation

```bash
# Update and install dependencies
sudo apt update && sudo apt install tor proxychains4 python3-pip git -y

# Install required Python packages
pip3 install requests beautifulsoup4 pandas scrapy

# Enable and start Tor
sudo systemctl enable tor
sudo systemctl start tor

# Confirm Tor works
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org

sudo nano /etc/proxychains4.conf
#Replace the last line with
socks5h  127.0.0.1 9050
#Test with:
proxychains curl http://check.torproject.org

#Create Project
scrapy startproject darkwebintel
cd darkwebintel
mkdir logs
touch leaks.txt onions.txt targets.txt

Project Folder Structure
darkwebintel/
├── darkwebintel/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       └── leaksearch.py
├── leaks.txt
├── onions.txt
├── targets.txt
├── logs/
└── scrapy.cfg

#Edit darkwebintel/darkwebintel/settings.py
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
}
HTTP_PROXY = 'socks5h://127.0.0.1:9050'

USER_AGENT = 'Mozilla/5.0 (compatible; LeakHunterBot/1.0)'
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 3
RETRY_TIMES = 3
LOG_LEVEL = 'INFO'
DEPTH_LIMIT = 10
COOKIES_ENABLED = False
REDIRECT_ENABLED = True
HTTPERROR_ALLOWED_CODES = [403, 404]

#Create leaksearch.py
nano darkwebintel/darkwebintel/spiders/leaksearch.py


