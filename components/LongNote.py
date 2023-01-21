import pygame.transform

import game
from components.Note import Note
from utils import Utils


class LongNote(Note):
    def __init__(self, pos, tile_speed, adjacent_key, height: int, holding_ms: int):
        super().__init__(pos, tile_speed, adjacent_key)
        self._height = height
        self._original_height = height
        self._holding_ms = holding_ms
        self._holding_time_counter = 0
        self.__active = True
        self.__total_rect = None
        self.__middle_long_tile = pygame.image. \
            load(f"./assets/notes/long_notes/{adjacent_key.get_color()}_tile/{adjacent_key.get_color()}_tile_mid.png")
        self.__top_long_tile = pygame.image. \
            load(f"./assets/notes/long_notes/{adjacent_key.get_color()}_tile/{adjacent_key.get_color()}_tile_top.png")
        self.__bot_long_tile = pygame.image. \
            load(f"./assets/notes/long_notes/{adjacent_key.get_color()}_tile/{adjacent_key.get_color()}_tile_bot.png")
        self.resize()

    def resize(self):
        self._original_height = self._sprite.get_height()
        self.__middle_long_tile = pygame.transform.smoothscale(self.__middle_long_tile,
                                                               (self.__middle_long_tile.get_width(),
                                                                round(self._height + self._original_height)))

    def render(self, surface: pygame.Surface):
        pos = (self._pos[0], self._pos[1] + self._original_height / 2 - 5)
        surface.blit(self.__bot_long_tile,
                     self.__bot_long_tile.get_rect(center=(pos[0], self._pos[1])))
        surface.blit(self.__middle_long_tile,
                     self.__middle_long_tile.get_rect(
                         midbottom=(pos[0], pos[1] - 3.3 * self.__bot_long_tile.get_height())))
        surface.blit(self.__top_long_tile,
                     self.__top_long_tile.get_rect(
                         center=(pos[0], pos[1] - self._height - 1.5 * self._original_height)))

    def move(self):
        pos = (self._pos[0], self._pos[1] + self._original_height / 2 - 5)
        tail = self.__middle_long_tile.get_rect(
                         midbottom=(pos[0], pos[1] - 3.3 * self.__bot_long_tile.get_height())).midtop
        wing = self.__middle_long_tile.get_rect(
                         midbottom=(pos[0], pos[1] - 3.3 * self.__bot_long_tile.get_height())).midbottom
        is_colliding = tail[1] < self._adjacent_key.get_pos()[1] < wing[1]
        if is_colliding and (self._adjacent_key.is_held()):
            self._holding_time_counter += 1

        if self.__active and self._holding_time_counter / game.GameSettings.game_fps >= self._holding_ms / 1000:
            game.GameWindow.level_running.add_user_score(
                round(1.3 * min(self._holding_time_counter, (self._holding_ms // 100))))
            self.__active = False

        if tail[1] >= 1.3 * round(self._height + self._original_height):
            game.GameWindow.level_running.add_user_score(-2
                                                         * round((self._holding_ms / 1000 - self._holding_time_counter / game.GameSettings.game_fps)))
            self.kill()

        self._pos = self._pos[0], self._pos[1] + self._tile_speed
