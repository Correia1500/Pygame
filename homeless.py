import pygame
from bullet import Bullet
from assets import *
from config import *

class Homeless(pygame.sprite.Sprite):
    def __init__(self, all_sprites, all_beers, beer_img, pew_sound):
        pygame.sprite.Sprite.__init__(self)
        self.sprites_right = load_sprites_homeless_right()
        self.sprites_left = load_sprites_homeless_left()
        self.sprites_jump = load_sprites_homeless_jump()
        self.current_sprite = 0
        self.animation_counter = 0
        
        self.image = self.sprites_right[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 100

        self.speedx = 0
        self.speedy = 0
        self.on_ground = True
        self.all_sprites = all_sprites
        self.all_beers = all_beers
        self.beer_img = beer_img
        self.pew_sound = pew_sound
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 500 #milisegundos
        self.direction = "right"
    
    def update(self):

        self.animation_counter += 1
        if self.on_ground:
            if self.speedx > 0:
                self.direction = "right"
            elif self.speedx < 0:
                self.direction = "left"

            if self.direction == "right":
                if self.animation_counter >= 5:
                    self.current_sprite = (self.current_sprite + 1) % len(self.sprites_right)
                    self.image = self.sprites_right[self.current_sprite]
                    self.animation_counter = 0
            elif self.direction == "left":
                if self.animation_counter >= 5:
                    self.current_sprite = (self.current_sprite + 1) % len(self.sprites_left)
                    self.image = self.sprites_left[self.current_sprite]
                    self.animation_counter = 0
        else:
            self.image = self.sprites_jump[0]  # Usa uma imagem de pulo (pode adicionar animação de pulo)
        

        # Atualiza a posição do jogador
        self.rect.x += self.speedx
        
        # aplica a gravidade se não estiver no chão
        if not self.on_ground:
            self.speedy += 1
        self.rect.y += self.speedy

        # Checa se o jogador está no chão
        if self.rect.bottom >= HEIGHT - 100:
            self.rect.bottom = HEIGHT - 100
            self.on_ground = True
            self.speedy = 0

        # Mantem dentro da tela horizontalmente
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0: 
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
        bullet_bottom = self.rect.top + 40 
        bullet_centerx = self.rect.centerx +15
        new_beer = Bullet(self.beer_img, bullet_bottom, bullet_centerx)
        self.all_sprites.add(new_beer)
        self.all_beers.add(new_beer)
        self.pew_sound.play()