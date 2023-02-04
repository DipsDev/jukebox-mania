import pygame

import game
from assets import asset_loader
from components.long_note import LongNote
from components.note import Note


# States
# 0 -> click each key
# 1 -> press on the note
# 2 -> hold press for long tiles

class GameTutorial:
    def __init__(self):
        self.__tutorial_state = 0
        self.__clicked_keys = []
        self.__active_notes = pygame.sprite.Group()
        self.__waiting_timer = 300
        self.__notes_sent = [False, False]

    def is_finished(self):
        return self.__tutorial_state >= 3

    def finish(self):
        self.__tutorial_state = 3

    def load(self):
        game.GameWindow.game_background.blit(asset_loader.background_img, (0, 0))
        text_top = asset_loader.medium_font.render(
            f"Learning the basics",
            True,
            (229, 161, 89))
        game.GameWindow.game_background.blit(text_top, (1440 / 2 - text_top.get_width() / 2, 130))

        return self

    def render(self, surface: pygame.Surface):
        if self.__tutorial_state == 0:
            press_keys = asset_loader.medium_font.render(
                f"Press each of the keyboard keys, {4 - len(self.__clicked_keys)} remaining.",
                True,
                (255, 255, 255)
            )
            surface.blit(press_keys, press_keys.get_rect(center=game.GameConstants.CENTER))
            for keyboard_key in game.keyboard_keys:
                if keyboard_key.is_clicked() and keyboard_key not in self.__clicked_keys:
                    self.__clicked_keys.append(keyboard_key)
            if len(self.__clicked_keys) == 4:
                self.__tutorial_state += 1
        elif self.__tutorial_state == 1:
            if len(self.__active_notes.sprites()) != 0:
                catch_note = asset_loader.medium_font.render(
                    f"Note is coming! catch it in the right time using its designated key.",
                    True,
                    (255, 255, 255)
                )
                surface.blit(catch_note, catch_note.get_rect(center=game.GameConstants.CENTER))
            elif self.__notes_sent[0]:
                catch_note = asset_loader.medium_font.render(
                    f"Great job! let's see how you deal with long notes.",
                    True,
                    (255, 255, 255)
                )
                surface.blit(catch_note, catch_note.get_rect(center=game.GameConstants.CENTER))
                if self.__waiting_timer <= 0:
                    self.__tutorial_state = 2
                    self.__waiting_timer = 230
                self.__waiting_timer -= 1

            if not self.__notes_sent[0]:
                self.__active_notes.add(Note((615, -500), 2, game.f_key))
                self.__notes_sent[0] = True
        elif self.__tutorial_state == 2:
            if len(self.__active_notes.sprites()) != 0:
                catch_note = asset_loader.medium_font.render(
                    f"Long press to active a long note.",
                    True,
                    (255, 255, 255)
                )
                surface.blit(catch_note, catch_note.get_rect(center=game.GameConstants.CENTER))
            else:
                catch_note = asset_loader.medium_font.render(
                    f"Awesome! You are now ready to deal with a real level.",
                    True,
                    (255, 255, 255)
                )
                surface.blit(catch_note, catch_note.get_rect(center=game.GameConstants.CENTER))
                if self.__waiting_timer <= 0:
                    self.__tutorial_state = 3
                    game.GameWindow.game_state = game.GameStates.MAIN_MENU
                self.__waiting_timer -= 1

            if not self.__notes_sent[1]:
                self.__active_notes.add(LongNote((615 + 220 - 4, -500), 4, game.j_key,
                                                 500 * 60 / 1000 *
                                                 4 * 6, 500 * 6))
                self.__notes_sent[1] = True

        for note in self.__active_notes:
            note.render(surface)
            note.move()

        for keyboard_key in game.keyboard_keys:
            keyboard_key.click_tick()
            keyboard_key.render(surface)

        surface.blit(asset_loader.keys_background, asset_loader.keys_background.get_rect(topleft=(204, 734)))
