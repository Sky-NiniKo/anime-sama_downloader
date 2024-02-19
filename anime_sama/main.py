import asyncio

from termcolor import colored

import config
import downloader
from utils import safe_input, select_one, select_range, put_color, keyboard_inter
from anime_sama import AnimeSama


async def main():
    catalogues = await AnimeSama(config.URL).search(
        safe_input("Anime name: " + put_color("blue"), str)
    )
    catalogue = select_one(catalogues)

    seasons = await catalogue.seasons()
    season = select_one(seasons)

    episodes = await season.episodes()
    print(
        colored(
            f"\n{season.serie_name} - {season.name}",
            "cyan",
            attrs=["bold", "underline"],
        )
    )
    selected_episodes = select_range(
        episodes, msg="Choose episode(s)", print_choices=False
    )

    for episode in selected_episodes:
        episode.languages.prefer_french = config.PREFER_VF
        episode.languages.set_best(config.PLAYERS["prefer"], config.PLAYERS["ban"])

    downloader.multi_download(
        selected_episodes, config.DOWNLOAD_PATH, config.CONCURRENT_DOWNLOADS
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        keyboard_inter()
