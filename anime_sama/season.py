import re

import httpx

from episode import Episode

class Season:
    def __init__(self, url: str, name="", serie_name="", client: httpx.AsyncClient = None) -> None:
        self.vf_url = url + "vf/"
        self.vostfr_url = url + "vostfr/"
        self.site_url = "/".join(url.split("/")[:3]) + "/"

        self.name = name or url.split("/")[-2]
        self.serie_name = serie_name or None

        self.client = client or httpx.AsyncClient()
        self.has_vf = None

    async def post_init(self) -> None:
        self.has_vf = (await self.client.get(self.vf_url)).is_success

    async def episodes(self, perfer_vf=False) -> list[Episode]:
        if self.has_vf is None:
            await self.post_init()

        page_url = self.vf_url if perfer_vf and self.has_vf else self.vostfr_url
        response = await self.client.get(page_url)

        episodes_url = page_url + re.search(r'episodes\.js\?filever=\d+', response.text).group(0)

        episodes_js = await self.client.get(episodes_url)

        players_list = episodes_js.text.split("[")[1:]
        players_links = [re.findall(r"'(.+?)'", player) for player in players_list]

        return [
            Episode(players, self.serie_name, self.name, index)
            for index, players in enumerate(zip(*players_links), start=1)
        ]

    def __repr__(self):
        return f"Season({self.vf_url[:-3]!r}, {self.name!r}, VF={self.has_vf})"

    def __str__(self):
        return self.name
