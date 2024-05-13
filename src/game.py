import pygame
import random
import time

pygame.init()
pygame.mixer.init()

#====== Gera tela principal=====

WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame")



# ----- Inicia assets
ZOMBIE_WIDTH = 50
ZOMBIE_HEIGHT = 50
HOMELESS_WIDTH = 50
HOMELESS_HEIGHT = 50
background_img = pygame.image.load("assets/img/starfield.png").convert()

plataform_img = pygame.image.load("assets/img/plataforma.png")
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

#jump_sound = pygame.mixer.Sound("assets/snd/jump.wav") #som do pulo

## ----- Inicia estruturas de dados
# Definindo os novos tipos

class Homeless(pygame.sprite.Sprite):
    def __init__(self,img,all_sprites,all_beers, beer_img, pew_sound):
        # Construtor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 100
        self.speedx = 0
        self.speedy = 0
        self.on_ground = True # verifica se o jogador está no chão
        self.all_sprites = all_sprites
        self.all_beers = all_beers
        self.beer_img = beer_img
        self.pew_sound = pew_sound 
    
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
        
    def shoot(self):
        #cria um novo tiro, a partir da posição do jogador
        new_beer = Bullet(self.beer_img, self.rect.top, self.rect.centerx)
        self.all_sprites.add(new_beer)
        self.all_beers.add(new_beer)
        self.pew_sound.play()

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
# Classe Beer que representa os tiros
class Bullet(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, img, bottom, centerx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = bottom
        self.rect.centerx = centerx
        self.speedx = 10 # Velocidade fixa para o lado direito
    def updade(self):
        # A bala só se move no eixo x
        self.rect.x += self.speedx

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.left > WIDTH:
            self.kill()
game = True

# variavel para ajustar a velocidade do jogo
clock = pygame.time.Clock()
FPS = 30
# Criando um grupo de beers
all_sprites = pygame.sprite.Group()
all_beers = pygame.sprite.Group()
all_zombies = pygame.sprite.Group()
# Criando o jogador
player = Homeless(homeless_img, all_sprites, all_beers, beer_img, pew_sound)
all_sprites.add(player)
# Criando os zumbies
for i in range(10):
    z = Zombie(zombie_img)
    all_sprites.add(z)
    all_zombies.add(z)
#cria um grupo de sprites e adiciona o jogador
# all_sprites = pygame.sprite.Group()
# all_obstaculos = pygame.sprite.Group()

# player = Player(player_img)
# all_sprites.add(player)
# obstaculo = Obstaculo(obstaculo_img)
# all_obstaculos.add(obstaculo)
# all_sprites.add(obstaculo) #para desenhar o obstaculo na tela

# for i in range(10):
#     #player = Player(player)
#     all_sprites.add(player)

# ===== Loop principal =====

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