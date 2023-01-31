import pygame

import game
from level import Level
from utils import Utils
from utils.level_loader import LevelLoader


class MusicTicket:
    def __init__(self, song_data):
        self.__padding_box = None
        self.__padding_rect = None
        self.__song_id = song_data[0]
        self.__song_artist = song_data[1]

    def tick(self):
        mouse = pygame.mouse
        if self.__padding_rect.collidepoint(
                mouse.get_pos()):
            level_data = LevelLoader().load_level_beatmap(self.__song_id.replace(" ", "_").lower())
            level = Level(level_data, game.keyboard_keys)
            game.GameWindow.level_running = level
            game.GameWindow.game_state = game.GameStates.PLAYING_LEVEL

        # Only hover ------------------
        elif self.__padding_rect.collidepoint(mouse.get_pos()):
            song_title_font = game.medium_font.render(self.__song_id, True, (212, 212, 212))
            self.__padding_box.fill((48, 33, 33))

    def render(self, surface: pygame.Surface,pos: tuple, index: int):
        # Variables ------------------
        high_score = Utils.get_high_score(self.__song_id)
        song_name = f'"{self.__song_id.title()}"'
        song_artist = f"By {self.__song_artist.title()}".strip()

        high_score_font = game.small_font.render(f"Highest Score: {high_score}", True, (255, 255, 255))
        song_title_font = game.medium_font.render(song_name, True, (255, 255, 255))
        song_artist_font = game.small_font.render(song_artist, True, (120, 120, 120))

        GAP = 120

        PADDING = 50
        song_box = pygame.Surface(
            (400, song_title_font.get_height() + song_artist_font.get_height() + PADDING))
        song_box.fill((56, 39, 39))

        self.__padding_box = song_box
        self.__padding_rect = song_box.get_rect(center=(pos[0], pos[1] + GAP * (index + 1)))

        # Blit ------------------
        surface.blit(self.__padding_box, self.__padding_rect)
        surface.blit(high_score_font, high_score_font.get_rect(center=(pos[0], pos[1] + GAP * (index + 1) - 30)))
        surface.blit(song_artist_font, song_artist_font.get_rect(center=(pos[0], pos[1] + GAP * (index + 1) + 30)))
        surface.blit(song_title_font, song_title_font.get_rect(center=(pos[0], pos[1] + GAP * (index + 1))))
