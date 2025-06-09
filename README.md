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
sudo apt update && sudo apt install tor proxychains4 python3-pip git -y
pip3 install scrapy requests beautifulsoup4 pandas
sudo systemctl enable tor
sudo systemctl start tor
