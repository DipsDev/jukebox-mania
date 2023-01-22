import os
from pathlib import Path

import game
from utils import Utils


class LevelLoader:
    @staticmethod
    def load_level_beatmap(name):
        tile_data = []
        bpm = 0
        song_name = "Unknown"
        artist = "Unknown"
        reading_tiles = False
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
                    song_name = data[index+1]
                if line.startswith("TILES"):
                    reading_tiles = True
                elif reading_tiles:
                    tile_data.append(line)

        if not bpm or len(tile_data) == 0:
            print('Invalid level data:', name)
        music_path = f"./assets/levels/{name}/{name}-music.wav"
        if not os.path.exists(music_path):
            raise Exception(f"Cannot find music file for level: '{name}'")

        level_speed = (game.GameConstants.KEYS_HEIGHT / Utils.from_bpm_to_ms(int(bpm)) * 60)

        return tile_data, int(bpm), float(level_speed), music_path, (song_name.strip(), artist.strip())

    @staticmethod
    def get_available_levels():
        levels = []
        for child in Path("./assets/levels").iterdir():
            if child.is_dir():
                levels.append(child.name.replace("_", " "))
        return levels
