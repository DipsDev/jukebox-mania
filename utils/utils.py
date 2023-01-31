import game
from collections import ChainMap


class Utils:
    @staticmethod
    def from_bpm_to_ms(bpm: int):
        return 60_000 / bpm

    @staticmethod
    def get_distance(pos1y, pos2y):
        if pos1y >= pos2y:
            return pos1y - pos2y
        else:
            return pos2y - pos1y

    @staticmethod
    def get_high_score(level_name):
        high_scores = game.GameWindow.database.get_data("high_score")
        high_scores = dict(ChainMap(*high_scores))
        return high_scores.get(Utils.encode_string(level_name))

    @staticmethod
    def encode_string(string1: str):
        return string1.lower().replace(" ", "_")
