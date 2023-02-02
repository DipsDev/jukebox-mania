import pygame

import game
from components.music_ticket import MusicTicket
from assets import asset_loader
from utils.level_loader import LevelLoader


class LevelBrowser:
    def __init__(self):
        self.__av_levels = LevelLoader().get_available_levels()
        self.__music_tickets = []
        self.__back_button_rect = None
        game.GameWindow.level_running = None
        self.__loaded = False
        pygame.mixer.music.stop()

    def load(self):
        if self.__loaded:
            return

        # Background importing --------------------------
        background_img = pygame.image.load("./assets/level_browser_bg.png").convert()
        background_img = pygame.transform.scale(background_img, game.GameConstants.DIMENSIONS)

        # Text and UI --------------------------
        level_browser = asset_loader.main_font.render("Song Browser", True, (255, 255, 255))
        background_img.blit(level_browser, level_browser.get_rect(center=(1440 / 2, 50)))

        # Blit to the screen --------------------------
        game.GameWindow.game_background.blit(background_img, (0, 0))
        game.GameWindow.combo_counter = 0
        return self

    def render(self, surface: pygame.Surface):
        pos = (game.GameConstants.DIMENSIONS[0] / 2, 100)

        back_button = asset_loader.small_font.render("Back", True, (255, 255, 255))
        self.__back_button_rect = back_button.get_rect(center=(1440 - 120, 780))
        game.GameWindow.screen.blit(back_button, self.__back_button_rect)
        for index, level_name in enumerate(self.__av_levels):
            ticket = MusicTicket(level_name)
            self.__music_tickets.append(ticket)
            ticket.render(surface, pos, index)

    def button_tick(self):
        mouse = pygame.mouse
        if self.__back_button_rect.collidepoint(mouse.get_pos()):
            game.GameWindow.game_state = game.GameStates.MAIN_MENU
        for ticket in self.__music_tickets:
            ticket.tick()
