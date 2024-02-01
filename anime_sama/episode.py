from itertools import product


class Episode:
    def __init__(self, players: list[str], serie_name="", season_name="", index=1) -> None:
        self.players = players
        self.serie_name = serie_name
        self.season_name = season_name
        self.index = index

        self.name = f"{season_name} - Episode {index:02}"
        self.best_player = None

    def get_best_player(self) -> str:
        if self.best_player is None:
            self.set_best_player()

        return self.best_player

    def set_best_player(self, prefers: list[str] = None, bans: list[str] = None) -> None:
        if prefers is None:
            prefers = []

        if bans is None:
            bans = []

        for prefer, player in product(prefers, self.players):
            if prefer in player:
                self.best_player = player
                return

        for i in range(self.index, len(self.players) + self.index):
            if self.players[i % len(self.players)] not in bans:
                self.best_player = self.players[i % len(self.players)]
                return

        print(f"WARNING: No player found for {self}")

    def __repr__(self):
        return f"Episode({self.season_name!r}, {self.index!r}, {self.best_player!r})"

    def __str__(self):
        return self.name
