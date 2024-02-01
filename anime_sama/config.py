from pathlib import Path

PREFER_VF = True
DOWNLOAD_PATH = Path("~/Downloads/Anime-Sama")

URL = "https://anime-sama.fr/"

PLAYERS = {
    "prefer": ["anime-sama", "sibnet", "sendvid"],
    "ban": ["myvid"]
}

CONCURRENT_DOWNLOADS = {
    "fragment": 3,
    "video": 5
}
