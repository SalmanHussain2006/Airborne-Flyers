import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airborne Flyers")

# Load images
player_image = pygame.image.load("pimage.png")
player_image = pygame.transform.scale(player_image, (50, 50))  # Resize if needed

obstacle_images = [
    pygame.image.load("obs1.png"),
    pygame.image.load("obs2.png"),
    pygame.image.load("obs3.png"),
    pygame.image.load("obs4.png"),
]    
# Load background image
background_image = pygame.image.load("plx-2.png")  # Replace with your background image path

# Background variables
background_width = background_image.get_width()
background_x = 0
# Player variables
player_rect = player_image.get_rect()
player_rect.topleft = (WIDTH // 2 - player_rect.width // 2, HEIGHT // 2 - player_rect.height // 2)
player_speed = 5

# Obstacle variables
obstacles = []
obstacle_speed = 5

# Score variables
score = 0
score_font = pygame.font.Font("freesansbold.ttf", 32)

def create_obstacle():
    obstacle_image = random.choice(obstacle_images)
    obstacle_rect = obstacle_image.get_rect()
    obstacle_rect.topleft = (WIDTH, random.randint(0, HEIGHT - obstacle_rect.height))

    return {
        'image': obstacle_image,
        'rect': obstacle_rect,
        'speed': obstacle_speed,
    }
def draw_game():
    global background_x

    # Draw background
    screen.fill((255, 255, 255))

    # Draw the background twice to create a looping effect
    screen.blit(background_image, (background_x, 0))
    screen.blit(background_image, (background_x + background_width, 0))

    # Draw player and obstacles
    screen.blit(player_image, player_rect)

    for obstacle in obstacles:
        screen.blit(obstacle['image'], obstacle['rect'])

    score_text = score_font.render("Score: {}".format(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
      # Update the background position
    background_x -= player_speed

    # Reset background position to create a looping effect
    if background_x <= -background_width:
        background_x = 0
def handle_game():
    global player_rect, obstacles, score, obstacle_speed

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect.y += player_speed

    # Move the obstacles
    for obstacle in obstacles:
        obstacle['rect'].x -= obstacle['speed']

    # Create a new obstacle with a certain probability
    if random.random() < 0.05:
        obstacles.append(create_obstacle())

    # Remove obstacles that go off the screen
    obstacles = [obstacle for obstacle in obstacles if obstacle['rect'].right > 0]

    # Check for collisions
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle['rect']):
            # Collision occurred
            pygame.quit()
            sys.exit()

    # Update the score
    score += 1

    # Increase obstacle speed gradually
    if score % 100 == 0:
        obstacle_speed += 1

def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        handle_game()
        draw_game()

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
