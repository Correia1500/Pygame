import pygame
from assets import *
from os import path
import os

# Definindo os novos tipos
def load_sprites_homeless_right():
    sprites = []
    spritesheet = [pygame.image.load(f'assets/img/run_homeless/run_right/run{i}.png') for i in range(1, 9)]
    for sprite in spritesheet:
        sprites.append(sprite)
    return sprites

def load_sprites_homeless_left():
    sprites = []
    spritesheet = [pygame.image.load(f'assets/img/run_homeless/run_left/run{i}.png') for i in range(1, 9)]
    for sprite in spritesheet:
        sprites.append(sprite)
    return sprites

def load_sprites_homeless_jump():
    sprites = []
    spritesheet = [pygame.image.load(f'assets/img/jump_homeless/jump{i}.png') for i in range(1, 9)]
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
