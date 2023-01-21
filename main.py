import pygame

import game
from Scenes.LevelBrowser import LevelBrowser
from Scenes.PlayScene import PlayScene
from utils.LevelLoader import LevelLoader
from game import GameWindow
from Level import Level


def main():
    # Fill background
    game.GameWindow.game_background = pygame.Surface(GameWindow.screen.get_size()).convert()
    game.GameWindow.game_background.fill((255, 255, 255))

    level_loaded = None
    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        GameWindow.screen.blit(game.GameWindow.game_background, (0, 0))
        if game.GameWindow.game_state == game.GameStates.LEVEL_BROWSER:
            LevelBrowser().render(game.GameWindow.screen)
        elif game.GameWindow.game_state == game.GameStates.PLAYING_LEVEL:
            if not level_loaded:
                level_loaded = PlayScene(game.GameWindow.level_running)
            else:
                level_loaded.play(game.GameWindow.screen)
        pygame.display.flip()
        GameWindow.clock.tick(game.GameConstants.GAME_FPS)


if __name__ == '__main__':
    main()
