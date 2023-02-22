import game
from level import Level


class PlayScene:
    def __init__(self, level: Level):
        self.__level = level
        self.__first_time = True

    def play(self, screen) -> None:
        if self.__first_time:
            self.__level.start()
            self.__first_time = False
        self.__level.tick()
        self.__level.render(screen)
        for keyboard_key in game.KEYBOARD_KEYS:
            keyboard_key.click_tick()
            keyboard_key.render(screen)

    def toggle_pause(self):
        self.__level.pause()
