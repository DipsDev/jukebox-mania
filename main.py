import pygame

import game
from scenes.level_browser import LevelBrowser
from scenes.play_scene import PlayScene
from game import GameWindow


def main():
    # Fill background
    game.GameWindow.game_background = pygame.Surface(GameWindow.screen.get_size()).convert()
    game.GameWindow.game_background.fill((255, 255, 255))

    level_loaded = None
    level_browser = None

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.GameWindow.database.save()
                return

        GameWindow.screen.blit(game.GameWindow.game_background, (0, 0))
        if game.GameWindow.game_state == game.GameStates.LEVEL_BROWSER:
            if not level_browser:
                level_browser = LevelBrowser().load()
            else:
                level_browser.render(game.GameWindow.screen)
        elif game.GameWindow.game_state == game.GameStates.PLAYING_LEVEL:
            if not level_loaded:
                level_loaded = PlayScene(game.GameWindow.level_running)
            else:
                level_loaded.play(game.GameWindow.screen)
                level_browser = None
        pygame.display.update()
        GameWindow.clock.tick(game.GameConstants.GAME_FPS)


if __name__ == '__main__':
    main()
