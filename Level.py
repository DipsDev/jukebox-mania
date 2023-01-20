
import pygame.time

import game
from components.LongNote import LongNote
from components.Note import Note
from utils import Utils

NOTE = "x"
NOTES = [NOTE]


# Equation to bpm from interval and speed
# 60 / (interval / speed)

# ms = (4 + 1/3) * BPM


class Level:

    def __init__(self, level_data, keys):
        self.__keys = keys
        self.__line_counter = 0
        self.__level_data = level_data
        self.__active_notes = pygame.sprite.Group()
        self.__time_from_last_call = pygame.time.get_ticks() + Utils.from_bpm_to_ms(self.__level_data[1])

    def start(self):
        if not game.GameSettings.debug_mode:
            pygame.mixer.music.load(self.__level_data[3])
            pygame.mixer.music.play()

    def tick(self):
        time = pygame.time.get_ticks()
        if len(self.__level_data[0]) <= self.__line_counter:
            return

        # Simple notes logic
        if time > self.__time_from_last_call:
            for index, sign in enumerate(self.__level_data[0][self.__line_counter]):
                if sign not in NOTES and not sign.isnumeric():
                    continue
                pos = (self.__keys[index].get_pos()[0], 0)
                if sign.isnumeric():
                    self.__active_notes.add(LongNote(pos, self.__level_data[2], self.__keys[index],
                                                     Utils.from_bpm_to_ms(self.__level_data[1]) * 60 / 1000 * self.__level_data[2] *
                                                     int(sign), int(sign)))
                if sign == NOTE:

                    self.__active_notes.add(Note(pos, self.__level_data[2], self.__keys[index]))

            self.__line_counter += 1
            self.__time_from_last_call = time + Utils.from_bpm_to_ms(self.__level_data[1])

    def render(self, surface: pygame.Surface):
        for note in self.__active_notes:
            note.move()
            note.render(surface)




