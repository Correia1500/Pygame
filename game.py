import pygame
import random
import time
import sys
from config import *
from assets import *
from homeless import *
from bullet import *

pygame.init()
pygame.mixer.init()

#====== Gera tela principal=====

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame")

# Carrega a spritesheet
# ----- Inicia assets

font = pygame.font.SysFont(None, 48)
background_img = pygame.image.load("assets/img/starfield.png").convert()

plataform_img = pygame.image.load("assets/img/plataforma.png").convert_alpha()
plataform_img = pygame.transform.scale(plataform_img, (WIDTH, 100))

homeless_img = pygame.image.load("assets/img/quadrado.png")
homeless_img = pygame.transform.scale(homeless_img, (HOMELESS_WIDTH, HOMELESS_HEIGHT))

zombie_img = pygame.image.load("assets/img/meteorBrown_med1.png").convert_alpha()
zombie_img = pygame.transform.scale(zombie_img, (ZOMBIE_WIDTH, ZOMBIE_HEIGHT))

beer_img = pygame.image.load("assets/img/laserRed16.png").convert_alpha()

# Carrega os sons do jogo
pygame.mixer.music.load("assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg") #musica de fundo
pygame.mixer.music.set_volume(0.4)
pew_sound = pygame.mixer.Sound("assets/snd/pew.wav") #som do tiro
collide_sound = pygame.mixer.Sound("assets/snd/expl6.wav") #som da colisão


## ----- Inicia estruturas de dados


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

game = True
# Define o número de frames e suas dimensões

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
    z = Zombie(zombie_img)
    all_sprites.add(z)
    all_zombies.add(z)


# ===== Loop principal =====
player = Homeless(all_sprites, all_beers, beer_img, pew_sound)
all_sprites.add(player)
pygame.mixer.music.play(loops=-1) #inicia a musica de fundo
while game:
    clock.tick(FPS)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        #Verifica se apertou alguma tecla
        if event.type ==pygame.KEYDOWN:
            #Dependendo da tecla, altera a velocidade
            if event.key == pygame.K_LEFT: #se a tecla for a seta para a esquerda
                player.speedx -= 8
            if event.key == pygame.K_RIGHT:#se a tecla for a seta para a direita
                player.speedx += 8
            if event.key == pygame.K_SPACE and player.on_ground:#se a tecla for a seta para cima
                player.speedy = -20 #pula
                player.on_ground = False
            if event.key == pygame.K_a: # Adiciona a tecla 'A' para atirar
                player.shoot()

        # verifica se soltou alguma tecla
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade
            if event.key == pygame.K_LEFT:
                player.speedx += 8
            if event.key == pygame.K_RIGHT:
                player.speedx -= 8 

    #atualiza estado do jogo

    #atualiza a posição do jogador
    all_sprites.update()

    #verifica se houve colisão entre o jogador e o obstaculo
    # colisao = pygame.sprite.spritecollide(player, all_obstaculos, True)

    # for zumbie in obstaculo: 
    #     z = Zumbie(zumbie_img)
    #     all_sprites.add(z)
    #     all_zumbies.add(z)
        

    # if len(colisao) > 0:
    #     # Toca o som da colisão
    #     collide_sound.play()
    #     time.sleep(1) # Precisa esperar senão fecha o jogo

    #     game = False
        
        

    #gera saidas
    window.fill((255, 255, 255)) #Preenche a tela com a cor branca
    window.blit(plataform_img, (0, 500))
    all_sprites.draw(window)  #Desenha o jogador na tela

    #atualiza a tela
    pygame.display.update()

#Finaliza o pygame
pygame.quit()
sys.exit()