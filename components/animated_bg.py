import random

import pygame.sprite

import game
from components.long_note import LongNote
from components.note import Note


class AnimatedBg:
    def __init__(self):
        self.__active_notes = pygame.sprite.Group()
        self.__spawning_time = pygame.time.get_ticks() + 500

    def render(self, surface: pygame.Surface):
        if pygame.time.get_ticks() >= self.__spawning_time:
            key_index = random.randint(0, 3)
            speed_rnd = random.randint(7, 10)
            offsets_lst = [i for i in range(-10, 11, 5)]
            key = game.KEYBOARD_KEYS[key_index]
            self.__active_notes.add(Note((key.get_pos()[0] + random.choice(offsets_lst), -100), speed_rnd, key))
            self.__spawning_time += 500
        for note in self.__active_notes:
            note.render(surface)
            note.move()
