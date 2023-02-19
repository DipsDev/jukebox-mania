import pygame

import game
from assets import asset_loader
from assets.asset_loader import CLICK_SOUND


class Settings:
    def __init__(self):
        self.__buttons = []

    def button_tick(self):
        mouse = pygame.mouse
        for name, rect in self.__buttons:
            if rect.collidepoint(
                    mouse.get_pos()):
                print(game.music_volume)
                if name == 'volume_up_music':
                    game.music_volume = min(game.music_volume + 10, 100)
                    CLICK_SOUND.set_volume(game.music_volume / 100)
                    CLICK_SOUND.play()
                elif name == "volume_down_music":
                    game.music_volume = max(game.music_volume - 10, 0)
                    CLICK_SOUND.set_volume(game.music_volume / 100)
                    CLICK_SOUND.play()
                elif name == "back":
                    game.GameWindow.game_state = game.GameStates.MAIN_MENU
                elif name == "volume_down_fx":
                    game.fx_volume = max(game.fx_volume - 10, 0)
                    CLICK_SOUND.set_volume(game.fx_volume / 100)
                    CLICK_SOUND.play()
                elif name == "volume_up_fx":
                    game.fx_volume = min(game.fx_volume + 10, 100)
                    CLICK_SOUND.set_volume(game.fx_volume / 100)
                    CLICK_SOUND.play()

    def render(self, surface: pygame.Surface):
        text_color = (255, 255, 255)

        # Main titles
        settings_title = asset_loader.bold_font.render("Settings", True, text_color)
        copyright_text = asset_loader.small_font.render('A Game By Ido Geva', True, text_color)

        # Labels
        volume_font = asset_loader.medium_font.render("Music Volume", True, text_color)
        volume_progress_num = game.music_volume * 10 * (volume_font.get_width() / 1000)
        volume_progress = pygame.Surface((volume_progress_num, 15))
        volume_progress.fill(text_color)

        fx_font = asset_loader.medium_font.render("FX Volume", True, text_color)
        fx_progress_num = game.fx_volume * 10 * (volume_font.get_width()) / 1000
        fx_progress = pygame.Surface((fx_progress_num, 15))
        fx_progress.fill(text_color)

        # Buttons
        volume_up = asset_loader.small_font.render("Volume Up", True, text_color)
        volume_down = asset_loader.small_font.render("Volume Down", True, text_color)
        back_button = asset_loader.small_font.render("Back", True, text_color)

        fx_up = asset_loader.small_font.render("Volume Up", True, text_color)
        fx_down = asset_loader.small_font.render("Volume Down", True, text_color)

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
        surface.blit(copyright_text, copyright_text.get_rect(center=(120, 780)))

        return self
