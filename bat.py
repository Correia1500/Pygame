import pygame
import random
from assets import *
from bullet import Bullet
from assets import load_sprites_bat
from config import *

class Bat(pygame.sprite.Sprite):
    def __init__(self):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)
        self.sprites = load_sprites_bat()
        self.current_sprite = 0
        self.animation_counter = 0

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(5,10)
        self.rect.y = random.randint(50,HEIGHT // 6) #velocidade vertical variável
        self.speedx = random.randint(5, 10)
        self.speedy = random.randint(-2, 2)
    def update(self):

        self.animation_counter += 1
        if self.animation_counter >= 5:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]
            self.animation_counter = 0

        # Atualiza a posição do bat
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Se o bar passar do final da tela,  volta para a esquerda e sorteia uma nova posição
        
        if self.rect.left > WIDTH:
            self.rect.right = 0
            self.rect.y = random.randint(100, 400)
            self.speedx = random.randint(5, 10)
            self.speedy = random.randint(-2, 2)
            
        # Mantém o morcego dentro dos limites verticais
        if self.rect.top < 0 or self.rect.bottom > HEIGHT // 8:
            self.speedy = -self.speedy