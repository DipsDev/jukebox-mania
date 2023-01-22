
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

