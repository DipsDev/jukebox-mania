import pygame

import game
from scenes.level_browser import LevelBrowser
from scenes.main_menu import MainMenu
from scenes.play_scene import PlayScene
from game import GameWindow


def main():
    # Fill background
    game.GameWindow.game_background = pygame.Surface(GameWindow.screen.get_size()).convert()
    game.GameWindow.game_background.fill((255, 255, 255))

    # Screens
    level_loaded = None
    level_browser = None

    # Event loop
    while True:
        game_state = game.GameWindow.game_state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.GameWindow.database.save()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == game.GameStates.MAIN_MENU:
                    MainMenu().render(game.GameWindow.screen).button_tick()
                elif game_state == game.GameStates.LEVEL_BROWSER:
                    level_browser.button_tick()

        GameWindow.screen.blit(game.GameWindow.game_background, (0, 0))
        if game_state == game.GameStates.LEVEL_BROWSER:
            if not level_browser:
                level_browser = LevelBrowser().load()
            else:
                level_browser.render(game.GameWindow.screen)
                level_loaded = None
        elif game_state == game.GameStates.MAIN_MENU:
            MainMenu().render(game.GameWindow.screen)
        elif game_state == game.GameStates.PLAYING_LEVEL:
            if not level_loaded:
                level_loaded = PlayScene(game.GameWindow.level_running)
            else:
                level_loaded.play(game.GameWindow.screen)
                level_browser = None

        pygame.display.update()
        GameWindow.clock.tick(game.GameConstants.GAME_FPS)


if __name__ == '__main__':
    main()
