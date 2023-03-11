import game
from collections import ChainMap


class Utils:
    @staticmethod
    def from_bpm_to_ms(bpm: int):
        return 60_000 / bpm / 2

    @staticmethod
    def get_distance(pos1y, pos2y):
        return abs(pos1y - pos2y)

    @staticmethod
    def get_high_score(level_name):
        high_scores = game.GameWindow.database.get_data("high_score")
        high_scores = dict(ChainMap(*high_scores))
        return high_scores.get(Utils.encode_string(level_name))

    @staticmethod
    def encode_string(string1: str):
        return string1.lower().replace(" ", "_")

    @staticmethod
    def update_highscore(encoded_level_name: str, value: int):
        sum_dict = {}
        scores = game.GameWindow.database.get_data("high_score")
        for d in scores:
            sum_dict.update(d)
        if not sum_dict.get(encoded_level_name) or sum_dict.get(encoded_level_name) < value:
            game.GameWindow.database.set_data("high_score", {encoded_level_name: value})
