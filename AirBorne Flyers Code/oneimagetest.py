import pygame
import sys
import math

pygame.init()

WIDTH = 1400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Screen")
#plx -2
bg = pygame.image.load("plx-2.png").convert()
scaled_image = pygame.transform.scale(bg, (WIDTH, HEIGHT))

bg_width = bg.get_width()
bg_x = 0
bg_y = 0

tiles = math.ceil(WIDTH / bg_width) + 1 #+1 as to get third image as when two images first image does not leave screen 
                                        #so blurry mess so need to get third image to reset first to front to give illusion

clock = pygame.time.Clock()

while True:

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #draw scrolling bg
    for i in range(0,tiles):
        screen.blit(scaled_image, (i*bg_width + bg_x, 0))
    #scroll background
    bg_x -= 5

    #reset scroll
    if abs(bg_x) > bg_width:    #abs as scroll can become negative we want absolute value
        bg_x = 0

    pygame.display.update()
    pygame.time.delay(40)  # Add a small delay to control scrolling speed, (background image moves slower higher it is).
    clock.tick(30)

