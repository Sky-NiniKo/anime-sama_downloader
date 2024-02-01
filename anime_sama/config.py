from pathlib import Path

prefer_vf = True
download_path = Path("~/Downloads/Anime-Sama")

url = "https://anime-sama.fr/"

players = {
    "prefer": ["anime-sama", "sibnet", "sendvid"],
    "ban": ["myvid"]
}

concurrent_downloads = {
    "fragment": 3,
    "video": 5
}