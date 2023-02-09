import pygame

import game
from level import Level
from utils import Utils
from assets import asset_loader
from utils.level_loader import LevelLoader


class MusicTicket:
    def __init__(self, song_data):
        self.__padding_rect = None
        self.__song_id = song_data[0]
        self.__song_artist = song_data[1]
        self.__song_difficulty = song_data[2]

    def tick(self):
        mouse = pygame.mouse
        if self.__padding_rect.collidepoint(
                mouse.get_pos()):
            level_data = LevelLoader().load_level_beatmap(self.__song_id.replace(" ", "_").lower())
            level = Level(level_data, game.KEYBOARD_KEYS)
            game.GameWindow.level_running = level
            game.GameWindow.game_state = game.GameStates.PLAYING_LEVEL

        # Only hover ------------------
        elif self.__padding_rect.collidepoint(mouse.get_pos()):
            pass
            # TODO: Add something

    def render(self, surface: pygame.Surface, index: int):
        # Variables ------------------
        GAP = 340
        base_pos = (385, 305)

        high_score = Utils.get_high_score(self.__song_id)
        song_name = f'"{self.__song_id.title()}"'
        song_artist = f"By {self.__song_artist.title()}".strip()
        song_difficulty = f"{self.__song_difficulty}"

        high_score_font = asset_loader.small_font.render(f"Highest Score: {high_score}", True, (120, 120, 120))
        song_title_font = asset_loader.medium_font.render(song_name, True, (255, 255, 255))
        song_artist_font = asset_loader.small_font.render(song_artist, True, (140, 140, 140))
        song_difficulty_font = asset_loader.small_font.render(song_difficulty, True, (71, 35, 64))

        offset = GAP * index

        rect_box = pygame.Surface((277, 135))
        self.__padding_rect = rect_box.get_rect(center=(base_pos[0] + offset - 4, base_pos[1] - 6))

        # Blit ------------------
        surface.blit(song_difficulty_font,
                     song_difficulty_font.get_rect(center=(base_pos[0] + offset, base_pos[1] - 55)))
        surface.blit(high_score_font, high_score_font.get_rect(center=(base_pos[0] + offset, base_pos[1] - 30)))
        surface.blit(song_artist_font, song_artist_font.get_rect(center=(base_pos[0] + offset, base_pos[1] + 30)))
        surface.blit(song_title_font, song_title_font.get_rect(center=(base_pos[0] + offset, base_pos[1])))
