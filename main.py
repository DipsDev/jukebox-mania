import pygame

import game
from Scenes.LevelBrowser import LevelBrowser
from Scenes.PlayScene import PlayScene
from utils.LevelLoader import LevelLoader
from game import GameWindow
from Level import Level


def main():
    # Fill background
    background = pygame.Surface(GameWindow.screen.get_size())
    background = background.convert()
    background_img = pygame.image.load("./assets/background.png")
    background.blit(background_img, (0, 0))

    GameWindow.screen.blit(background, (0, 0))
    pygame.display.flip()

    # Levels
    level1_data = LevelLoader().load_level_beatmap("gamor_and_manoi")
    level1 = Level(level1_data, game.keyboard_keys)
    play = PlayScene(level1)

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        GameWindow.screen.blit(background, (0, 0))
        if game.GameWindow.game_state == game.GameStates.LEVEL_BROWSER:
            LevelBrowser().render(game.GameWindow.screen)
        if game.GameWindow.game_state == game.GameStates.PLAYING_LEVEL:
            play.play(game.GameWindow.screen)
        pygame.display.flip()
        GameWindow.clock.tick(game.GameSettings.game_fps)


if __name__ == '__main__':
    main()
