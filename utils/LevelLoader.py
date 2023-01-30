import os
from pathlib import Path


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

        return tile_data, int(bpm), float(level_speed), music_path, (song_name.strip(), artist.strip())

    @staticmethod
    def get_available_levels():
        levels = []
        for child in Path("./assets/levels").iterdir():
            if child.is_dir():
                levels.append((child.name.replace("_", " "), LevelLoader.get_level_artist(child.__str__())))
        return levels

    @staticmethod
    def is_valid_level(dir_path: str):
        return not os.path.exists(dir_path) or len([name for name in os.listdir(dir_path) if os.path.isfile(name)]) != 2

    @staticmethod
    def get_level_artist(dir_path):
        level_name = dir_path.split("\\")[-1]
        artist = "Unknown"
        with open(f"./assets/levels/{level_name}/{level_name}.beatmap", 'r') as music_file:
            music_data = music_file.readlines()
            for index, line in enumerate(music_data):
                if line.startswith("ARTIST"):
                    artist = music_data[index + 1]
            return artist

