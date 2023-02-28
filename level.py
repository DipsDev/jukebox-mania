import pygame.time
from pygame import Surface

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
        self.__is_paused = False

        self.__high_score_announced = False
        self.__high_score_timer = 0

        self.__menu_buttons = []

        self.__keys_bg = asset_loader.keys_background.convert()

    def get_level_data(self):
        return self.__level_data

    def start(self):
        game.GameWindow.game_background.blit(asset_loader.background_img.convert(), (0, 0))
        game.GameWindow.level_running = self
        game.GameWindow.combo_counter = 0
        song_name = asset_loader.medium_bold_font.render(
            f"Currently Playing: {self.__level_data.song_data.song_name.title()}",
            True,
            (229, 161, 89))
        game.GameWindow.game_background.blit(song_name, (1440 / 2 - song_name.get_width() / 2, 130))

    def button_tick(self):
        mouse = pygame.mouse
        for name, rect in self.__menu_buttons:
            if rect.collidepoint(
                    mouse.get_pos()):
                game.CLICK_SOUND.set_volume(game.fx_volume / 100)
                game.CLICK_SOUND.play()
                if name == 'restart level':
                    game.GameWindow.game_state = game.GameStates.RESTARTING_LEVEL
                elif name == "main menu":
                    game.GameWindow.game_state = game.GameStates.MAIN_MENU

    def pause(self):
        self.__is_paused = not self.__is_paused
        if self.__is_paused:
            pygame.mixer.music.pause()
        else:
            self.__starting_timer = 300

    def start_music(self):
        if not game.GameConstants.DEBUG_MODE and not self.__music_started:
            pygame.mixer.music.set_volume(game.music_volume / 10)
            pygame.mixer.music.play()
            self.__time_from_last_call_ms = pygame.mixer.music.get_pos() + self.__bpm_in_ms
            self.__music_started = True
        else:
            pygame.mixer.music.unpause()

    def add_user_score(self, score: float):
        if score > 0:
            game.GameWindow.combo_counter += 1
            self.__level_score += round(score * (game.GameWindow.combo_counter * game.GameConstants.COMBO_MULTIPLIER))
        else:
            self.__level_score += score
            game.GameWindow.combo_counter = 0
        self.__level_score = max(self.__level_score, 0)
        song_id = Utils.encode_string(self.__level_data.song_data.song_name)
        database_score = Utils.get_high_score(song_id)
        if not self.__high_score_announced and database_score and self.__level_score > database_score:
            self.__high_score_announced = True
            self.__high_score_timer = 200

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

    def __render_menu(self, surface):
        bg_black_alpha = Surface(game.GameConstants.DIMENSIONS)
        bg_black_alpha.set_alpha(200)
        surface.blit(bg_black_alpha, (0, 0))

        level_paused_announcement = asset_loader.announcement_font.render("Level Paused", True,
                                                                          (255, 255, 255))
        esc_to_resume = asset_loader.small_font.render("ESC to resume", True, (111, 111, 111))

        main_menu_button = asset_loader.medium_font.render("Main Menu", True, (255, 255, 255))
        restart_button = asset_loader.medium_font.render("Restart Level", True, (255, 255, 255))
        self.__menu_buttons.append(("main menu", main_menu_button.get_rect(center=(game.GameConstants.CENTER[0], 300))))
        self.__menu_buttons.append(("restart level", restart_button.get_rect(center=(game.GameConstants.CENTER[0], 350))))

        surface.blit(level_paused_announcement,
                     level_paused_announcement.get_rect(center=(game.GameConstants.CENTER[0], 250)))
        surface.blit(main_menu_button, main_menu_button.get_rect(center=(game.GameConstants.CENTER[0], 300)))
        surface.blit(restart_button, restart_button.get_rect(center=(game.GameConstants.CENTER[0], 350)))
        surface.blit(esc_to_resume, esc_to_resume.get_rect(center=(game.GameConstants.CENTER[0], 400)))

    def tick(self):
        if self.__is_paused:
            return

        if self.__starting_timer >= 0:
            r = asset_loader.medium_font.render(f"Starting in {self.__starting_timer // 100 + 1}", True,
                                                (255, 255, 255))
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
        if self.__high_score_timer > 0:
            new_high_score_announcment = asset_loader.announcement_font.render("New Highscore!", True, (255, 255, 255))
            surface.blit(new_high_score_announcment,
                         new_high_score_announcment.get_rect(center=(game.GameConstants.CENTER[0], 205)))
            self.__high_score_timer -= 1

        for note in self.__active_notes:
            note.render(surface)
            if not self.__is_paused and self.__starting_timer <= 0:
                note.move()

        surface.blit(self.__keys_bg, self.__keys_bg.get_rect(topleft=(204, 730)))

        if self.__is_paused:
            self.__render_menu(surface)
