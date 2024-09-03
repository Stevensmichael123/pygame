import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Player properties
player_size = 20
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - player_size
player_speed = 5
player_velocity_y = 0
gravity = 0.5
jump_power = -12
is_jumping = False

# Define platforms
platforms = [
    pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)  # Ground platform
]
drawing = False
start_pos = None

def draw_player(x, y):
    pygame.draw.rect(screen, RED, (x, y, player_size, player_size))

def draw_platforms():
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

def check_collisions(x, y, velocity_y):
    # Check collision with platforms
    for platform in platforms:
        if (x + player_size > platform.x and x < platform.x + platform.width and
            y + player_size > platform.y and y < platform.y + platform.height):
            if velocity_y > 0:
                # Player is falling and hits the platform
                y = platform.y - player_size
                return y, 0, False
            elif velocity_y < 0:
                # Player is jumping up and hits the platform
                y = platform.y + platform.height
                return y, 0, is_jumping
    return y, velocity_y, is_jumping

def game_loop():
    global player_x, player_y, player_velocity_y, is_jumping, platforms, drawing, start_pos

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    drawing = not drawing  # Toggle drawing mode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if drawing:
                    start_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and start_pos:
                    end_pos = pygame.mouse.get_pos()
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    width = abs(x2 - x1)
                    height = abs(y2 - y1)
                    x = min(x1, x2)
                    y = min(y1, y2)
                    platforms.append(pygame.Rect(x, y, width, height))
                    start_pos = None

        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_SPACE] and not is_jumping:
            player_velocity_y = jump_power
            is_jumping = True

        # Apply gravity
        player_velocity_y += gravity
        player_y += player_velocity_y

        # Check for collisions with platforms
        player_y, player_velocity_y, is_jumping = check_collisions(player_x, player_y, player_velocity_y)

        # Check for left and right boundaries
        if player_x < 0:
            player_x = 0
        if player_x > SCREEN_WIDTH - player_size:
            player_x = SCREEN_WIDTH - player_size

        # Clear the screen
        screen.fill(WHITE)

        # Draw platforms
        draw_platforms()

        # Draw player
        draw_player(player_x, player_y)

        # Draw current platform being drawn
        if drawing and start_pos:
            current_pos = pygame.mouse.get_pos()
            x1, y1 = start_pos
            x2, y2 = current_pos
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            x = min(x1, x2)
            y = min(y1, y2)
            pygame.draw.rect(screen, BLUE, (x, y, width, height), 2)  # Outline the platform being drawn

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    game_loop()