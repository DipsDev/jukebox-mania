import pygame.transform

import game
from components.Note import Note
from utils import Utils


class LongNote(Note):
    def __init__(self, pos, tile_speed, adjacent_key, height: int, holding_beats: int):
        super().__init__(pos, tile_speed, adjacent_key, True)
        self._height = height
        self._original_height = height
        self._holding_beats = holding_beats
        self._holding_time_counter = 0
        self.resize()

    def resize(self):
        self._original_height = self._sprite.get_height()
        self._sprite = pygame.transform.scale(self._sprite, (self._sprite.get_width(),
                                                             self._height + self._original_height))

    def render(self, surface: pygame.Surface):
        surface.blit(self._sprite, self._sprite.get_rect(
            midbottom=(self._pos[0], self._pos[1] + self._original_height / 2)))

    def move(self):
        # Implement Logic!
        mid_bottom = (self._pos[0], self._pos[1] - self._original_height / 2)
        is_colliding = self._sprite.get_rect(midbottom=mid_bottom) \
            .colliderect(self._adjacent_key.get_rect())

        self._pos = self._pos[0], self._pos[1] + self._tile_speed
        if self._pos[1] > 800 + self._sprite.get_height():
            self.kill()
