import httpx

from utils import find_pattern_in
from catalogue import Catalogue

class AnimeSama:
    def __init__(self, site_url: str) -> None:
        self.site_url = site_url
        self.client = httpx.AsyncClient()

    async def search(self, query: str) -> list[Catalogue]:
        response = await self.client.post(
            f"{self.site_url}template-php/defaut/fetch.php",
            data={"query": query}
        )

        xpaths = find_pattern_in(
            response.text,
            f"\"{self.site_url}catalogue/", '" '
        )

        names = find_pattern_in(
            response.text,
            "<h3 class=\"text-xs uppercase font-extrabold\">", "</h3>"
        )

        return [
            Catalogue(
                url=f"{self.site_url}catalogue/{xpath}/",
                name=name,
                client=self.client
            )
            for xpath, name in zip(xpaths, names)
        ]
