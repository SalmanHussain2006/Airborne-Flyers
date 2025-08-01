import pygame
import subprocess
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()
pygame.init()
userRetrieve = open("uName.txt", "r")
username = userRetrieve.read()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creates a game window with the specified width and height.
pygame.display.set_caption("Airborne Flyers") #title

font = pygame.font.Font("freesansbold.ttf", 24) #font and size defined

#define game variables
background_image = pygame.image.load("plx-2.png") #loads bg image and assigned to variable
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT)) #scales to fit screen

background_width = background_image.get_width()
background_x = 0 #varible to keep track of x co-ords of bg image


def load_gold(username):
    gold = ""
    conn = sqlite3.connect('user_data.db')
    #essentially selecting gold, limit 1 ensures only 1 value is selected
    cursor = conn.execute('SELECT gold FROM users WHERE username=? LIMIT 1', (username,))
    #we know gold is in the index 0 so assign variable gold to that index which holds gold value
    #in the database
    for row in cursor:
        gold = row[0]
    return gold
#defines gold
gold = load_gold(username)  # Retrieve gold from db
def launch_game():
    pygame.quit()
    pygame.init()
    # Launch the game script as a separate process 
    # subproccess.Popen (launches a new python process running playgametest script)
    #stdin part with parameters ensures communication between parent process MAINMENU and child process playgametest
    game_process = subprocess.Popen(["python", "playgametest.py"], stdin=subprocess.PIPE) 

    # Wait for the game process to finish
    #game process here interacts with child process communicate is called without any input parameters and waits for 
    #child child process to reach end of file [0] index retrived data from child process
    game_process.communicate(input=b"")[0]
    #prints after communicate() call returns indicating game process has been finished.
    print("Game finished")
def launch_shop():
    pygame.quit()
    pygame.init()
    subprocess.run(["python", "shop.py"])

def draw_main_menu():
    global gold
    global username
    screen.blit(background_image, (background_x, 0)) #image loaded
    screen.blit(background_image, (background_x + background_width, 0)) #2nd image loaded to create looping when first goes off screen

    play_button = pygame.draw.rect(screen, "light gray", (250, 200, 300, 50), 0, 5) #draws rec box for play button
    play_text = font.render("Play", True, "black") # Renders the text Play
    screen.blit(play_text, (370, 210)) #draws that text on screen at the button co-ords

    options_button = pygame.draw.rect(screen, "light gray", (250, 300, 300, 50), 0, 5)
    options_text = font.render("Shop", True, "black")
    screen.blit(options_text, (365, 310))

    exit_button = pygame.draw.rect(screen, "light gray", (250, 400, 300, 50), 0, 5)
    exit_text = font.render("Exit Game", True, "black")
    screen.blit(exit_text, (340, 410))
    gold_text = font.render("Gold: {:.0f}".format(gold), True, "black")
    screen.blit(gold_text, (10, 10))
    # Display welcome message with username
    welcome_text = font.render("Welcome To Airborne Flyers Player: {}".format(username), True, "black")
    text_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))  # Center the text vertically and horizontally
    screen.blit(welcome_text, text_rect.topleft)
    return play_button, options_button, exit_button #returns the buttons to use later

def handle_main_menu(play_button, options_button, exit_button):
    global background_x #ensures that the global variable is being used not a local one

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    # Scroll the background
    background_x -= 1   #causes that scrolling effect / subtracting 1 from x co-ords

    # Reset background position to create a looping effect
    if background_x <= -background_width:   #once the co-ord becomes less than or equal to negative of the width value 
        background_x = 0                    # of bg_x reset to 0 to create looping

    if play_button.collidepoint(mouse_pos) and mouse_click[0]:      #checks for mouse clicks and how to respond
        print("Play selected")
        
        launch_game()
        
    elif options_button.collidepoint(mouse_pos) and mouse_click[0]:
        print("Shop selected")
        launch_shop()
    elif exit_button.collidepoint(mouse_pos) and mouse_click[0]:
        pygame.quit()
        exit()

def main():
    clock = pygame.time.Clock()
    main_menu = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if main_menu:

            buttons = draw_main_menu()
            handle_main_menu(*buttons)

        pygame.display.update()
        clock.tick(30)

main()