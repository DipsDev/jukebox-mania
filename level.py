import pygame.time

import game
from assets import asset_loader
from components.long_note import LongNote
from components.note import Note
from utils import Utils
from utils.types import LevelData

NOTE = "x"
NOTES = [NOTE]


class Level:
    def __init__(self, level_data: LevelData, keys):
        self.__keys = keys
        self.__line_counter = 0
        self.__music_started = False
        self.__starting_timer = 300
        self.__ending_timer = 300
        self.__level_score = 0
        self.__level_data = level_data
        pygame.mixer.music.load(self.__level_data.music_path)
        self.__active_notes = pygame.sprite.Group()
        self.__bpm_in_ms = Utils.from_bpm_to_ms(level_data.song_bpm)
        self.__song_progression = 0
        self.__time_from_last_call_ms = self.__bpm_in_ms

    def start(self):
        game.GameWindow.game_background.blit(asset_loader.background_img, (0, 0))
        game.GameWindow.level_running = self
        game.GameWindow.combo_counter = 0
        song_name = asset_loader.medium_font.render(
            f"Currently Playing: {self.__level_data.song_data.song_name.title()}",
            True,
            (229, 161, 89))
        game.GameWindow.game_background.blit(song_name, (1440 / 2 - song_name.get_width() / 2, 130))

    def start_music(self):
        if not game.GameConstants.DEBUG_MODE and not self.__music_started:
            pygame.mixer.music.set_volume(game.music_volume / 10)
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
        for index, note_length in enumerate(self.__level_data.tile_data[self.__line_counter]):
            if note_length not in NOTES and not note_length.isnumeric():
                continue
            pos = (self.__keys[index].get_pos()[0], 0)
            if note_length.isnumeric():
                self.__active_notes.add(LongNote(pos, self.__level_data.level_speed, self.__keys[index],
                                                 Utils.from_bpm_to_ms(self.__level_data.song_bpm) * 60 / 1000 *
                                                 self.__level_data.level_speed *
                                                 int(note_length), self.__bpm_in_ms * int(note_length)))
            if note_length == NOTE:
                self.__active_notes.add(Note(pos, self.__level_data.level_speed, self.__keys[index]))
        self.__line_counter += 1

    def tick(self):
        if self.__starting_timer >= 0:
            r = asset_loader.medium_font.render(f"Starting in {self.__starting_timer // 100 + 1}", True, (255, 255, 255))
            game.GameWindow.screen.blit(r, r.get_rect(center=(1440 / 2, 800 / 2)))
            self.__starting_timer -= 1
            return

        self.start_music()

        if self.__starting_timer <= 0 and len(self.__active_notes) == 0 and \
                len(self.__level_data.tile_data) <= self.__line_counter:
            r = asset_loader.medium_font.render("Level Finished, Great Job!", True, (255, 255, 255))
            game.GameWindow.screen.blit(r, r.get_rect(center=game.GameConstants.CENTER))
            if self.__ending_timer <= 0:
                Utils.update_highscore(Utils.encode_string(self.__level_data.song_data.song_name), self.__level_score)
                game.GameWindow.level_running = None
                game.GameWindow.game_state = game.GameStates.LEVEL_BROWSER
            self.__ending_timer -= 1
            return
        if self.__song_progression > self.__time_from_last_call_ms \
                and len(self.__level_data.tile_data) > self.__line_counter:
            self.generate_new_notes()
            self.__time_from_last_call_ms += self.__bpm_in_ms
        self.__song_progression += game.GameWindow.clock.get_time()

    def render(self, surface: pygame.Surface):
        level_score = asset_loader.medium_font.render(f"Score: {self.__level_score}", True, (255, 255, 255))
        surface.blit(level_score, level_score.get_rect(center=(1440 / 2, 100)))
        combo_counter = asset_loader.small_font.render(f"X {game.GameWindow.combo_counter}", True, (204, 190, 234))
        surface.blit(combo_counter, combo_counter.get_rect(center=(1440 / 2, 70)))
        for note in self.__active_notes:
            note.render(surface)
            note.move()

        surface.blit(asset_loader.keys_background, asset_loader.keys_background.get_rect(topleft=(204, 730)))
