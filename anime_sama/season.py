import httpx

from utils import find_pattern_in
from episode import Episode

class Season:
    def __init__(self, url: str, name="", serie_name: str = None, client: httpx.AsyncClient = None) -> None:
        self.vf_url = url + "vf/"
        self.vostfr_url = url + "vostfr/"
        self.site_url = "/".join(url.split("/")[:3]) + "/"

        self.name = name or url.split("/")[-2]
        self.serie_name = serie_name
        
        self.client = client or httpx.AsyncClient()
        self.has_vf = None

    async def post_init(self) -> None:
        self.has_vf = (await self.client.get(self.vf_url)).is_success
    
    async def episodes(self, perfer_vf=False) -> list[Episode]:
        if self.has_vf is None:
            await self.post_init()

        url = self.vf_url if perfer_vf and self.has_vf else self.vostfr_url
        response = await self.client.get(url)

        fileever_number = find_pattern_in(response.text, "'episodes.js?filever", "'")[0]
        episodes_url = url + "episodes.js?filever" + fileever_number

        episodes_js = await self.client.get(episodes_url)

        return [Episode(players, self.serie_name, self.name, index) for index, players in
            enumerate(
                zip(
                    *(eval(player) 
                    for player 
                    in find_pattern_in(episodes_js.text, "[", "]", with_pattern=True))
                ),
                start=1
            )
        ]
    
    def __repr__(self):
        return f"Season({self.vf_url[:-3]!r}, {self.name!r}, VF={self.has_vf})"
    
    def __str__(self):
        return self.name