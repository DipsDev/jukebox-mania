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



    # Levels
    level1_data = LevelLoader().load_level_beatmap("gamor_and_manoi")
    level1 = Level(level1_data, game.keyboard_keys)
    play = PlayScene(level1)

    GameWindow.screen.blit(game.GameWindow.game_background, (0, 0))
    pygame.display.flip()

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        GameWindow.screen.blit(game.GameWindow.game_background, (0, 0))
        if game.GameWindow.game_state == game.GameStates.LEVEL_BROWSER:
            LevelBrowser().render(game.GameWindow.screen)
        elif game.GameWindow.game_state == game.GameStates.PLAYING_LEVEL:
            play.play(game.GameWindow.screen)
        pygame.display.flip()
        GameWindow.clock.tick(game.GameSettings.game_fps)


if __name__ == '__main__':
    main()
