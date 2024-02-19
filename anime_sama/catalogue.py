import re

import httpx
from termcolor import colored
from yaspin import kbi_safe_yaspin

from custom_client import CustomAsyncClient
from season import Season


class Catalogue:
    def __init__(self, url: str, name="", client: httpx.AsyncClient = None) -> None:
        self.url = url + "/" if url[-1] != "/" else url
        self.name = name or url.split("/")[-2]
        self.site_url = "/".join(url.split("/")[:3]) + "/"
        self.client = client or CustomAsyncClient()

    async def seasons(self) -> list[Season]:
        with kbi_safe_yaspin(
            text=f"Getting season list for {colored(self.name, 'blue')}", color="cyan"
        ):
            response = await self.client.get(self.url)

            seasons = re.findall(
                r'panneauAnime\("(.+?)", *"(.+?)(?:vostfr|vf)"\);', response.text
            )

            seasons = [
                Season(
                    url=self.url + link,
                    name=name,
                    serie_name=self.name,
                    client=self.client,
                )
                for name, link in seasons
            ]

            # await asyncio.gather(*(asyncio.create_task(season.post_init()) for season in seasons))
            return seasons

    def __repr__(self):
        return f"Catalogue({self.url!r}, {self.name!r})"

    def __str__(self):
        return self.name
