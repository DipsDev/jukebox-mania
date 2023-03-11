import os
from pathlib import Path

from utils.types import LevelData, Song


class LevelLoader:
    @staticmethod
    def load_level_beatmap(name):
        name = name.replace('"', "")
        tile_data = []
        bpm = 0
        song_name = "Unknown"
        artist = "Unknown"
        diff = "easy"
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
                elif line.startswith("SPEED"):
                    level_speed = data[index + 1]
                elif line.startswith("ARTIST"):
                    artist = data[index + 1]
                elif line.startswith("NAME"):
                    song_name = data[index + 1]
                elif line.startswith("DIFFICULTY"):
                    diff = data[index + 1]
                elif line.startswith("TILES"):
                    reading_tiles = True
                elif reading_tiles:
                    if line.startswith("#"):
                        continue
                    tile_data.append(line)

        if not bpm or len(tile_data) == 0:
            print('Invalid level data:', name)
        music_path = f"./assets/levels/{name}/audio.wav"
        if not os.path.exists(music_path):
            raise Exception(f"Cannot find music file for level: '{name}', Make sure the file is called 'audio.wav'")

        return LevelData(tile_data,
                         int(bpm),
                         float(level_speed),
                         music_path,
                         Song(song_name.strip(),
                              artist.strip()),
                         diff)

    @staticmethod
    def get_available_levels():
        levels = []
        for child in Path("./assets/levels").iterdir():
            if child.is_dir() and LevelLoader.is_valid_level(child.name) and not child.name.startswith("__"):
                levels.append((child.name.replace("_", " "),
                               LevelLoader.get_level_artist(child.name),
                               LevelLoader.get_level_difficulty(child.name),
                               LevelLoader.is_level_recommended(child.name)))
            elif not LevelLoader.is_valid_level(child.name):
                print(f"Invalid level: '{child.name}', ignoring...")
        return levels

    @staticmethod
    def is_valid_level(level_name: str):
        dir_path = f"./assets/levels/{level_name}"
        flag = os.path.exists(dir_path) and len(os.listdir(dir_path)) == 2
        return flag

    @staticmethod
    def get_level_difficulty(level_name):
        diff = "easy"
        with open(f"./assets/levels/{level_name}/{level_name}.beatmap", 'r') as music_file:
            music_data = music_file.readlines()
            for index, line in enumerate(music_data):
                if line.startswith("DIFFICULTY"):
                    diff = music_data[index + 1]
        return diff.strip().title()

    @staticmethod
    def get_level_artist(level_name):
        artist = "Unknown"
        with open(f"./assets/levels/{level_name}/{level_name}.beatmap", 'r') as music_file:
            music_data = music_file.readlines()
            for index, line in enumerate(music_data):
                if line.startswith("ARTIST"):
                    artist = music_data[index + 1]
        return artist

    @staticmethod
    def is_level_recommended(level_name):
        is_recommended = False
        with open(f"./assets/levels/{level_name}/{level_name}.beatmap", 'r') as music_file:
            music_file = music_file.readlines()
            if music_file[0].startswith("RECOMMEND"):
                is_recommended = True
        return is_recommended
