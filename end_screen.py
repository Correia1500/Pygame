import pygame
from config import *
from assets import *
from homeless import *
from zombie import *
from bat import *
from powerup import *
import random




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