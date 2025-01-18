import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set up game window
WIDTH, HEIGHT = 1550, 850

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Complicated Game')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up fonts
font = pygame.font.SysFont('arial', 24)

# Game variables
player_speed = 5
score = 0
clock = pygame.time.Clock()

# Define player and enemy classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.x_speed = 0
        self.y_speed = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += player_speed
        if keys[pygame.K_UP]:
            self.rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            self.rect.y += player_speed

        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-50)
        self.rect.y = random.randint(-100, -50)
        self.y_speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH-50)
            self.rect.y = random.randint(-100, -50)
            global score
            score -= 1  # Decrease score if enemy passes by

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-30)
        self.rect.y = random.randint(-100, -50)
        self.y_speed = random.randint(2, 4)

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH-30)
            self.rect.y = random.randint(-100, -50)
        if self.rect.colliderect(player.rect):
            global score
            score += 5  # Increase score if player collects power-up
            self.rect.x = random.randint(0, WIDTH-30)
            self.rect.y = random.randint(-100, -50)

def reset_game():
    global score
    # Reset all necessary game variables
    score = 0
    player.rect.center = (WIDTH // 2, HEIGHT - 50)

    # Clear all previous enemies and power-ups
    for enemy in enemies:
        enemy.kill()
    for power_up in powerups:
        power_up.kill()

    # Reinitialize enemies and power-ups
    for _ in range(5):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    for _ in range(2):
        power_up = PowerUp()
        all_sprites.add(power_up)
        powerups.add(power_up)

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Create initial enemies and power-ups
for _ in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

for _ in range(2):
    power_up = PowerUp()
    all_sprites.add(power_up)
    powerups.add(power_up)

# Game loop
def game_loop():
    running = True
    global score
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update
        all_sprites.update()

        # Collision detection
        if pygame.sprite.spritecollide(player, enemies, False):
            print("Game Over! Press 'R' to Restart or 'Q' to Quit.")
            display_restart_screen()
            return

        # Drawing
        screen.fill(WHITE)
        all_sprites.draw(screen)

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Refresh screen
        pygame.display.flip()

        # Frame rate
        clock.tick(60)

def display_restart_screen():
    # Display a game over message and restart prompt
    game_over_text = font.render("Game Over! Press 'R' to Restart or 'Q' to Quit.", True, BLACK)
    screen.fill(WHITE)
    screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()

    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_loop()  # Restart the game
                    waiting_for_restart = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Start the game
game_loop()
