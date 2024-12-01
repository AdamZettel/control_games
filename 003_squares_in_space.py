import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Squares in Space")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
FONT = pygame.font.Font(None, 36)
LARGE_FONT = pygame.font.Font(None, 72)

# FPS
FPS = 60

# Game settings
player_width, player_height = 50, 40
enemy_width, enemy_height = 40, 30
bullet_width, bullet_height = 5, 10

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, -10, RED)
        all_sprites.add(bullet)
        player_bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((enemy_width, enemy_height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed = -self.speed
            self.rect.y += 30
        if random.random() < 0.01:  # Chance to shoot
            bullet = Bullet(self.rect.centerx, self.rect.bottom, 5, WHITE)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, color):
        super().__init__()
        self.image = pygame.Surface((bullet_width, bullet_height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# Functions
def spawn_enemies(level):
    """Spawns enemies based on the current level."""
    for i in range(level + 5):  # Increase number of enemies with level
        x = random.randint(0, WIDTH - enemy_width)
        y = random.randint(30, 150)
        speed = random.choice([2, 3, 4]) + level  # Faster enemies at higher levels
        enemy = Enemy(x, y, speed)
        all_sprites.add(enemy)
        enemies.add(enemy)

def reset_game():
    """Resets the game state for a new game."""
    all_sprites.empty()
    enemies.empty()
    player_bullets.empty()
    enemy_bullets.empty()

    player = Player()
    all_sprites.add(player)
    spawn_enemies(1)
    return player, 0, 1  # Return initial player, score, and level

def show_final_score(score):
    """Displays the final score and restart prompt."""
    screen.fill(BLACK)
    final_text = LARGE_FONT.render("Game Over", True, RED)
    score_text = FONT.render(f"Final Score: {score}", True, WHITE)
    restart_text = FONT.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(final_text, (WIDTH // 2 - final_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

# Main game loop
running = True
while running:
    # Sprite groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()

    player, score, level = reset_game()
    in_game = True
    clock = pygame.time.Clock()

    while in_game:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Update
        all_sprites.update()

        # Collision detection
        for hit in pygame.sprite.groupcollide(enemies, player_bullets, True, True):
            score += 10

        # Progress to next level when all enemies are destroyed
        if not enemies:
            level += 1
            spawn_enemies(level)

        # Player hit by enemy bullet
        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            in_game = False

        # Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Display score and level
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        level_text = FONT.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (WIDTH - 150, 10))

        pygame.display.flip()

    # Show final score and wait for restart or quit
    show_final_score(score)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    waiting = False
                if event.key == pygame.K_q:  # Quit the game
                    running = False
                    waiting = False

pygame.quit()
