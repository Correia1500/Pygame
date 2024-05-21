import pygame
from config import *
from assets import *
from homeless import *
from zombie import *
from bat import *
from powerup import *
import random



def game_screen(window):
    # variavel para ajustar a velocidade do jogo
    clock = pygame.time.Clock()

     # Carrega as imagens de fundo para o parallax
    bg_imagens = []
    for i in range(1, 6):
        bg_image = pygame.image.load(f'assets/img/background/parallax/plx-{i}.png').convert_alpha()
        bg_imagens.append(bg_image)
    bg_width = bg_imagens[0].get_width()

    # Carrega outros assets
    plataform_img = pygame.image.load("assets/img/ground2.png").convert_alpha()
    plataform_img = pygame.transform.scale(plataform_img, (WIDTH, 100))

    beer_img = pygame.image.load("assets/img/beer.png").convert_alpha()
    beer_img = pygame.transform.scale(beer_img, (20, 20))

    powerup_img = pygame.image.load("assets/img/powerup.png").convert_alpha()
    powerup_img = pygame.transform.scale(powerup_img, (30, 30))

    lives_img = pygame.image.load("assets/img/coracao.png")
    lives_img = pygame.transform.scale(lives_img, (50, 50))

    # Definindo a fonte para o texto do score
    font = pygame.font.SysFont(None, 48)

    # Carrega os sons do jogo
    pygame.mixer.music.load("assets/snd/muvibeat8_130bpm.mp3")  # música de fundo
    pygame.mixer.music.set_volume(0.4)
    beer_sound = pygame.mixer.Sound("assets/snd/glass_clink.mp3")  # som do tiro
    collide_sound = pygame.mixer.Sound("assets/snd/Zombie_colisao.mp3")  # som da colisão
    powerup_sound = pygame.mixer.Sound("assets/snd/glass_clink.mp3")  # som do powerup

    # Criando um grupo de beers
    all_sprites = pygame.sprite.Group()
    all_beers = pygame.sprite.Group()
    all_zombies = pygame.sprite.Group()
    all_bats = pygame.sprite.Group()
    all_powerups = pygame.sprite.Group()

    # Criando o jogador
    player = Homeless(all_sprites, all_beers, beer_img, beer_sound)
    all_sprites.add(player)
    # Criando os zumbies
    def create_zombie():
        z = Zombie()
        all_sprites.add(z)
        all_zombies.add(z)
    # Criando os morcegos
    def create_bat():
        b = Bat()
        all_sprites.add(b)
        all_bats.add(b)

    # Função para criar powerups
    def create_powerup():
        powerup = PowerUp(powerup_img)
        all_sprites.add(powerup)
        all_powerups.add(powerup)

     # Criando os zumbis iniciais
    for i in range(3):
        create_zombie()

    DONE = 0
    PLAYING = 1
    state = PLAYING


    score = 0 #Pontuação do jogador
    lives = 3 #Vidas do jogador
    powerup_active = False
    powerup_time = 0

    
        # ===== Loop principal =====
    pygame.mixer.music.play(-1) #inicia a musica de fundo
    
    # Variáveis para o parallax
    scroll = 0
    ground_scroll = 0
    ground_image = pygame.image.load("assets/img/ground2.png").convert_alpha()
    ground_width = ground_image.get_width()

    while state != DONE:
        clock.tick(FPS)

         # Spawning logic
        if random.randint(1, 100) > 98 and len(all_bats) < 5:
            create_bat()

        if random.randint(1, 100) > 97 and len(all_powerups) < 3:
            create_powerup()

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

        # Ajustar a lógica de movimento do parallax
        if player.speedx != 0:
            scroll += player.speedx
            
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
                create_zombie()

        # Verifica colisões dos tiros com os morcegos
        for bullet in all_beers:
            hits = pygame.sprite.spritecollide(bullet, all_bats, True)
            for hit in hits:
                bullet.kill()
                score += 100 #Incrementar o score em 10
                create_bat()

            #Verifica colisão do jogador com os zumbis   
        hits = pygame.sprite.spritecollide(player, all_zombies, True) 
        if hits:
            collide_sound.play()
            lives -= 1
            if lives <= 0:
                state = DONE
                print("Game Over")

        #Verifica colisão do jogador com os morcegos
        hits = pygame.sprite.spritecollide(player, all_bats, True)
        if hits:
            collide_sound.play()
            lives -= 1
            if lives <= 0:
                state = DONE
                print("Game Over")

            # Verifica colisão do jogador com os powerups
        hits = pygame.sprite.spritecollide(player, all_powerups, True)
        if hits:
            powerup_sound.play()
            powerup_active = True
            powerup_time = pygame.time.get_ticks()
            for hit in hits:
                hit.kill()

         # Verifica se o powerup ainda está ativo
        if powerup_active:
            if pygame.time.get_ticks() - powerup_time > 5000:  # Duração do powerup: 5 segundos
                powerup_active = False
        
        #Limpa a tela preenchendo com uma cor de fundo
        window.fill((0, 0, 0))

        # Desenha o fundo com parallax
        for x in range(5):
            speed = 1
            for i in bg_imagens:
                window.blit(i, ((x * bg_width) - scroll * speed, 0))
                window.blit(i, ((x * bg_width) - scroll * speed + bg_width, 0))
                speed += 0.2
        
        # Desenha o chão
        for x in range(15):
            window.blit(ground_image, ((x * ground_width) - ground_scroll * 2.5, HEIGHT - 100))
            window.blit(ground_image, ((x * ground_width) - ground_scroll * 2.5 + ground_width, HEIGHT - 100))

        if scroll >= bg_width:
            scroll = 0
        if ground_scroll >= ground_width:
            ground_scroll = 0

        all_sprites.draw(window)  # Desenha o jogador e os inimigos na tela

        #Desenhando o score
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        window.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
        #Desenhando as vidas
        for i in range(lives):
            window.blit(lives_img, (10 + 40 * i, 10))
        #atualiza a tela
        pygame.display.update() # Mostra o novo frame para o jogador

        # Tela de fim de jogo
    end_screen(window, score)
    return QUIT, score

def end_screen(window, score):
    font = pygame.font.SysFont(None, 74)
    small_font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.KEYUP:
                return GAME

        window.fill((0, 0, 0))
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        score_text = small_font.render(f'Score: {score}', True, (255, 255, 255))
        retry_text = small_font.render("Press any key to retry", True, (255, 255, 255))

        window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
        window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        window.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 1.5))

        pygame.display.flip()
        clock.tick(FPS)

    return QUIT
    #Finaliza o pygame
    pygame.quit()
