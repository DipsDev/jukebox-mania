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
    pygame.display.set_caption('Jukebox Mania')
    game_state = GameStates.LEVEL_BROWSER
    level_running: Level = None
    game_background: pygame.Surface = None
    combo_counter = 0


class GameConstants:
    COMBO_MULTIPLIER = 0.1
    DEBUG_MODE = False  # Print variables or no
    GAME_FPS = 60
    KEYS_HEIGHT = 695
    TOLERANCE_OFFSET = 78  # Pixel difference tolerance
    HOLDING_OFFSET = 0.33
    TARGET_FPS = 60
    KEYS_RECT_HEIGHT = 705.5


# Game keys
f_key = KeyboardButton("F", (615, GameConstants.KEYS_HEIGHT), pygame.K_f, "green")
d_key = KeyboardButton("D", (395, GameConstants.KEYS_HEIGHT), pygame.K_d, "yellow")
j_key = KeyboardButton("J", (615 + 220 - 4, GameConstants.KEYS_HEIGHT), pygame.K_j, "blue")
k_key = KeyboardButton("K", (615 + 220 * 2 + 9, GameConstants.KEYS_HEIGHT), pygame.K_k, "pink")
keyboard_keys = [f_key, d_key, j_key, k_key]

main_font = pygame.font.Font("./assets/fonts/Peaberry-Doublespace.otf", 32)
small_font = pygame.font.Font("./assets/fonts/Peaberry-Base.otf", 16)

keys_background = pygame.image.load("./assets/keys_background.png")
