import re
from itertools import product
from dataclasses import dataclass, field

from termcolor import colored

zero = re.match(r"\d", "0")


@dataclass
class Players:
    availables: list[str] = field(default_factory=list)
    _best: str = field(default=None, init=False)
    index: int = field(default=1, init=False)

    @property
    def best(self) -> str:
        if self._best is None:
            self.set_best()

        return self._best

    def set_best(self, prefers: list[str] = None, bans: list[str] = None) -> None:
        if not self.availables:
            return

        if prefers is None:
            prefers = []

        if bans is None:
            bans = []

        for prefer, player in product(prefers, self.availables):
            if prefer in player:
                self._best = player
                return

        for i in range(self.index, len(self.availables) + self.index):
            candiate = self.availables[i % len(self.availables)]

            if all(ban not in candiate for ban in bans):
                self._best = candiate
                return

        print(colored(f"WARNING: No player found for {self}", "yellow"))


@dataclass
class Languages:
    french: Players
    original: Players

    prefer_french: bool = field(default=False, init=False)

    def __post_init__(self):
        self.has_vf = bool(self.french.availables)
        self.availables = (self.french, self.original)

    @property
    def best(self) -> str:
        return (
            self.french._best
            if self.prefer_french and self.has_vf
            else self.original._best
        )

    def set_best(self, *args, **kwargs):
        for players in self.availables:
            players.set_best(*args, **kwargs)


@dataclass
class Episode:
    languages: Languages

    serie_name: str = ""
    season_name: str = ""
    _index: int = 1

    def __post_init__(self) -> None:
        self.index = self._index

        self.season_number = int((re.search(r"\d+", self.season_name) or zero).group(0))

        self.name = f"{self.season_name} - Episode {self.index:02}"
        self.short_name = f"{self.serie_name} S{self.season_number:02}E{self.index:02}"

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int):
        self._index = value
        for players in self.languages.availables:
            players.index = self._index

    def __str__(self):
        return self.name


if __name__ == "__main__":
    Episode(Languages(Players(), Players()))
