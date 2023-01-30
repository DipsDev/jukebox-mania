import pygame.time

import game
from assets.assets_loading import background_img
from components.long_note import LongNote
from components.note import Note
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
        self.__music_started = False
        self.__starting_timer = 300
        self.__level_score = 0
        self.__level_data = level_data
        pygame.mixer.music.load(self.__level_data[3])
        self.__active_notes = pygame.sprite.Group()
        self.__bpm_in_ms = Utils.from_bpm_to_ms(level_data[1])
        self.__song_progression = 0
        self.__time_falling_ms = (game.GameConstants.KEYS_RECT_HEIGHT / self.__level_data[2])
        self.__time_from_last_call_ms = self.__bpm_in_ms

    def start(self):
        game.GameWindow.game_background.blit(background_img, (0, 0))
        game.GameWindow.level_running = self
        game.GameWindow.combo_counter = 0
        song_name = game.main_font.render(
            f"Currently Playing: {self.__level_data[-1][0].title()}",
            True,
            (229, 161, 89))
        game.GameWindow.game_background.blit(song_name, (1440 / 2 - song_name.get_width() / 2, 130))

    def start_music(self):
        if not game.GameConstants.DEBUG_MODE and not self.__music_started:
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play()
            self.__time_from_last_call_ms = pygame.mixer.music.get_pos() + self.__bpm_in_ms
            self.__music_started = True

    def add_user_score(self, score: float):
        if score > 0:
            game.GameWindow.combo_counter += 1
            self.__level_score += round(score * (game.GameWindow.combo_counter * game.GameConstants.COMBO_MULTIPLIER))
        else:
            self.__level_score += score
            game.GameWindow.combo_counter = 0
        self.__level_score = max(self.__level_score, 0)

    def generate_new_notes(self):
        for index, sign in enumerate(self.__level_data[0][self.__line_counter]):
            if sign not in NOTES and not sign.isnumeric():
                continue
            pos = (self.__keys[index].get_pos()[0], 0)
            if sign.isnumeric():
                self.__active_notes.add(LongNote(pos, self.__level_data[2], self.__keys[index],
                                                 Utils.from_bpm_to_ms(self.__level_data[1]) * 60 / 1000 *
                                                 self.__level_data[2] *
                                                 int(sign), self.__bpm_in_ms * int(sign)))
            if sign == NOTE:
                self.__active_notes.add(Note(pos, self.__level_data[2], self.__keys[index]))
        self.__line_counter += 1

    def tick(self):
        if self.__starting_timer >= 0:
            r = game.main_font.render(f"Starting in {self.__starting_timer // 100 + 1}", True, (255, 255, 255))
            game.GameWindow.screen.blit(r, r.get_rect(center=(1440 / 2, 800 / 2)))
            self.__starting_timer -= 1
            return

        self.start_music()

        if len(self.__level_data[0]) <= self.__line_counter:
            print("Level finished")
            game.GameWindow.database.set_data("best_score", {self.__level_data[-1][0]: self.__level_score})
            game.GameWindow.level_running = None
            game.GameWindow.game_state = game.GameStates.LEVEL_BROWSER
            return
        if self.__song_progression > self.__time_from_last_call_ms:
            self.generate_new_notes()
            self.__time_from_last_call_ms += self.__bpm_in_ms
        self.__song_progression += game.GameWindow.clock.get_time()

    def render(self, surface: pygame.Surface):
        level_score = game.main_font.render(f"Score: {self.__level_score}", True, (255, 255, 255))
        surface.blit(level_score, level_score.get_rect(center=(1440 / 2, 100)))
        combo_counter = game.small_font.render(f"X {game.GameWindow.combo_counter}", True, (204, 190, 234))
        surface.blit(combo_counter, combo_counter.get_rect(center=(1440 / 2, 70)))
        for note in self.__active_notes:
            note.render(surface)
            note.move()

        surface.blit(game.keys_background, game.keys_background.get_rect(topleft=(204, 730)))
