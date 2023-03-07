import random

import pygame.sprite

import game
from components.note import Note


class AnimatedBg:
    def __init__(self):
        self.__active_notes = pygame.sprite.Group()
        self.__spawning_time = pygame.time.get_ticks() + 500

    def render(self, surface: pygame.Surface):
        if pygame.time.get_ticks() >= self.__spawning_time:
            key_index = random.randint(0, 3)
            key = game.KEYBOARD_KEYS[key_index]
            self.__active_notes.add(Note((key.get_pos()[0], -100), 10, key))
            self.__spawning_time += 500
        for note in self.__active_notes:
            note.render(surface)
            note.move()
