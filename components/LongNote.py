import pygame.transform

from components.Note import Note


class LongNote(Note):
    def __init__(self, pos, tile_speed, adjacent_key, height: int, holding_beats: int):
        super().__init__(pos, tile_speed, adjacent_key, True)
        self._height = height
        self._original_height = height
        self._holding_beats = holding_beats
        self._started = False
        self._holding_time_counter = 0
        self.__middle_long_tile = pygame.image. \
            load(f"./assets/notes/long_notes/{adjacent_key.get_color()}_tile/{adjacent_key.get_color()}_tile_mid")
        self.__top_long_tile = pygame.image. \
            load(f"./assets/notes/long_notes/{adjacent_key.get_color()}_tile/{adjacent_key.get_color()}_tile_top")
        self.__bot_long_tile = pygame.image. \
            load(f"./assets/notes/long_notes/{adjacent_key.get_color()}_tile/{adjacent_key.get_color()}_tile_bot")
        self.resize()

    def resize(self):
        self._original_height = self._sprite.get_height()
        self.__middle_long_tile = pygame.transform.smoothscale(self.__middle_long_tile,
                                                               (self.__middle_long_tile.get_width(),
                                                                round(self._height + self._original_height)))

    def render(self, surface: pygame.Surface):
        pos = (self._pos[0], self._pos[1] + self._original_height / 2)
        if not self._started:
            surface.blit(self.__bot_long_tile, self.__bot_long_tile.get_rect(midbottom=pos))
            self._started = True
            return
        surface.blit(self.__middle_long_tile, self.__middle_long_tile.get_rect(midbottom=(pos[0], pos[1] + self.__bot_long_tile.get_height())))

    def move(self):
        # Implement Logic!
        mid_bottom = (self._pos[0], self._pos[1] - self._original_height / 2)
        is_colliding = self._sprite.get_rect(midbottom=mid_bottom) \
            .colliderect(self._adjacent_key.get_rect())

        self._pos = self._pos[0], self._pos[1] + self._tile_speed
        if self._pos[1] > 800 + self._sprite.get_height():
            self.kill()
