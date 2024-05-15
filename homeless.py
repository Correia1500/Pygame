import pygame
from bullet import Bullet
from assets import load_sprites_homeless
from config import *

class Homeless(pygame.sprite.Sprite):
    def __init__(self, all_sprites, all_beers, beer_img, pew_sound):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = load_sprites_homeless()
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
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
        self.animation_speed = 0.2
        self.pulando = False

    def animate(self):
        self.current_sprite = self.animation_speed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
#adicior pulando aqui            

    
    def update(self):
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

        self.animate()
        
    def shoot(self):
        #cria um novo tiro, a partir da posição do jogador
        new_beer = Bullet(self.beer_img, self.rect.top, self.rect.centerx)
        self.all_sprites.add(new_beer)
        self.all_beers.add(new_beer)
        self.pew_sound.play()