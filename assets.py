import pygame

# Definindo os novos tipos
def load_sprites_homeless():
    sprites = []
    spritesheet = [pygame.image.load(f'assets/img/run_homeless/run{i}.png') for i in range(1, 9)]
    for sprite in spritesheet:
        sprites.append(sprite)
    return sprites

def load_sprites_zombies():
    sprites = []
    spritesheet = [pygame.image.load(f'assets/img/run_zombie/runz{i}.png') for i in range(1,8)]
    for sprite in spritesheet:
        sprites.append(sprite)
    return sprites

def load_sprites_bat():
    sprites = []
    spritesheet = [pygame.image.load(f'assets/img/flight_bat/voo{i}.png') for i in range(1, 5)]
    for sprite in spritesheet:
        sprites.append(sprite)
    return sprites