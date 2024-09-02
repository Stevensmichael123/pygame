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

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Player properties
player_size = 50
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - player_size
player_speed = 5
player_velocity_y = 0
gravity = 0.5
jump_power = -10
is_jumping = False

# Ground properties
ground_height = SCREEN_HEIGHT - 50

def draw_player(x, y):
    pygame.draw.rect(screen, RED, (x, y, player_size, player_size))

def game_loop():
    global player_x, player_y, player_velocity_y, is_jumping

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

        # Check for collision with ground
        if player_y >= ground_height - player_size:
            player_y = ground_height - player_size
            player_velocity_y = 0
            is_jumping = False

        # Check for left and right boundaries
        if player_x < 0:
            player_x = 0
        if player_x > SCREEN_WIDTH - player_size:
            player_x = SCREEN_WIDTH - player_size

        # Clear the screen
        screen.fill(WHITE)

        # Draw player
        draw_player(player_x, player_y)

        # Draw ground
        pygame.draw.rect(screen, BLACK, (0, ground_height, SCREEN_WIDTH, SCREEN_HEIGHT - ground_height))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    game_loop()