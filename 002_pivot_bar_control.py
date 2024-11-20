import pygame
import pymunk
import pymunk.pygame_util
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pivot Bar")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Physics space
space = pymunk.Space()
space.gravity = (0, 900)  # Gravity pulling down

# Draw options for visualizing pymunk objects
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Create static floor
floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
floor_shape = pymunk.Segment(floor_body, (0, HEIGHT), (WIDTH, HEIGHT), 5)
floor_shape.elasticity = 1.0
space.add(floor_body, floor_shape)

# Game variables
platform_length = 400
score = 0
high_score = 0
game_start_time = time.time()


def reset_game():
    """Reset the game elements after failure."""
    global ball_body, platform_body, score, game_start_time

    # Reset ball
    ball_body.position = WIDTH // 2 + 100, HEIGHT // 2 - 100  # Slightly to the right
    ball_body.velocity = 0, 0

    # Reset platform
    platform_body.position = WIDTH // 2, HEIGHT // 2
    platform_body.angle = 0
    platform_body.angular_velocity = 0

    # Reset score and timer
    score = 0
    game_start_time = time.time()


# Create the pivoting platform
platform_body = pymunk.Body(10, pymunk.moment_for_segment(10, (-platform_length // 2, 0), (platform_length // 2, 0), 5))
platform_body.position = WIDTH // 2, HEIGHT // 2
platform_shape = pymunk.Segment(platform_body, (-platform_length // 2, 0), (platform_length // 2, 0), 5)
platform_shape.friction = 1.0
space.add(platform_body, platform_shape)

# Add a pivot constraint (pin joint) for free rotation
pivot_joint = pymunk.PinJoint(floor_body, platform_body, (WIDTH // 2, HEIGHT // 2), (0, 0))
space.add(pivot_joint)

# Add a rotary limit joint to restrict platform rotation (-30° to 30°)
rotary_limit = pymunk.RotaryLimitJoint(floor_body, platform_body, -0.5, 0.5)  # ±0.5 radians
space.add(rotary_limit)

# Create the ball
ball_radius = 20
ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, ball_radius))
ball_shape = pymunk.Circle(ball_body, ball_radius)
ball_shape.elasticity = 0.8
space.add(ball_body, ball_shape)

# Start the game for the first time
reset_game()

# Game loop to run x times
runs = 10 
total_score = 0

for run in range(runs):
    print(f"Starting run {run + 1}/{runs}")

    # Reset game state at the start of each run
    reset_game()

    # Run the game until the ball falls off the platform
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle user input
        keys = pygame.key.get_pressed()
       
        # Check if ball is outside the platform
        platform_x, platform_y = platform_body.position
        left_end = platform_x - platform_length // 2
        right_end = platform_x + platform_length // 2
        ball_x, ball_y = ball_body.position


        torque = 500000  # Increased torque for noticeable movement

        # CONTROL RULES HERE
        # applies clockwise torque if it is moving left more than 1 velocity unit 
        # and it is less than halfway to the right end

        # applies counterclockwise if it is moving right more the 1 velocity unit
        # and it is greather than halfway from the left end


        vel_x, vel_y = ball_body.velocity
        half_left_end = platform_x - platform_length // 4
        half_right_end = platform_x + platform_length // 4
        max_vel = 1.0
        if vel_x > max_vel and ball_x > half_left_end:
            platform_body.torque = -torque  # Apply counterclockwise torque
        if vel_x < -1.0*max_vel and ball_x < half_right_end:
            platform_body.torque = torque  # Apply clockwise torque



        if ball_x < left_end or ball_x > right_end:
            # Game over, record the score for this run
            total_score += score
            print(f"Run {run + 1} finished. Score: {score}")
            running = False

        # Clear screen
        screen.fill(WHITE)

        # Draw boundary lines
        boundary_line_length = 250
        pygame.draw.line(screen, RED, (left_end, platform_y - boundary_line_length), (left_end, platform_y + boundary_line_length), 3)
        pygame.draw.line(screen, RED, (right_end, platform_y - boundary_line_length), (right_end, platform_y + boundary_line_length), 3)

        # Update score
        score = int(10*(time.time() - game_start_time))

        # Draw score and high score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLUE)
        screen.blit(score_text, (10, 10))

        # Update physics
        space.step(1 / FPS)

        # Draw objects
        space.debug_draw(draw_options)

        # Flip screen
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

# After 20 runs, calculate and display the average score
average_score = total_score / runs
print(f"Average Score: {average_score:.2f}")

# Display the average score at the end of the game
screen.fill(WHITE)
final_text = font.render(f"Average Score: {average_score:.2f}", True, GREEN)
screen.blit(final_text, (WIDTH // 2 - final_text.get_width() // 2, HEIGHT // 2))
pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.delay(3000)

pygame.quit()
