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
        self.__level_score = 0
        self.__level_data = level_data
        self.__active_notes = pygame.sprite.Group()
        self.__time_from_last_call = pygame.time.get_ticks() + Utils.from_bpm_to_ms(self.__level_data[1])

    def start(self):
        game.GameWindow.level_running = self
        if not game.GameSettings.debug_mode:
            pygame.mixer.music.load(self.__level_data[3])
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play()
        song_name = game.main_font.render(f"Currently Playing: {self.__level_data[-1][0]}", True, (229, 161, 89))
        song_artist = game.main_font.render(f"By: {self.__level_data[-1][1]}", True, (255, 255, 255))
        game.GameWindow.game_background.blit(song_name, (1440 / 2 - song_name.get_width() / 2, 130))

    def add_user_score(self, score: float):
        self.__level_score += score
        self.__level_score = max(self.__level_score, 0)

    def tick(self):
        time = pygame.time.get_ticks()
        if len(self.__level_data[0]) <= self.__line_counter:
            print("Level finished")
            return

        # Simple notes logic
        if time > self.__time_from_last_call:
            for index, sign in enumerate(self.__level_data[0][self.__line_counter]):
                if sign not in NOTES and not sign.isnumeric():
                    continue
                pos = (self.__keys[index].get_pos()[0], 0)
                if sign.isnumeric():
                    self.__active_notes.add(LongNote(pos, self.__level_data[2], self.__keys[index],
                                                     Utils.from_bpm_to_ms(self.__level_data[1]) * 60 / 1000 *
                                                     self.__level_data[2] *
                                                     int(sign), Utils.from_bpm_to_ms(self.__level_data[1]) * int(sign)))
                if sign == NOTE:
                    self.__active_notes.add(Note(pos, self.__level_data[2], self.__keys[index]))

            self.__line_counter += 1
            self.__time_from_last_call = time + Utils.from_bpm_to_ms(self.__level_data[1])

    def render(self, surface: pygame.Surface):
        level_score = game.main_font.render(f"Score: {self.__level_score}", True, (255, 255, 255))
        surface.blit(level_score, level_score.get_rect(center=(1440 / 2, 100)))
        for note in self.__active_notes:
            note.render(surface)
            note.move()

