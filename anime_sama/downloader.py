from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from yt_dlp import YoutubeDL
from tqdm import tqdm

from utils import put_color
from episode import Episode


class OnlyErrorLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


class TqdmYoutubeDL(tqdm):
    def __init__(self, *args, **kwargs):
        super().__init__(unit="B", unit_scale=True, mininterval=1, *args, **kwargs)

    def hook(self, data):
        if data["status"] != "downloading":
            return

        if not self.total:
            self.total = data["total_bytes"]
            # Resume download
            self.last_print_n = data["downloaded_bytes"]
            self.last_print_t = self._time()
            return

        self.update(data["downloaded_bytes"] - self.n)


def download(
    episode: Episode, path: Path, concurrent_fragment_downloads=3, main_tqdm_bar=None
):
    full_path = (
        path / episode.serie_name / episode.season_name / episode.name
    ).expanduser()

    with TqdmYoutubeDL(
        desc=put_color("red") + episode.short_name,
        leave=not bool(main_tqdm_bar),
    ) as tqdm_bar:
        option = {
            "outtmpl": {"default": f"{full_path}.%(ext)s"},
            "concurrent_fragment_downloads": concurrent_fragment_downloads,
            "progress_hooks": [tqdm_bar.hook],
            "logger": OnlyErrorLogger(),
        }

        with YoutubeDL(option) as ydl:
            ydl.download([episode.languages.best])

    if main_tqdm_bar is not None:
        main_tqdm_bar.update()


def multi_download(episodes: list[Episode], path: Path, concurrent_downloads):
    print(put_color("light_red"), end="")
    with tqdm(total=len(episodes), unit="Ep") as tqdm_bar:
        with ThreadPoolExecutor(max_workers=concurrent_downloads["video"]) as executor:
            executor.map(
                lambda episode: download(
                    episode, path, concurrent_downloads["fragment"], tqdm_bar
                ),
                episodes,
            )
