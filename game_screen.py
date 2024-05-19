import pygame
from config import *
from assets import *
from homeless import *
from zombie import *
from bat import *



def game_screen(window):
    # variavel para ajustar a velocidade do jogo
    clock = pygame.time.Clock()

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

    # Criando um grupo de beers
    all_sprites = pygame.sprite.Group()
    all_beers = pygame.sprite.Group()
    all_zombies = pygame.sprite.Group()
    all_bats = pygame.sprite.Group()

    # Criando o jogador
    sprites = load_sprites_homeless()
    player = Homeless(all_sprites, all_beers, beer_img, pew_sound)
    all_sprites.add(player)
    # Criando os zumbies
    for i in range(10):
        z = Zombie()
        all_sprites.add(z)
        all_zombies.add(z)
    # Criando os morcegos
    for i in range(5):
        b = Bat()
        all_sprites.add(b)
        all_bats.add(b)

    DONE = 0
    PLAYING = 1
    state = PLAYING

    keys_down={}
    score = 0
    lives = 3
    
        # ===== Loop principal =====
    pygame.mixer.music.play(-1) #inicia a musica de fundo
    
    background_x = 0 #para animacao do fundo

    while state != QUIT:
        clock.tick(FPS)

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                state = DONE
            # Só verifica o teclado se está no estado de jogo
            if state == PLAYING:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.speedx -= 8
                    if event.key == pygame.K_RIGHT:
                        player.speedx += 8
                    if event.key == pygame.K_SPACE and player.on_ground:
                        player.speedy= -20
                        player.on_ground = False
                    if event.key == pygame.K_a:
                        player.shoot()
                if event.type == pygame.KEYUP:
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_LEFT:
                            player.speedx -= 8
                        if event.key == pygame.K_RIGHT:
                            player.speedx += 8
                        if event.key[pygame.K_SPACE] and player.on_ground:
                            player.speedy = -20
                            player.on_ground = False

        #Atualiza estado do jogo
        all_sprites.update()

        if state == PLAYING:
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

        #Desenhando o score

        #Desenhando as vidas

        #atualiza a tela
        pygame.display.update() # Mostra o novo frame para o jogador

    #Finaliza o pygame
    pygame.quit()
    sys.exit()