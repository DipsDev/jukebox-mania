import pygame.sprite

import game
from components.KeyboardButton import KeyboardButton
from utils import Utils

track1_move_next_time = 0


class Note(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, tile_speed: int, adjacent_key: KeyboardButton):
        super().__init__()
        self._adjacent_key = adjacent_key
        self._pos = pos
        self.hit_sound = pygame.mixer.Sound('./assets/sounds/hitsound.wav')
        self._tile_speed = tile_speed
        self._sprite = pygame.image.load(f"./assets/notes/{adjacent_key.get_color()}_tile.png").convert_alpha()

    def move(self):
        d = Utils.get_distance(self._pos[1], game.GameConstants.KEYS_HEIGHT)
        if (d <= game.GameConstants.TOLERANCE_OFFSET or self._sprite.get_rect().colliderect(
                self._adjacent_key.get_rect())) \
                and self._adjacent_key.is_clicked():
            self.hit_sound.set_volume(0.3)
            self.hit_sound.play()
            game.GameWindow.level_running.add_user_score(25)
            self.kill()
        self._pos = self._pos[0], self._pos[1] + self._tile_speed
        if self._pos[1] > 800 + self._sprite.get_height() + 10:
            game.GameWindow.level_running.add_user_score(-15)
            self.kill()

    def render(self, surface: pygame.Surface):
        surface.blit(self._sprite, self._sprite.get_rect(center=self._pos))
