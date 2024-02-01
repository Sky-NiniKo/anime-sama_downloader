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

If you can't install poetry: `pip install -r requirements.txt` but be warn, it is not supported.

## Config
You can customize the config in `anime_sama/config.py`

```yaml
PREFER_VF: If you want to download the french version (if available)
DOWNLOAD_PATH: Where to place downloaded videos
URL: url of anime-sama (You shouldn't touch that)
PLAYERS:
    prefer: player to use if multiple are available (first in the list are prefer over the afters)
    ban: player to not use (even if that the only player)
CONCURRENT_DOWNLOADS:
    fragment: how many fragment of a video to download at once
    video: how many video to download at once
```

# Contribution
I am open to contribution.