import pygame
from config import WIDTH, HEIGHT

# Classe Beer que representa os tiros
class Bullet(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, img, bottom, centerx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - 130
        # Coloca no lugar inicial definido em x, y do constutor
        #self.rect.bottom = bottom
        self.rect.centerx = centerx
        self.speedx = -10 # Velocidade fixa para o lado direito
    def update(self):
        # A bala só se move no eixo x
        self.rect.x += self.speedx

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.left > WIDTH:
            self.kill()
