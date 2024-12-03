import pygame
import random

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 40
BIRD_HEIGHT = 40
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_VELOCITY = 4
GRAVITY = 0.5
JUMP_STRENGTH = -10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Set up the screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()

# Load bird image
bird_image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
bird_image.fill(BLACK)

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

        # Prevent bird from falling off screen
        if self.y > SCREEN_HEIGHT - BIRD_HEIGHT:
            self.y = SCREEN_HEIGHT - BIRD_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.top = self.height
        self.bottom = self.height + PIPE_GAP

    def update(self):
        self.x -= PIPE_VELOCITY

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.top))
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom, PIPE_WIDTH, SCREEN_HEIGHT - self.bottom))


# Game loop
def main():
    bird = Bird()
    pipes = []
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(30)  # Limit to 30 frames per second
        screen.fill(BLUE)  # Fill the screen with blue (sky color)

        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()

            # Update bird position
            bird.update()

            # Add new pipes
            if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe())

            # Update and draw pipes
            for pipe in pipes:
                pipe.update()
                pipe.draw()

                # Remove pipes that are off-screen
                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)
                    score += 1

                # Check for collisions with pipes
                if bird.x + BIRD_WIDTH > pipe.x and bird.x < pipe.x + PIPE_WIDTH:
                    if bird.y < pipe.top or bird.y + BIRD_HEIGHT > pipe.bottom:
                        game_over = True  # Game over

            # Draw the bird
            bird.draw()

        else:
            # Game over screen
            font = pygame.font.SysFont("Arial", 48)
            game_over_text = font.render("Game Over", True, WHITE)
            restart_text = font.render("Press R to Restart", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart the game
                        main()
                        return

        # Draw the score
        font = pygame.font.SysFont("Arial", 32)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
