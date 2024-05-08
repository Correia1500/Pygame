import pygame
import sys

# Inicializa Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Animação de Corrida')

# Carrega a spritesheet
spritesheet = pygame.image.load('assets/Run.png').convert_alpha()

# Função para extrair sprites
def load_sprites(spritesheet, num_sprites, sprite_width, sprite_height):
    sprites = []
    for i in range(num_sprites):
        # Calcula a posição x do sprite na spritesheet
        x = i * sprite_width
        sprite = spritesheet.subsurface(pygame.Rect(x, 0, sprite_width, sprite_height))
        sprites.append(sprite)
    return sprites

# Classe Player
class Player(pygame.sprite.Sprite):
    def __init__(self, sprites):
        super().__init__()
        self.sprites = sprites
        self.current_sprite = 0
        self.image = sprites[self.current_sprite]
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.animation_speed = 0.2

    def animate(self):
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def update(self):
        self.animate()

# Define o número de frames e suas dimensões
num_sprites = 8
sprite_width, sprite_height = spritesheet.get_width() // num_sprites, spritesheet.get_height()

# Carrega os sprites
sprites = load_sprites(spritesheet, num_sprites, sprite_width, sprite_height)

# Cria um grupo de sprites e adiciona o Player
player = Player(sprites)
all_sprites = pygame.sprite.Group(player)

# Loop principal
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizações
    all_sprites.update()

    # Desenha tudo
    window.fill((0, 0, 0))
    all_sprites.draw(window)
    pygame.display.update()

    # Controla a taxa de quadros
    clock.tick(60)

pygame.quit()
sys.exit()
