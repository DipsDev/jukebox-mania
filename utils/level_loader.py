
import os
from pathlib import Path

from utils.types import LevelData, Song


class LevelLoader:
    @staticmethod
    def load_level_beatmap(name):
        tile_data = []
        bpm = 0
        song_name = "Unknown"
        artist = "Unknown"
        reading_tiles = False
        level_speed = 1
        if not os.path.exists(f"./assets/levels/{name}/{name}.beatmap"):
            raise Exception(f"Cannot find beatmap '{name}'")
        with open(f"./assets/levels/{name}/{name}.beatmap", "r") as f:
            data = f.readlines()
            for index, line in enumerate(data):
                line = line.strip()
                if line.startswith("BPM"):
                    bpm = data[index + 1]
                if line.startswith("SPEED"):
                    level_speed = data[index + 1]
                if line.startswith("ARTIST"):
                    artist = data[index + 1]
                if line.startswith("NAME"):
                    song_name = data[index + 1]
                if line.startswith("TILES"):
                    reading_tiles = True
                elif reading_tiles:
                    tile_data.append(line)

        if not bpm or len(tile_data) == 0:
            print('Invalid level data:', name)
        music_path = f"./assets/levels/{name}/{name}-music.wav"
        if not os.path.exists(music_path):
            raise Exception(f"Cannot find music file for level: '{name}'")

        return LevelData(tile_data, int(bpm), float(level_speed), music_path, Song(song_name.strip(), artist.strip()))

    @staticmethod
    def get_available_levels():
        levels = []
        for child in Path("./assets/levels").iterdir():
            if child.is_dir() and LevelLoader.is_valid_level(child.name):
                levels.append((child.name.replace("_", " "), LevelLoader.get_level_artist(child.name)))
            elif not LevelLoader.is_valid_level(child.name):
                print(f"Invalid level: '{child.name}', Ignoring...")
        return levels

    @staticmethod
    def is_valid_level(level_name: str):
        dir_path = f"./assets/levels/{level_name}"
        flag = os.path.exists(dir_path) and len(os.listdir(dir_path)) == 2
        return flag

    @staticmethod
    def get_level_artist(level_name):
        artist = "Unknown"
        with open(f"./assets/levels/{level_name}/{level_name}.beatmap", 'r') as music_file:
            music_data = music_file.readlines()
            for index, line in enumerate(music_data):
                if line.startswith("ARTIST"):
                    artist = music_data[index + 1]
            return artist

