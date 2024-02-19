import re
import asyncio
from itertools import zip_longest

import httpx
from termcolor import colored
from yaspin import kbi_safe_yaspin

from custom_client import CustomAsyncClient
from episode import Episode, Players, Languages


class Season:
    def __init__(
        self, url: str, name="", serie_name="", client: httpx.AsyncClient = None
    ) -> None:
        self.vf_url = url + "vf/"
        self.vostfr_url = url + "vostfr/"
        self.site_url = "/".join(url.split("/")[:3]) + "/"

        self.name = name or url.split("/")[-2]
        self.serie_name = serie_name or None

        self.client = client or CustomAsyncClient()

    async def episodes(self) -> list[Episode]:
        with kbi_safe_yaspin(
            text=f"Getting episode list for {colored(self.name, 'blue')}", color="cyan"
        ):

            async def get_players_links_from(page):
                response = await self.client.get(page)

                if not response.is_success:
                    return ()

                episodes_url = page + re.search(
                    r"episodes\.js\?filever=\d+", response.text
                ).group(0)
                episodes_js = await self.client.get(episodes_url)

                players_list = episodes_js.text.split("[")[1:]
                players_list_links = (
                    re.findall(r"'(.+?)'", player) for player in players_list
                )

                return zip(*players_list_links)

            episodes_pages = await asyncio.gather(
                get_players_links_from(self.vf_url),
                get_players_links_from(self.vostfr_url),
            )

            return [
                Episode(
                    Languages(*(Players(players) for players in players_links)),
                    self.serie_name,
                    self.name,
                    index,
                )
                for index, players_links in enumerate(
                    zip_longest(*episodes_pages, fillvalue=[]), start=1
                )
            ]

    def __repr__(self):
        return f"Season({self.vf_url[:-3]!r}, {self.name!r}, VF={self.has_vf})"

    def __str__(self):
        return self.name
