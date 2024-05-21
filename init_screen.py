import pygame
import random
from os import path
from config import *


def init_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join('assets/img/inicio.jpg')).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

    # Carrega o título e o botão
    font = pygame.font.SysFont(None, 74)
    small_font = pygame.font.SysFont(None, 48)
    title_text = font.render("ZOMBIE RUN", True, (255, 0, 0))
    start_button_text = small_font.render("Press any key to start", True, (255, 255, 255))

    running = True
    state = INIT

    while running:
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processamento de eventos(mouse, teclado, botão, etc ).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
            if event.type == pygame.KEYUP:
                state = GAME
                running = False

        # A cada loop, redesenha o fundo e os sprites
        window.fill(BLACK)
        window.blit(background, background_rect)
        window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        window.blit(start_button_text, (WIDTH // 2 - start_button_text.get_width() // 2, HEIGHT // 2))

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
    return state



        

       
