import pygame.sprite

import game
from components.KeyboardButton import KeyboardButton
from utils import Utils

track1_move_next_time = 0


class Note(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, tile_speed: int, adjacent_key: KeyboardButton, long_tile=False):
        super().__init__()
        self._adjacent_key = adjacent_key
        self._pos = pos
        self.hit_sound = pygame.mixer.Sound('./assets/sounds/hitsound.wav')
        self._tile_speed = tile_speed
        self._sprite = pygame.image.load("./assets/tile.png").convert_alpha()
        if not long_tile:
            self.resize()

    def resize(self):
        self._sprite = pygame.transform.scale(self._sprite, (self._adjacent_key.get_dimensions()[0], 30))

    def move(self):
        d = Utils.get_distance(self._pos[1], game.GameSettings.keys_height)
        print(d)
        if (d <= game.GameSettings.offset or self._sprite.get_rect().colliderect(self._adjacent_key.get_rect())) \
                and self._adjacent_key.is_clicked():
            self.hit_sound.set_volume(0.03)
            self.hit_sound.play()
            self.kill()
        self._pos = self._pos[0], self._pos[1] + self._tile_speed
        if self._pos[1] > 800:
            self.kill()

    def render(self, surface: pygame.Surface):
        surface.blit(self._sprite, self._sprite.get_rect(center=self._pos))
