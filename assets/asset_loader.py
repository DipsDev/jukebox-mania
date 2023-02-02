import pygame

pygame.mixer.init()
pygame.font.init()

background_img = pygame.image.load("./assets/background.png")


# Fonts
main_font = pygame.font.Font("./assets/fonts/Silver.ttf", 50)
medium_font = pygame.font.Font("./assets/fonts/m5x7.ttf", 40)
small_font = pygame.font.Font("./assets/fonts/m5x7.ttf", 30)

# Sounds
HIT_SOUND = pygame.mixer.Sound('./assets/sounds/hitsound.wav')

keys_background = pygame.image.load("./assets/keys_background.png")
