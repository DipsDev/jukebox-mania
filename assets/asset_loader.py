import pygame

pygame.mixer.init()
pygame.font.init()

background_img = pygame.image.load("./assets/background.png")
level_browser_bg = pygame.image.load("./assets/level_browser_bg.png")

# Fonts
main_font = pygame.font.Font("./assets/fonts/NicoClean-Regular.ttf", 40)
bold_font = pygame.font.Font("./assets/fonts/NicoBold-Regular.ttf", 30)
medium_bold_font = pygame.font.Font("./assets/fonts/NicoBold-Regular.ttf", 20)
medium_font = pygame.font.Font("./assets/fonts/NicoClean-Regular.ttf", 20)
small_font = pygame.font.Font("./assets/fonts/NicoClean-Regular.ttf", 15)
announcment_font = pygame.font.Font("./assets/fonts/NicoBold-Regular.ttf", 20)

# Sounds
HIT_SOUND = pygame.mixer.Sound('./assets/sounds/hitsound.wav')
CLICK_SOUND = pygame.mixer.Sound("./assets/sounds/clicksound.wav")

keys_background = pygame.image.load("./assets/keys_background.png")
