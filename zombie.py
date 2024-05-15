import pygame
import random
from bullet import Bullet
from assets import load_sprites_homeless
from config import *

class Zombie(pygame.sprite.Sprite):
    def __init__(self,img):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - ZOMBIE_WIDTH)
        #self.rect.y = random.randint(-100, -ZOMBIE_HEIGHT)
        self.speedx = random.randint(3, 10)
        #self.rect.x = WIDTH
        #
        self.rect.y = HEIGHT - 150
        #self.speedx = -10

    def update(self):
        # Atualiza a posição do zombie
        self.rect.x += self.speedx
        # Se o zombie passar do final da tela, volta para cima e sorteia uma nova posição
        # novas posições e velocidades
        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.rect.x = random.randint(0, WIDTH - ZOMBIE_WIDTH)
            self.speedx = random.randint(-3, -10)