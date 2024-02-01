import json
import asyncio
from typing import TypeVar, List

import config
import downloader
from anime_sama import AnimeSama
from utils import safe_input

T = TypeVar("T")


def print_selection(choices: list) -> None:
    if len(choices) == 0: exit("No result")
    if len(choices) == 1: return print(f"-> {choices[0]}")

    for index, choice in enumerate(choices, start=1):
        print(f"{index}: {choice}")


def select_one_from(choices: List[T]) -> T:
    print_selection(choices)
    if len(choices) == 1:
        return choices[0]

    return choices[safe_input("Choose a number: ", int) - 1]


def select_range_from(choices: List[T]) -> List[T]:
    print_selection(choices)
    if len(choices) == 1:
        return [choices[0]]

    ints = safe_input(f"Choose a range [1-{len(choices)}]: ", lambda string: tuple(map(int, string.split("-"))))
    if len(ints) == 1:
        return [choices[ints[0] - 1]]

    return choices[ints[0]-1:ints[1]]


async def main():
    catalogues = await AnimeSama(config.url).search(input("Anime name: "))
    catalogue = select_one_from(catalogues)

    seasons = await catalogue.seasons()
    season = select_one_from(seasons)

    episodes = await season.episodes(perfer_vf=config.prefer_vf)
    selected_episodes = select_range_from(episodes)

    for episode in selected_episodes: 
        episode.set_best_player(config.players["prefer"], config.players["ban"])

    downloader.multi_download(selected_episodes, config.download_path, config.concurrent_downloads)


asyncio.run(main())