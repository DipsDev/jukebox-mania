from enum import Enum

import pygame

from database.database import Database
from level import Level
from components.keyboard_button import KeyboardButton


class GameStates(str, Enum):
    PLAYING_LEVEL = "playing_lvl"
    LEVEL_BROWSER = "browsing_levels"
    MAIN_MENU = "main_menu"


class GameConstants:
    COMBO_MULTIPLIER = 0.1
    DEBUG_MODE = False  # Print variables or no
    GAME_FPS = 60
    KEYS_HEIGHT = 695
    TOLERANCE_OFFSET = 78  # Pixel difference tolerance
    HOLDING_OFFSET = 0.33
    TARGET_FPS = 60
    KEYS_RECT_HEIGHT = 705.5
    DIMENSIONS = (1440, 800)
    CENTER = (DIMENSIONS[0] / 2, DIMENSIONS[1] / 2)


class GameWindow:
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    screen = pygame.display.set_mode((GameConstants.DIMENSIONS[0], GameConstants.DIMENSIONS[1]))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Jukebox Mania')
    game_state = GameStates.MAIN_MENU
    level_running: Level = None
    game_background: pygame.Surface = None
    combo_counter = 0
    database = Database().load()


# Game keys
f_key = KeyboardButton("F", (615, GameConstants.KEYS_HEIGHT), pygame.K_f, "green")
d_key = KeyboardButton("D", (395, GameConstants.KEYS_HEIGHT), pygame.K_d, "yellow")
j_key = KeyboardButton("J", (615 + 220 - 4, GameConstants.KEYS_HEIGHT), pygame.K_j, "blue")
k_key = KeyboardButton("K", (615 + 220 * 2 + 9, GameConstants.KEYS_HEIGHT), pygame.K_k, "pink")
keyboard_keys = [f_key, d_key, j_key, k_key]

main_font = pygame.font.Font("./assets/fonts/m6x11.ttf", 32)
small_font = pygame.font.Font("./assets/fonts/m5x7.ttf", 16)

keys_background = pygame.image.load("./assets/keys_background.png")
