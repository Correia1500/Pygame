import pygame
import random
from os import path
from config import *


def init_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join('assets/img', 'inicio.jpg')).convert()
    background= pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

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

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
    return state

# tela final
def end_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join('assets/img', 'game_over.jpg')).convert()
    background= pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

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

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
    return state
