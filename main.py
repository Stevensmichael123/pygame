import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
RESPAWN_X = SCREEN_WIDTH // 2
RESPAWN_Y = SCREEN_HEIGHT // 2
FALL_THRESHOLD = SCREEN_HEIGHT + 100  # If player falls below this Y-coordinate, respawn
PLATFORM_HEIGHT = 10
GRASS_COLOR = (0, 128, 0)

# Number of screens worth of width
WORLD_WIDTH = SCREEN_WIDTH * 5  # Extending the world to 5 times the screen width

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer with Extended Randomized Platforms")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Player properties
player_size = 20
player_x = RESPAWN_X
player_y = RESPAWN_Y
player_speed = 5
player_velocity_y = 0
gravity = 0.5
jump_power = -10
is_jumping = False

# Scrolling variables
camera_x = 0
camera_y = 0

# Create a list of static platforms, randomly generated
def generate_random_platforms(num_platforms, platform_width, world_width, screen_height):
    platforms = []
    current_x = 0  # Start from the left side
    platform_y = screen_height - 50  # Start with the ground level

    for _ in range(num_platforms):
        # Randomize gaps between platforms
        gap = random.randint(100, 200)
        current_x += gap

        if current_x + platform_width > world_width:
            break  # Stop if we're beyond the world width

        # Randomize the Y position of the platform to add vertical variation
        platform_y = random.randint(screen_height - 200, screen_height - 100)

        platform = pygame.Rect(current_x, platform_y, platform_width, PLATFORM_HEIGHT)
        platforms.append(platform)

        # Move current_x forward by the width of the platform
        current_x += platform_width

    return platforms

# Generate random platforms that go across the entire extended world
platforms = generate_random_platforms(50, 100, WORLD_WIDTH, SCREEN_HEIGHT)

# Function to create a grass texture
def create_grass_texture(width, height):
    surface = pygame.Surface((width, height))
    surface.fill(GRASS_COLOR)  # Base green color
    return surface

def draw_player(x, y):
    pygame.draw.rect(screen, RED, (x - camera_x, y - camera_y, player_size, player_size))

def draw_platforms(texture):
    texture_width, texture_height = texture.get_size()
    for platform in platforms:
        for x in range(int(platform.x - camera_x), int(platform.x - camera_x + platform.width), texture_width):
            for y in range(int(platform.y - camera_y), int(platform.y - camera_y + platform.height), texture_height):
                screen.blit(texture, (x, y))

def check_collisions(x, y, velocity_y, drop_through):
    # Check collisions with static platforms
    for platform in platforms:
        if drop_through and velocity_y > 0:  # Drop through platforms only when falling
            continue

        if (x + player_size > platform.x and x < platform.x + platform.width and
                y + player_size > platform.y and y < platform.y + platform.height):
            if velocity_y > 0:
                y = platform.y - player_size
                return y, 0, False
            elif velocity_y < 0:
                y = platform.y + platform.height
                return y, 0, is_jumping

    return y, velocity_y, is_jumping

def respawn_player():
    global player_x, player_y, player_velocity_y, is_jumping
    player_x = RESPAWN_X
    player_y = RESPAWN_Y
    player_velocity_y = 0
    is_jumping = False

# Main game loop
def game_loop():
    global player_x, player_y, player_velocity_y, is_jumping, platforms, camera_x, camera_y

    grass_texture = create_grass_texture(100, PLATFORM_HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # WASD controls
        if keys[pygame.K_a]:  # Move left with 'A'
            player_x -= player_speed
        if keys[pygame.K_d]:  # Move right with 'D'
            player_x += player_speed
        if keys[pygame.K_w] and not is_jumping:  # Jump with 'W'
            player_velocity_y = jump_power
            is_jumping = True

        drop_through = keys[pygame.K_s]  # Holding 'S' to drop through platforms

        player_velocity_y += gravity
        player_y += player_velocity_y

        # Check if the player has fallen off the map
        if player_y > FALL_THRESHOLD:
            respawn_player()

        # Check for platform collisions, with drop-through support
        player_y, player_velocity_y, is_jumping = check_collisions(player_x, player_y, player_velocity_y, drop_through)

        # Camera follow player, within bounds of the extended world
        camera_x = max(0, min(player_x - SCREEN_WIDTH // 2, WORLD_WIDTH - SCREEN_WIDTH))
        camera_y = max(0, min(player_y - SCREEN_HEIGHT // 2, SCREEN_HEIGHT - SCREEN_HEIGHT))

        screen.fill(WHITE)

        # Draw static platforms
        draw_platforms(grass_texture)

        # Draw player
        draw_player(player_x, player_y)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()