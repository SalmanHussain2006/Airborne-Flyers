import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airborne Flyers")

font = pygame.font.Font("freesansbold.ttf", 24)

#define game variables
scroll = 0

bg_images = []

for i in range(1, 5):
    bg_image = pygame.image.load(f"plx-{i}.png").convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

def draw_bg():
    for i, image in enumerate(bg_images):
        x_position = i * bg_width - scroll
        screen.blit(image, (x_position, 0))


def draw_main_menu():
    screen.fill((255, 255, 255))
    draw_bg()
    play_button = pygame.draw.rect(screen, "light gray", (250, 200, 300, 50), 0, 5)
    play_text = font.render("Play", True, "black") 
    screen.blit(play_text, (370, 210))

    options_button = pygame.draw.rect(screen, "light gray", (250, 300, 300, 50), 0, 5)
    options_text = font.render("Options", True, "black")
    screen.blit(options_text, (340, 310))

    exit_button = pygame.draw.rect(screen, "light gray", (250, 400, 300, 50), 0, 5)
    exit_text = font.render("Exit Game", True, "black")
    screen.blit(exit_text, (340, 410))

    return play_button, options_button, exit_button

def handle_main_menu(play_button, options_button, exit_button):
    global scroll
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    # background scroll
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        scroll -= 5
    if key[pygame.K_RIGHT]:
        scroll += 5

    if play_button.collidepoint(mouse_pos) and mouse_click[0]:
        print("Play selected")
        # Add logic for starting the game
    elif options_button.collidepoint(mouse_pos) and mouse_click[0]:
        print("Options selected")
        # Add logic for handling options
    elif exit_button.collidepoint(mouse_pos) and mouse_click[0]:
        pygame.quit()
        sys.exit()

def main():
    clock = pygame.time.Clock()
    main_menu = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
        if main_menu:
            buttons = draw_main_menu()
            handle_main_menu(*buttons)
        
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
