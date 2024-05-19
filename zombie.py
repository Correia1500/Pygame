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
        
        # Variáveis para controle de salto
        self.jump_time = random.randint(0, 300)  # Tempo aleatório para o próximo pulo
        self.jump_counter = 0
        self.jump_height = random.randint(-20, -10)  # Altura do pulo

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
            self.speedx = random.randint(1, 3)
        # Lógica para pular

        self.jump_counter += 1
        if self.jump_counter >= self.jump_time and self.on_ground:
            self.speedy = self.jump_height
            self.on_ground = False
            self.jump_counter = 0
            self.jump_time = random.randint(100, 300) # Define um novo tempo aleatório para o próximo pulo
        # Atualiza a posicao vertical do zombie
        if not self.on_ground:
            self.speedy += 1
        self.rect.y += self.speedy
        # Verifica se o zombie esta no chão
        if self.rect.bottom >= HEIGHT - 100:
            self.rect.bottom = HEIGHT - 100
            self.on_ground = True
            self.speedy = 0