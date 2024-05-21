import pygame
import random
from os import path
from config import *


def init_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    tela_inicial = pygame.image.load(path.join('assets/img', 'inicio.jpg')).convert()
    tela_inicial= pygame.transform.scale(tela_inicial, (WIDTH, HEIGHT))
    tela_inicial_rect = tela_inicial.get_rect()

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
        window.blit(tela_inicial, tela_inicial_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
    return state

# tela final
def end_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    t_final = pygame.image.load(path.join('assets/img', 'game_over.jpg')).convert()
    t_final= pygame.transform.scale(t_final, (WIDTH, HEIGHT))
    final_rect = t_final.get_rect()

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

        

       
