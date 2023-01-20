import pygame

import game
from Scenes.PlayScene import PlayScene
from utils.LevelLoader import LevelLoader
from game import GameWindow
from Level import Level


def main():
    # Fill background
    background = pygame.Surface(GameWindow.screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    GameWindow.screen.blit(background, (0, 0))
    pygame.display.flip()

    # Levels
    level1_data = LevelLoader().load_level_beatmap("level_1")
    level1 = Level(level1_data, game.keyboard_keys)
    play = PlayScene(level1)

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        GameWindow.screen.blit(background, (0, 0))
        play.play(GameWindow.screen)
        pygame.display.flip()
        GameWindow.clock.tick(game.GameSettings.game_fps)


if __name__ == '__main__':
    main()
