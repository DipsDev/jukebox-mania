from enum import Enum

import pygame

from Level import Level
from components.KeyboardButton import KeyboardButton


class GameStates(str, Enum):
    PLAYING_LEVEL = "playing_lvl"
    LEVEL_BROWSER = "browsing_levels"
    MAIN_MENU = "main_menu"


class GameWindow:
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1440, 800))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Jukebox Hero')
    game_state = GameStates.PLAYING_LEVEL
    level_running: Level = None
    game_background: pygame.Surface = None


class GameSettings:
    debug_mode = True  # Print variables or no
    game_fps = 60
    keys_height = 695
    offset = 50  # Pixel difference tolerance
    holding_offset = 0.33


# Game keys
f_key = KeyboardButton("F", (615, GameSettings.keys_height), pygame.K_f, "yellow")
d_key = KeyboardButton("D", (395, GameSettings.keys_height), pygame.K_d, "green")
j_key = KeyboardButton("J", (615 + 220 - 4, GameSettings.keys_height), pygame.K_j, "blue")
k_key = KeyboardButton("K", (615 + 220 * 2 + 9, GameSettings.keys_height), pygame.K_k, "pink")
keyboard_keys = [f_key, d_key, j_key, k_key]


main_font = pygame.font.Font("./assets/fonts/Peaberry-Base.otf",32)
