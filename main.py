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
    for x in range(width):
        for y in range(height):
            color_variation = pygame.Color(0, 0, 0, 10)
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
player_x = RESPAWN_X
player_y = RESPAWN_Y
player_speed = 5
player_velocity_y = 0
gravity = 0.5
jump_power = -10
is_jumping = False

# Define platforms
platforms = [
    pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),
    pygame.Rect(100, SCREEN_HEIGHT - 100, 80, 10),
    pygame.Rect(200, SCREEN_HEIGHT - 100, 80, 10),
    pygame.Rect(300, SCREEN_HEIGHT - 100, 80, 10),
    pygame.Rect(400, SCREEN_HEIGHT - 100, 80, 10),
    pygame.Rect(90, SCREEN_HEIGHT - 200, 100, 10),
    pygame.Rect(220, SCREEN_HEIGHT - 200, 100, 10),
    pygame.Rect(350, SCREEN_HEIGHT - 200, 100, 10),
    pygame.Rect(480, SCREEN_HEIGHT - 200, 100, 10),
    pygame.Rect(610, SCREEN_HEIGHT - 200, 100, 10),
    pygame.Rect(130, SCREEN_HEIGHT - 300, 70, 10),
    pygame.Rect(220, SCREEN_HEIGHT - 350, 70, 10),
    pygame.Rect(310, SCREEN_HEIGHT - 400, 70, 10),
    pygame.Rect(400, SCREEN_HEIGHT - 450, 70, 10),
    pygame.Rect(490, SCREEN_HEIGHT - 500, 70, 10),
    pygame.Rect(580, SCREEN_HEIGHT - 550, 70, 10),
    pygame.Rect(670, SCREEN_HEIGHT - 600, 70, 10),
    pygame.Rect(800, SCREEN_HEIGHT - 650, 120, 10)
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
        for x in range(platform.x - camera_x, platform.x - camera_x + platform.width, texture_width):
            for y in range(platform.y - camera_y, platform.y - camera_y + platform.height, texture_height):
                screen.blit(texture, (x, y))

def check_collisions(x, y, velocity_y):
    for platform in platforms:
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

def game_loop():
    global player_x, player_y, player_velocity_y, is_jumping, platforms, drawing, start_pos, camera_x, camera_y

    grass_texture = create_grass_texture(100, 10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    drawing = not drawing

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

        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_SPACE] and not is_jumping:
            player_velocity_y = jump_power
            is_jumping = True

        player_velocity_y += gravity
        player_y += player_velocity_y

        # Check if the player has fallen off the map
        if player_y > FALL_THRESHOLD:
            respawn_player()

        player_y, player_velocity_y, is_jumping = check_collisions(player_x, player_y, player_velocity_y)

        camera_x = player_x - SCREEN_WIDTH // 2
        camera_y = player_y - SCREEN_HEIGHT // 2

        max_camera_x = max(0, max(p.x + p.width for p in platforms) - SCREEN_WIDTH)
        max_camera_y = max(0, max(p.y + p.height for p in platforms) - SCREEN_HEIGHT)
        camera_x = min(max(camera_x, 0), max_camera_x)
        camera_y = min(max(camera_y, 0), max_camera_y)

        screen.fill(WHITE)

        draw_platforms(grass_texture)
        draw_player(player_x, player_y)

        if drawing and start_pos:
            current_pos = pygame.mouse.get_pos()
            x1, y1 = start_pos
            x2, y2 = current_pos
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            x = min(x1, x2)
            y = min(y1, y2)
            pygame.draw.rect(screen, BLUE, (x - camera_x, y - camera_y, width, height), 2)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()