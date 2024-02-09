import re

import httpx

from season import Season

class Catalogue:
    def __init__(self, url: str, name="", client: httpx.AsyncClient = None) -> None:
        self.url = url
        self.name = name or url.split("/")[-2]
        self.site_url = "/".join(url.split("/")[:3]) + "/"
        self.client = client or httpx.AsyncClient()

    async def seasons(self) -> list[Season]:
        response = await self.client.get(self.url)

        seasons = re.findall(r'panneauAnime\("(.+?)", *"(.+?)vostfr"\);', response.text)[1:]

        seasons = [
            Season(
                url=self.url + link,
                name=name,
                serie_name=self.name,
                client=self.client
            )
            for name, link in seasons
        ]

        # await asyncio.gather(*(asyncio.create_task(season.post_init()) for season in seasons))
        return seasons

    def __repr__(self):
        return f"Catalogue({self.url!r}, {self.name!r})"

    def __str__(self):
        return self.name
