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

    lives_img=pygame.image.load("assets/img/coracao.png")
    lives_img = pygame.transform.scale(lives_img, (50, 50))

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
    for i in range(1):
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
    score = 0 #Pontuação do jogador
    lives = 3 #Vidas do jogador
    
        # ===== Loop principal =====
    pygame.mixer.music.play(-1) #inicia a musica de fundo
    
    background_x = 0 #para animacao do fundo

    while state != DONE:
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
                        player.speedx = - 8
                    if event.key == pygame.K_RIGHT:
                        player.speedx = 8
                    if event.key == pygame.K_SPACE and player.on_ground:
                        player.speedy= -20
                        player.on_ground = False
                    if event.key == pygame.K_a:
                        player.shoot()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.speedx = 0

        #Atualiza estado do jogo
        all_sprites.update()

        if state == PLAYING:
            # Ajustar a lógica de movimento
            if 100 < player.rect.centerx < 700:
                player.speedx = player.speedx
            elif player.rect.centerx >= 700:
                background_x -= player.speedx
            elif player.rect.centerx <= 100:
                background_x += player.speedx
            
            # Ajustar a velocidade dos inimigos com base no movimento do jogador
            if player.speedx == 0:
                enemy_speed_multiplier = 1
            elif player.speedx > 0:
                enemy_speed_multiplier = 0.25
            else:
                enemy_speed_multiplier = 0.25
            
            for zombie in all_zombies:
                zombie.rect.x += zombie.speedx * enemy_speed_multiplier
                if zombie.rect.right < 0:
                    zombie.rect.left = WIDTH
            
            for bat in all_bats:
                bat.rect.x += bat.speedx * enemy_speed_multiplier
                if bat.rect.right < 0:
                    bat.rect.left = WIDTH
            

            # Verifica colisões dos tiros com os zumbis
            for bullet in all_beers:
                hits = pygame.sprite.spritecollide(bullet, all_zombies, True)
                for hit in hits:
                    bullet.kill()
                    score += 100 #Incrementar o score em 100
                    z = Zombie()
                    all_sprites.add(z)
                    all_zombies.add(z)

            # Verifica colisões dos tiros com os morcegos
            for bullet in all_beers:
                hits = pygame.sprite.spritecollide(bullet, all_bats, True)
                for hit in hits:
                    bullet.kill()
                    score += 100 #Incrementar o score em 10
                    b = Bat()
                    all_sprites.add(b)
                    all_bats.add(b)

            #Verifica colisão do jogador com os zumbis   
            hits = pygame.sprite.spritecollide(player, all_zombies, True) 
            if hits:
                collide_sound.play()
                lives -= 1
                if lives<=0:
                    state = DONE
                    print("Game Over")


            #Verifica colisão do jogador com os morcegos
            hits = pygame.sprite.spritecollide(player, all_bats, True)
            if hits:
                collide_sound.play()
                lives -= 1
                if lives<=0:
                    state = DONE
                    print("Game Over")
      
        #gera saidas
        window.fill((255, 255, 255)) #Preenche a tela com a cor branca

        #Desenha o fundo e as plataformas
        window.blit(background_img, (background_x, 0))
        window.blit(background_img, (background_x + WIDTH, 0))
        if lives==3:
            window.blit(lives_img, (10, 10))
            window.blit(lives_img, (30, 10))
            window.blit(lives_img, (50, 10))
        elif lives ==2:
            window.blit(lives_img, (10, 10))
            window.blit(lives_img, (30, 10))
        elif lives ==1:
            window.blit(lives_img, (10, 10))



        
        
        if background_x <= -WIDTH:
            background_x = 0
        elif background_x >= 0:
            background_x = -WIDTH

        window.blit(plataform_img, (0, HEIGHT - 100))    
        all_sprites.draw(window)  #Desenha o jogador na tela

        #Desenhando o score
        score_text = font.render(f'Score: {score}', True, (255, 255, 0))
        window.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
        #Desenhando as vidas
        

        
        

        #atualiza a tela
        pygame.display.update() # Mostra o novo frame para o jogador
    return QUIT
    #Finaliza o pygame
    pygame.quit()
