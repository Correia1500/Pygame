# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from config import WIDTH, HEIGHT, INIT, GAME, QUIT 
from game import game

img_if = pygame.image.load("assets/img/inicio.jpg").convert_alpha()

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Zombie Run')

state = INIT
while state != QUIT:
    if state == INIT:
        state = img_if(window)
    elif state == GAME:
        state = game(window)
    else:
        state = QUIT

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados