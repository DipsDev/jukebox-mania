import pygame

from components.KeyboardButton import KeyboardButton


class GameWindow:
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1440, 800))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Jukebox Hero')


class GameSettings:
    debug_mode = True  # Print variables or no
    game_fps = 60
    keys_height = 650
    offset = 5  # Pixel difference tolerance


f_key = KeyboardButton("F", (1440 / 2 - 45, GameSettings.keys_height), pygame.K_f)
d_key = KeyboardButton("D", (1440 / 2 - 90 - 45, GameSettings.keys_height), pygame.K_d)
j_key = KeyboardButton("J", (1440 / 2 + 45, GameSettings.keys_height), pygame.K_j)
k_key = KeyboardButton("K", (1440 / 2 + 90 + 45, GameSettings.keys_height), pygame.K_k)
keyboard_keys = [f_key, d_key, j_key, k_key]
