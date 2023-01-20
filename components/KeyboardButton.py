import pygame

import game


class KeyboardButton(pygame.sprite.Sprite):

    def __init__(self, name: str, pos: tuple, key_constant):
        super().__init__()
        self.__name = name
        self.__pos = pos
        self.__holding_time = 0
        self.__key_constant = key_constant
        self.__normal = pygame.image.load(f"./assets/keys/{name}/normal.png").convert_alpha()
        self.__anim_2 = pygame.image.load(f"./assets/keys/{name}/clicked.png").convert_alpha()
        self.__sprite = self.__normal
        self.init_images()

    def get_pos(self):
        return self.__pos

    def get_dimensions(self):
        return self.__normal.get_width(), self.__normal.get_height()

    def get_rect(self):
        return self.__sprite.get_rect(center=self.__pos)

    def init_images(self):
        scale_constant = 4
        self.__normal = pygame.transform.scale(self.__normal,
                                               (self.__normal.get_width() * scale_constant,
                                                self.__normal.get_height() * scale_constant))
        self.__anim_2 = pygame.transform.scale(self.__anim_2,
                                               (self.__anim_2.get_width() * scale_constant,
                                                self.__anim_2.get_height() * scale_constant))

    def is_clicked(self):
        return 0 < self.__holding_time / 60 < 0.3

    def is_held(self):
        return 0 < self.__holding_time / 60

    def get_holding_time(self):
        return self.__holding_time / 60

    def click_tick(self):
        keys = pygame.key.get_pressed()
        if not keys[self.__key_constant]:
            self.__sprite = self.__normal
            if self.__holding_time > 0:
                if game.GameSettings.debug_mode:
                    print(f"{self.__name} was pressed for {self.__holding_time / 60} seconds")
                self.__holding_time = 0
            return
        self.__sprite = self.__anim_2
        self.__holding_time += 1

    def render(self, surface: pygame.Surface):
        surface.blit(self.__sprite, self.__sprite.get_rect(center=self.__pos))
