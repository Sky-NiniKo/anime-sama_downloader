import re

from termcolor import colored
from yaspin import yaspin

from custom_client import CustomAsyncClient
from catalogue import Catalogue


class AnimeSama:
    def __init__(self, site_url: str) -> None:
        self.site_url = site_url
        self.client = CustomAsyncClient()

    async def search(self, query: str) -> list[Catalogue]:
        with yaspin(text=f"Searching for {colored(query, 'blue')}", color="cyan"):
            response = await self.client.post(
                f"{self.site_url}template-php/defaut/fetch.php", data={"query": query}
            )

            links = re.findall(r'href="(.+?)"', response.text)
            names = re.findall(r">(.+?)<\/h3>", response.text)

            return [
                Catalogue(url=link, name=name, client=self.client)
                for link, name in zip(links, names)
            ]
