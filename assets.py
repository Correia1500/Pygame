import pygame

# Definindo os novos tipos
def load_sprites_homeless():

    spritesheet = pygame.image.load("assets/img/run.png").convert_alpha()
    sprite_width,sprite_height = spritesheet.get_width() // 8, spritesheet.get_height()
    #sprite_height = 50

    spritesheet = pygame.image.load("assets/img/run_homeless.png").convert_alpha()
    sprite_width, sprite_height= spritesheet.get_width() // 8, spritesheet.get_height()

    sprites = []
    for i in range(8):
        # Calcula a posição x do sprite na spritesheet
        x = i * sprite_width
        sprite = spritesheet.subsurface(pygame.Rect(x, 0, sprite_width, sprite_height))
        sprites.append(sprite)
    return sprites

def load_sprites_zombies():
    spritesheet = pygame.image.load("assets/img/run_zombie.png").convert_alpha()
    sprite_width, sprite_height= spritesheet.get_width() // 7, spritesheet.get_height()

    sprites = []
    for i in range(7):
        # Calcula a posição x do sprite na spritesheet
        x = i * sprite_width
        sprite = spritesheet.subsurface(pygame.Rect(x, 0, sprite_width, sprite_height))
        sprites.append(sprite)
    return sprites