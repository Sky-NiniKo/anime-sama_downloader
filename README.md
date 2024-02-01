# Anime-Sama Downloader
Download video from anime-sama.fr

# How to run
```bash
git clone https://github.com/Sky-NiniKo/anime-sama_downloader.git
cd anime-sama_downloader

poetry install
poetry run python anime_sama/main.py
```
If you don't have poetry, `pip install poetry`. And if you don't have pip, intall Python.

## Config
You can customize the config in `anime_sama/config.py`

```yaml
prefer_vf: If you want to download the french version (if available)
download_path: Where to place downloaded videos
url: url of anime-sama (You shouldn't touch that)
players:
    prefer: player to use if multiple are available (first in the list are prefer over the afters)
    ban: player to not use (even if that the only player)
concurrent_downloads:
    fragment: how many fragment of a video to download at once
    video: how many video to download at once
```

# Contribution
I am open to contribution.