import httpx

from utils import find_pattern_in
from season import Season

class Catalogue:
    def __init__(self, url: str, name="", client: httpx.AsyncClient = None) -> None:
        self.url = url
        self.name = name or url.split("/")[-2]
        self.site_url = "/".join(url.split("/")[:3]) + "/"
        self.client = client or httpx.AsyncClient()

    async def seasons(self) -> list[Season]:
        response = await self.client.get(self.url)

        seasons = (
            season.split(", ")
            for season in
            find_pattern_in(response.text, "\tpanneauAnime(\"", "vostfr\");")
        )

        seasons = [
            Season(
                url=self.url + xpath[1:],
                name=name[:-1],
                serie_name=self.name,
                client=self.client
            )
            for name, xpath in seasons
        ]

        # await asyncio.gather(*(asyncio.create_task(season.post_init()) for season in seasons))
        return seasons

    def __repr__(self):
        return f"Catalogue({self.url!r}, {self.name!r})"

    def __str__(self):
        return self.name
