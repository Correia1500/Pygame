import pygame
import random
from assets import *
from bullet import Bullet
from assets import load_sprites_homeless
from config import *

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)
        self.sprites = load_sprites_zombies()
        self.current_sprite = 0
        self.animation_counter = 0

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()

        self.rect.x = (0)
        self.rect.y = HEIGHT - 195
        
        self.speedx = random.randint(3, 8)
        self.on_ground = False
        self.speedy = 0

    def update(self):

        self.animation_counter += 1
        if self.animation_counter >= 5:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]
            self.animation_counter = 0

        # Atualiza a posição do zombie
        self.rect.x += self.speedx
        # Se o zombie passar do final da tela, volta para cima e sorteia uma nova posição
        # novas posições e velocidades

        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.rect.x = random.randint(0, WIDTH - ZOMBIE_WIDTH)
            self.speedx = random.randint(3, 8)

        if not self.on_ground:
            self.speedy += 1
        self.rect.y += self.speedy

        if self.rect.bottom >= HEIGHT - 100:
            self.rect.bottom = HEIGHT - 100
            self.on_ground = True
            self.speedy = 0