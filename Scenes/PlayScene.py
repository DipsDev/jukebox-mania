import pygame

import game
from Level import Level
from assets.assets_loading import background_img


class PlayScene:
    def __init__(self, level: Level):
        self.__level = level
        self.__first_time = True

    def play(self, screen):
        if self.__first_time:
            self.__level.start()
            self.__first_time = False
        self.__level.tick()
        self.__level.render(screen)
        for keyboard_key in game.keyboard_keys:
            keyboard_key.click_tick()
            keyboard_key.render(screen)
