import dataclasses
from typing import NamedTuple


class Song(NamedTuple):
    song_name: str
    artist_name: str


@dataclasses.dataclass
class LevelData:
    tile_data: list
    song_bpm: int
    level_speed: float
    music_path: str
    song_data: Song
    difficulty: str = "easy"
