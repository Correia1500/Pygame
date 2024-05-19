import pygame
import random
import time
import sys
from config import *
from assets import *
from homeless import *
from bullet import *
from zombie import *

pygame.init()
pygame.mixer.init()

#====== Gera tela principal=====

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame")

# Carrega a spritesheet
# ----- Inicia assets

font = pygame.font.SysFont(None, 48)
background_img = pygame.image.load("assets/img/background/postapocalypse1.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

plataform_img = pygame.image.load("assets/img/plataforma.png").convert_alpha()
plataform_img = pygame.transform.scale(plataform_img, (WIDTH, 100))

beer_img = pygame.image.load("assets/img/beer.png").convert_alpha()
beer_img = pygame.transform.scale(beer_img, (20, 20))

# Carrega os sons do jogo
pygame.mixer.music.load("assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg") #musica de fundo
pygame.mixer.music.set_volume(0.4)
pew_sound = pygame.mixer.Sound("assets/snd/pew.wav") #som do tiro
collide_sound = pygame.mixer.Sound("assets/snd/expl6.wav") #som da colisão

## ----- Inicia estruturas de dados

game = True
#conflito------------
# Define o número de frames e suas dimensões
# variavel para ajustar a velocidade do jogo
clock = pygame.time.Clock()
FPS = 30
# Criando um grupo de beers
all_sprites = pygame.sprite.Group()
all_beers = pygame.sprite.Group()
all_zombies = pygame.sprite.Group()
# Criando o jogador
sprites = load_sprites_homeless()
# Criando os zumbies

for i in range(10):
    z = Zombie()
    all_sprites.add(z)
    all_zombies.add(z)

# ===== Loop principal =====

player = Homeless(all_sprites, all_beers, beer_img, pew_sound)
all_sprites.add(player)

pygame.mixer.music.play(-1) #inicia a musica de fundo

background_x = 0

while game:
    clock.tick(FPS)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if game == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.shoot()
        #Verifica se apertou alguma tecla
        #if event.type ==pygame.KEYDOWN:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.speedx = -8
    if keys[pygame.K_RIGHT]:
        player.speedx = 8
    if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        player.speedx = 0
    if keys[pygame.K_SPACE] and player.on_ground:
        player.speedy = -20
        player.on_ground = False
    
    
    #Atualiza estado do jogo
    all_sprites.update()
    # Mantém o jogador centralizado na tela ao andar para a direita 
    if player.rect.centerx > WIDTH // 2 and player.speedx > 0:
        background_x -= player.speedx
        player.rect.centerx = WIDTH // 2
    # Mantém o jogador centralizado na tela ao andar para a esquerda
    if player.rect.centerx < WIDTH // 2 and player.speedx < 0:
        background_x -= player.speedx
        player.rect.centerx = WIDTH // 2

    # Verifica colisões
    for bullet in all_beers:
        hits = pygame.sprite.spritecollide(bullet, all_zombies, True)
        for hit in hits:
            bullet.kill()
            z = Zombie()
            all_sprites.add(z)
            all_zombies.add(z)
        
    hits = pygame.sprite.spritecollide(player, all_zombies, False) 
    if hits:
        game = False
        print("Game Over")
    
    #gera saidas
    window.fill((255, 255, 255)) #Preenche a tela com a cor branca

    #Desenha o fundo e as plataformas
    window.blit(background_img, (background_x, 0))
    window.blit(background_img, (background_x + WIDTH, 0))
    
    if background_x <= -WIDTH:
        background_x = 0
    elif background_x >= 0:
        background_x = -WIDTH

    window.blit(plataform_img, (0, HEIGHT - 100))    
    all_sprites.draw(window)  #Desenha o jogador na tela

    #atualiza a tela
    pygame.display.update()

#Finaliza o pygame
pygame.quit()
sys.exit()