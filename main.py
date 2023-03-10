import sys

import pygame

import game
from components.animated_bg import AnimatedBg
from level import Level
from scenes.level_browser import LevelBrowser
from scenes.main_menu import MainMenu
from scenes.play_scene import PlayScene
from game import GameWindow
from scenes.settings import Settings
from scenes.tutorial import GameTutorial


def main():
    # Fill background
    game.GameWindow.game_background = pygame.Surface(GameWindow.screen.get_size()).convert()
    game.GameWindow.game_background.fill((255, 255, 255))

    # Screens
    level_loaded = None
    tutorial_loaded = None
    level_browser = None
    main_menu = None
    animated_bg = None

    # Event loop
    while True:
        game_state = game.GameWindow.game_state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.GameWindow.database.save()
                pygame.quit()
                sys.exit(1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == game.GameStates.MAIN_MENU:
                    main_menu.render(game.GameWindow.screen).button_tick()
                elif game_state == game.GameStates.LEVEL_BROWSER:
                    level_browser.button_tick()
                elif game_state == game.GameStates.SETTINGS:
                    Settings().render(game.GameWindow.screen).button_tick()
                elif game_state == game.GameStates.PLAYING_LEVEL:
                    game.GameWindow.level_running.button_tick()
            elif event.type == pygame.KEYDOWN:
                if game_state == game.GameStates.TUTORIAL:
                    if event.key == pygame.K_ESCAPE:
                        game.GameWindow.game_state = game.GameStates.MAIN_MENU
                if game_state == game.GameStates.PLAYING_LEVEL:
                    if level_loaded and event.key == pygame.K_ESCAPE:
                        level_loaded.toggle_pause()

        GameWindow.screen.blit(game.GameWindow.game_background, (0, 0))
        if game_state == game.GameStates.LEVEL_BROWSER:
            animated_bg = None
            if not level_browser:
                level_browser = LevelBrowser().load()
            else:
                level_browser.load().render(game.GameWindow.screen)
                level_loaded = None
        elif game_state == game.GameStates.MAIN_MENU:
            if not animated_bg:
                animated_bg = AnimatedBg()
            animated_bg.render(game.GameWindow.screen)
            tutorial_loaded = None
            if not main_menu:
                main_menu = MainMenu()
            else:
                main_menu.render(game.GameWindow.screen)
        elif game_state == game.GameStates.SETTINGS:
            animated_bg.render(game.GameWindow.screen)
            Settings().render(game.GameWindow.screen)
        elif game_state == game.GameStates.PLAYING_LEVEL:
            if not level_loaded:
                level_loaded = PlayScene(game.GameWindow.level_running)
                level_browser = None
            else:
                level_loaded.play(game.GameWindow.screen)
        elif game_state == game.GameStates.RESTARTING_LEVEL:
            game.GameWindow.game_state = game.GameStates.PLAYING_LEVEL
            new_level = Level(game.GameWindow.level_running.get_level_data(), game.KEYBOARD_KEYS)
            game.GameWindow.level_running = new_level
            level_loaded = PlayScene(new_level)

        elif game_state == game.GameStates.TUTORIAL:
            animated_bg = None
            if not tutorial_loaded or tutorial_loaded.is_finished():
                tutorial_loaded = GameTutorial().load()
            else:
                tutorial_loaded.render(game.GameWindow.screen)

        pygame.display.update()
        GameWindow.clock.tick(game.GameConstants.GAME_FPS)


if __name__ == '__main__':
    main()
