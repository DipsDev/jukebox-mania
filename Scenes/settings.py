import pygame

import game
from assets import asset_loader


class Settings:
    def __init__(self):
        self.__buttons = []

    def button_tick(self):
        mouse = pygame.mouse
        for name, rect in self.__buttons:
            if rect.collidepoint(
                    mouse.get_pos()):
                if name == 'volume_up_music':
                    game.music_volume = min(game.music_volume + 10, 100)
                    game.GameWindow.database.set_data("music_volume", game.music_volume)
                elif name == "volume_down_music":
                    game.music_volume = max(game.music_volume - 10, 0)
                    game.GameWindow.database.set_data("music_volume", game.music_volume)
                elif name == "back":
                    game.GameWindow.game_state = game.GameStates.MAIN_MENU
                elif name == "volume_down_fx":
                    game.fx_volume = max(game.fx_volume - 10, 0)
                    game.GameWindow.database.set_data("fx_volume", game.fx_volume)
                elif name == "volume_up_fx":
                    game.fx_volume = min(game.fx_volume + 10, 100)
                    game.GameWindow.database.set_data("fx_volume", game.fx_volume)

    def render(self, surface: pygame.Surface):
        # Main titles
        settings_title = asset_loader.main_font.render("Settings", True, (0, 0, 0))
        copyright = asset_loader.small_font.render('A Game By Ido Geva', True, (0, 0, 0))

        # Labels
        volume_font = asset_loader.medium_font.render("Music Volume", True, (0, 0, 0))
        volume_progress_num = game.music_volume * 10 * (volume_font.get_width() / 1000)
        volume_progress = pygame.Surface((volume_progress_num, 15))

        fx_font = asset_loader.medium_font.render("FX Volume", True, (0, 0, 0))
        fx_progress_num = game.fx_volume * 10 * (volume_font.get_width()) / 1000
        fx_progress = pygame.Surface((fx_progress_num, 15))

        # Buttons
        volume_up = asset_loader.small_font.render("Volume Up", True, (0, 0, 0))
        volume_down = asset_loader.small_font.render("Volume Down", True, (0, 0, 0))
        back_button = asset_loader.small_font.render("Back", True, (0, 0, 0))

        fx_up = asset_loader.small_font.render("Volume Up", True, (0, 0, 0))
        fx_down = asset_loader.small_font.render("Volume Down", True, (0, 0, 0))

        self.__buttons.append(
            ("volume_up_music", volume_up.get_rect(center=(game.GameConstants.CENTER[0] + 170, 200 - 12))))
        self.__buttons.append(
            ("volume_down_music", volume_down.get_rect(center=(game.GameConstants.CENTER[0] - 170, 200 - 12))))

        self.__buttons.append(
            ("volume_up_fx", fx_up.get_rect(center=(game.GameConstants.CENTER[0] + 170, 300 - 12))))
        self.__buttons.append(
            ("volume_down_fx", fx_down.get_rect(center=(game.GameConstants.CENTER[0] - 170, 300 - 12))))

        self.__buttons.append(("back", back_button.get_rect(center=(1440 - 120, 780))))

        surface.blit(volume_up, self.__buttons[0][1])
        surface.blit(volume_down, self.__buttons[1][1])
        surface.blit(fx_up, self.__buttons[2][1])
        surface.blit(fx_down, self.__buttons[3][1])
        surface.blit(back_button, self.__buttons[-1][1])

        surface.blit(fx_progress, fx_progress.get_rect(bottomleft=(game.GameConstants.CENTER[0] - 89, 300)))
        surface.blit(fx_font, fx_font.get_rect(center=(game.GameConstants.CENTER[0], 250)))

        surface.blit(volume_progress, volume_progress.get_rect(bottomleft=(game.GameConstants.CENTER[0] - 89, 200)))
        surface.blit(volume_font, volume_font.get_rect(center=(game.GameConstants.CENTER[0], 150)))
        surface.blit(settings_title, settings_title.get_rect(center=(game.GameConstants.CENTER[0], 50)))
        surface.blit(copyright, copyright.get_rect(center=(120, 780)))

        return self
