import pygame

import game
from Level import Level
from utils.LevelLoader import LevelLoader


def render(surface: pygame.Surface, level_data: tuple, pos: tuple, index: int):
    # Variables ------------------
    mouse = pygame.mouse
    song_name = f'"{level_data[0].title()}"'
    song_artist = f"By {level_data[1].title()}".strip()
    song_title_font = game.main_font.render(song_name, True, (255, 255, 255))
    song_artist_font = game.small_font.render(song_artist, True, (120, 120, 120))

    GAP = 110

    PADDING = 50
    song_box = pygame.Surface(
        (400, song_title_font.get_height() + song_artist_font.get_height() + PADDING))
    song_box.fill((56, 39, 39))

    # Click and hover ------------------
    if mouse.get_pressed()[0] and song_box.get_rect(center=(pos[0], pos[1] + GAP * (index + 1))).collidepoint(
            mouse.get_pos()):
        level_data = LevelLoader().load_level_beatmap(level_data[0].replace(" ", "_"))
        level = Level(level_data, game.keyboard_keys)
        game.GameWindow.level_running = level
        game.GameWindow.game_state = game.GameStates.PLAYING_LEVEL

    # Only hover ------------------
    elif song_box.get_rect(center=(pos[0], pos[1] + GAP * (index + 1))).collidepoint(mouse.get_pos()):
        song_title_font = game.main_font.render(song_name, True, (212, 212, 212))

    # Blit ------------------
    surface.blit(song_box, song_box.get_rect(center=(pos[0], pos[1] + GAP * (index + 1))))
    surface.blit(song_artist_font, song_artist_font.get_rect(center=(pos[0], pos[1] + GAP * (index + 1) + 30)))
    surface.blit(song_title_font, song_title_font.get_rect(center=(pos[0], pos[1] + GAP * (index + 1))))
