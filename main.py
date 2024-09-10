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


# Function to create a grass texture
def create_grass_texture(width, height):
    """Creates a grass texture using a simple algorithm.

    Args:
        width: The width of the texture.
        height: The height of the texture.

    Returns:
        A pygame Surface object representing the grass texture.
    """
    surface = pygame.Surface((width, height))
    surface.fill((0, 128, 0))  # Base green color

    # Add some variation for a natural look
    for x in range(width):
        for y in range(height):
            color_variation = pygame.Color(0, 0, 0, 10)  # Slight dark variation
            current_color = surface.get_at((x, y))
            new_color = (min(current_color.r + color_variation.r, 255),
                         min(current_color.g + color_variation.g, 255),
                         min(current_color.b + color_variation.b, 255))
            surface.set_at((x, y), new_color)

    return surface


# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Player properties
player_size = 20
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
player_speed = 5
player_velocity_y = 0
gravity = 0.5
jump_power = -10
is_jumping = False

# Define platforms
platforms = [
    pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH * 3, 50),
    pygame.Rect(10, 10, 20, 10),
    pygame.Rect(50, 200, 100, 10),
    pygame.Rect(50, 275, 100, 10),
    pygame.Rect(185, 340, 100, 10),
    pygame.Rect(355, 425, 100, 10),
    pygame.Rect(50, 500, 300, 10),
    pygame.Rect(1000, 500, 300, 10)  # Ground platform
]

# Scrolling variables
camera_x = 0
camera_y = 0

drawing = False
start_pos = None


def draw_player(x, y):
    pygame.draw.rect(screen, RED, (x - camera_x, y - camera_y, player_size, player_size))


def draw_platforms(texture):
    """Draws platforms with the given texture, tiling as necessary."""
    texture_width, texture_height = texture.get_size()
    for platform in platforms:
        # Tile the texture across the platform
        for x in range(platform.x - camera_x, platform.x - camera_x + platform.width, texture_width):
            for y in range(platform.y - camera_y, platform.y - camera_y + platform.height, texture_height):
                screen.blit(texture, (x, y))


def check_collisions(x, y, velocity_y):
    for platform in platforms:
        if (x + player_size > platform.x and x < platform.x + platform.width and
                y + player_size > platform.y and y < platform.y + platform.height):
            if velocity_y > 0:  # Falling down
                y = platform.y - player_size
                return y, 0, False
            elif velocity_y < 0:  # Jumping up
                y = platform.y + platform.height
                return y, 0, is_jumping
    return y, velocity_y, is_jumping


def game_loop():
    global player_x, player_y, player_velocity_y, is_jumping, platforms, drawing, start_pos, camera_x, camera_y

    # Create grass texture
    grass_texture = create_grass_texture(100, 10)  # Create a 100x50 grass texture

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
                    platforms.append(pygame.Rect(x - camera_x, y - camera_y, width, height))
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

        # Update camera position to follow the player
        camera_x = player_x - SCREEN_WIDTH // 2
        camera_y = player_y - SCREEN_HEIGHT // 2

        # Prevent the camera from going out of bounds
        max_camera_x = max(0, max(p.x + p.width for p in platforms) - SCREEN_WIDTH)
        max_camera_y = max(0, max(p.y + p.height for p in platforms) - SCREEN_HEIGHT)
        camera_x = min(max(camera_x, 0), max_camera_x)
        camera_y = min(max(camera_y, 0), max_camera_y)

        # Clear the screen
        screen.fill(WHITE)

        # Draw platforms with texture
        draw_platforms(grass_texture)

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
            pygame.draw.rect(screen, BLUE, (x - camera_x, y - camera_y, width, height),
                             2)  # Outline the platform being drawn

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)


if __name__ == "__main__":
    game_loop()