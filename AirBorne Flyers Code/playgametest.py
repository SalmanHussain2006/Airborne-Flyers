import pygame
import random
import subprocess
from pygame.locals import *
import sqlite3
userRetrieve = open("uName.txt", "r")
username = userRetrieve.read()
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airborne Flyers - Game")

# Load images
player_image = pygame.image.load("pimage.png")
player_image = pygame.transform.scale(player_image, (50, 50))

obstacle_images = [
    pygame.image.load("obs1.png"),
    pygame.image.load("obs2.png"),
    pygame.image.load("obs3.png"),
    pygame.image.load("obs4.png"),
]

# Player variables
player_rect = player_image.get_rect()   #rectangle representing the player
#top left hand corner of rectangle represents plahyer which is then centred to middle of screen 
player_rect.topleft = (WIDTH // 2 - player_rect.width // 2, HEIGHT // 2 - player_rect.height // 2) #(x,y,width,height)
player_speed = 5

# Obstacle variables
obstacles = [] #list to keep track of current obstacles
max_obstacles = 5  # Adjust this value based on the desired difficulty / essentially number of obstacles at one time on screen
obstacle_speed = 5  
obstacle_frequency = 30  #freq and max both adjust how often new obstacles are created
max_obstacle_frequency = 40  # Adjust this value as needed

# Score variables 
score = 0#
score_font = pygame.font.Font("freesansbold.ttf", 32)

# Background variables
background_image = pygame.image.load("plx-2.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
background_width = background_image.get_width() #keeping track of width of image which is width of screen
background_x = 0    #define background x co-ord to keep track 

def load_gold(username):
    global gold
    conn = sqlite3.connect('user_data.db')
    #essentially selecting gold, limit 1 ensures only 1 value is selected
    cursor = conn.execute('SELECT gold FROM users WHERE username=? LIMIT 1', (username,))
    #we know gold is in the index 0 so assign variable gold to that index which holds gold value
    #in the database
    for row in cursor:
        gold = row[0]
    return gold
#gold variable
gold = load_gold(username)
#creates new obstacle with random image, position and speed
#using masks to ensure pixel to pixel collisions
def check_collision(player_rect, player_image, obstacle_rect, obstacle_image):
    player_mask = pygame.mask.from_surface(player_image)
    obstacle_mask = pygame.mask.from_surface(obstacle_image)
    offset = (int(obstacle_rect.x - player_rect.x), int(obstacle_rect.y - player_rect.y))
    overlap = player_mask.overlap(obstacle_mask, offset)
    return overlap is not None
def create_obstacle():
    obstacle_rect = random.choice(obstacle_images).get_rect() #choses random obstacle from list
    obstacle_rect.topleft = (WIDTH, random.randint(0, HEIGHT - obstacle_rect.height)) 

    return {
        'rect': obstacle_rect,
        'speed': obstacle_speed,
        'image': random.choice(obstacle_images),
    }
#simulate scrolling
def draw_game():
    global background_x

    # Draw background
    screen.blit(background_image, (background_x, 0))
    screen.blit(background_image, (background_x + background_width, 0))

    # Draw player and obstacles
    screen.blit(player_image, player_rect)

    for obstacle in obstacles: #This is a loop that iterates over each obstacle in the obstacles list.
        screen.blit(obstacle['image'], obstacle['rect']) #draw an image (the obstacle's image) 
                    #on the screen at a specified position (the obstacle's rectangle).

    # Draw score
    score_text = score_font.render("Score: {}".format(score), True, (0, 0, 0)) #: This renders a text surface for the score.
    screen.blit(score_text, (10, 10)) #draws it at position 10,10
    gold_text = score_font.render("Gold: {:.0f}".format(gold), True, (255, 215, 0))
    screen.blit(gold_text, (10, 50))
    # Update the background position
    background_x -= player_speed

    # Reset background position to create a looping effect
    if background_x <= -background_width:
        background_x = 0

def handle_game():
    global player_rect, obstacles, score, obstacle_speed, obstacle_frequency, gold

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

    # Increase obstacle frequency as score increases
    obstacle_frequency += 1

    # Create new obstacles
    if obstacle_frequency > max_obstacle_frequency and len(obstacles) < max_obstacles:
        obstacles.append(create_obstacle())     #New obstacles are created based on the frequency conditions.
        obstacle_frequency = 0

    # Remove obstacles that go off the screen
    obstacles = [obstacle for obstacle in obstacles if obstacle['rect'].right > 0]

    # Check for collisions
    for obstacle in obstacles: #iterates over each obstacle in the obstacle list
        obstacle_rect = obstacle['rect']
        obstacle_image = obstacle['image']
        if check_collision(player_rect, player_image, obstacle_rect, obstacle_image):
            # Collision occurred
            draw_game_over(score)
            pygame.display.update()
            pygame.time.delay(2000)  # Display the game over screen for 2000 milliseconds (2 seconds)
            pygame.quit()
            exit()
    # Update the score
    score += 1
    gold += 0.1  # Increment gold based on score or distance
    # Increase obstacle speed gradually
    if score % 200 == 0:    #obstacle increases speed for score of every 100 points
        obstacle_speed += 1
def draw_game_over(score):
    # Create a semi-transparent surface
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)#creates new surface with an alpha channel, making it capable of transparency
    #SCRALPHA is in addition to rgb range from 0-255 from transparent -> opaque
    overlay.fill((0, 0, 0, 128))# 128 is the alpha value, making it semi-transparent
    # rest is zero is rgb to be black, 128 is alpha val higher val less transparent
    # Draw the rectangle on the overlay
    pygame.draw.rect(overlay, (255, 255, 255), (100, 200, WIDTH - 200, 300))

    # Render the score text
    font = pygame.font.Font("freesansbold.ttf", 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Blit the overlay onto the screen
    screen.blit(overlay, (0, 0))
    screen.blit(score_text, text_rect)

    return_button_height = HEIGHT // 8
    return_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + return_button_height, WIDTH // 2, return_button_height)

    pygame.draw.rect(screen, (255, 255, 255), return_button_rect)
    pygame.draw.rect(screen, (192, 192, 192), return_button_rect, width=3)

    return_text = score_font.render("Return to Main Menu", True, (0, 0, 0))
    text_rect = return_text.get_rect(center=return_button_rect.center)
    screen.blit(return_text, text_rect)

    #updated gold
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE  users SET gold=? WHERE username=?', (gold,username))
    conn.commit()
    conn.close()

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return #another way to end the loop
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if return_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    pygame.init()
                    subprocess.run(["python", "MAINMENU.py"])
  #effectively ends the loop
        pygame.time.delay(10) #delays execution by 10ms so cpu dont overload
        pygame.display.update()
def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        handle_game()
        draw_game()
        
        pygame.display.update()
        clock.tick(30)

main()