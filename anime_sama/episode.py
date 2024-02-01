from itertools import product


class Episode:
    def __init__(self, players: list[str], serie_name="", season_name="", index=1) -> None:
        self.players = players
        self.serie_name = serie_name
        self.season_name = season_name
        self.index = index

        self.name = f"{season_name} - Episode {index:02}"
        self.short_name = f"Ep {index}"
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
            candiate = self.players[i % len(self.players)]

            if all(ban not in candiate for ban in bans):
                self.best_player = candiate
                return

        print(f"WARNING: No player found for {self}")

    def __repr__(self):
        return f"Episode({self.season_name!r}, {self.index!r}, {self.best_player!r})"

    def __str__(self):
        return self.name
