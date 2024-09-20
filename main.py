import pygame
import sys

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

# Function to create a grass texture
def create_grass_texture(width, height):
    surface = pygame.Surface((width, height))
    surface.fill((0, 128, 0))  # Base green color
    return surface

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer with Moving Platforms")

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

# Define static platforms
platforms = [
    pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),
    pygame.Rect(100, SCREEN_HEIGHT - 100, 80, 10),
    pygame.Rect(200, SCREEN_HEIGHT - 100, 80, 10),
]

# Define moving platforms
moving_platforms = [
    {"rect": pygame.Rect(100, SCREEN_HEIGHT - 200, 100, 10), "speed_x": 2, "speed_y": 0, "direction_x": 1, "direction_y": 0},
    {"rect": pygame.Rect(400, SCREEN_HEIGHT - 300, 150, 10), "speed_x": 3, "speed_y": 0, "direction_x": 1, "direction_y": 0},
    {"rect": pygame.Rect(600, SCREEN_HEIGHT - 400, 100, 10), "speed_x": 0, "speed_y": 2, "direction_x": 0, "direction_y": 1},
]

# Scrolling variables
camera_x = 0
camera_y = 0

drawing = False
start_pos = None

def draw_player(x, y):
    pygame.draw.rect(screen, RED, (x - camera_x, y - camera_y, player_size, player_size))

def draw_platforms(texture):
    texture_width, texture_height = texture.get_size()
    for platform in platforms:
        for x in range(int(platform.x - camera_x), int(platform.x - camera_x + platform.width), texture_width):
            for y in range(int(platform.y - camera_y), int(platform.y - camera_y + platform.height), texture_height):
                screen.blit(texture, (x, y))

def draw_moving_platforms(texture):
    texture_width, texture_height = texture.get_size()
    for platform in moving_platforms:
        rect = platform["rect"]
        for x in range(int(rect.x - camera_x), int(rect.x - camera_x + rect.width), texture_width):
            for y in range(int(rect.y - camera_y), int(rect.y - camera_y + rect.height), texture_height):
                screen.blit(texture, (x, y))

def move_platforms():
    for platform in moving_platforms:
        platform["rect"].x += platform["speed_x"] * platform["direction_x"]
        platform["rect"].y += platform["speed_y"] * platform["direction_y"]

        # Horizontal boundaries for left-right movement
        if platform["rect"].x < 0 or platform["rect"].x + platform["rect"].width > 3000:  # Limit to large area
            platform["direction_x"] *= -1

        # Vertical boundaries for up-down movement
        if platform["rect"].y < 0 or platform["rect"].y + platform["rect"].height > SCREEN_HEIGHT:
            platform["direction_y"] *= -1

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

    # Check collisions with moving platforms
    for platform in moving_platforms:
        if drop_through and velocity_y > 0:  # Drop through moving platforms
            continue

        rect = platform["rect"]
        if (x + player_size > rect.x and x < rect.x + rect.width and
                y + player_size > rect.y and y < rect.y + rect.height):
            if velocity_y > 0:
                y = rect.y - player_size
                return y, 0, False
            elif velocity_y < 0:
                y = rect.y + rect.height
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
    global player_x, player_y, player_velocity_y, is_jumping, platforms, drawing, start_pos, camera_x, camera_y

    grass_texture = create_grass_texture(100, 10)

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

        # Move moving platforms
        move_platforms()

        # Check for platform collisions, with drop-through support
        player_y, player_velocity_y, is_jumping = check_collisions(player_x, player_y, player_velocity_y, drop_through)

        # Camera follow player
        camera_x = player_x - SCREEN_WIDTH // 2
        camera_y = player_y - SCREEN_HEIGHT // 2

        screen.fill(WHITE)

        # Draw static and moving platforms
        draw_platforms(grass_texture)
        draw_moving_platforms(grass_texture)

        # Draw player
        draw_player(player_x, player_y)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()