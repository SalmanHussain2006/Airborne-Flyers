import pygame
import subprocess
import sqlite3
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()
pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airborne Flyers - Shop")

font = pygame.font.Font("freesansbold.ttf", 24)
userRetrieve = open("uName.txt", "r")
username = userRetrieve.read()
# Currency variables
gold = 0
# Bird prices
bird_prices = {
    "Pidgeon": 50,
    "Falcon": 100,
    "Dragon": 200
}
# Bird images
bird_images = {
    "Pidgeon": pygame.transform.scale(pygame.image.load("pimage1.png"), (100,50)),
    "Falcon": pygame.transform.scale(pygame.image.load("pimage2.png"), (100,50)),
    "Dragon": pygame.transform.scale(pygame.image.load("pimage3.png"), (100,50)),
}

# Birds bought by the player/ keep track of it
birds_bought = []
#Messages to be sent
messages = []
# Load background image
background_image = pygame.image.load("plx-2.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
background_width = background_image.get_width()
background_x = 0

def load_gold(username):
    cursor.execute('SELECT gold FROM users WHERE username=?', (username,))
    row = cursor.fetchone()
    if row:
        return row[0]  # Return the user's gold balance
    else:
        return 0  # User not found or no gold balance
  
def launch_main_menu():
    pygame.quit()
    pygame.init()
    subprocess.run(["python", "mainmenu.py"])

def draw_shop():
    screen.blit(background_image, (background_x, 0)) #image loaded
    screen.blit(background_image, (background_x + background_width, 0)) #2nd image loaded to create looping when first goes off screen
    # Display gold balance
    gold_text = font.render("Gold: {:.0f}".format(gold), True, "black")
    screen.blit(gold_text, (10, 10))

    # Display available birds and their prices
    # Display available birds, their prices, and images
    y_offset = 100
    for bird, price in bird_prices.items():
        button_rect = pygame.Rect(50, y_offset, 200, 50)
        if bird in birds_bought:
            pygame.draw.rect(screen, (100, 100, 100), button_rect)
        else:
            pygame.draw.rect(screen, "light gray", button_rect)
        text = font.render(f"{bird}: {price} Gold", True, "black")
        screen.blit(text, (50, y_offset + 10))  # Adjusted x-offset for the text
        screen.blit(bird_images[bird], (250, y_offset))  # Adjusted y-offset for the image
        y_offset += 100
    # Draw return button near bottom middle
    return_button = pygame.draw.rect(screen, "light gray", (200, 500, 400, 50)) #rectangle
    return_text = font.render("Return to Main Menu", True, "black") #text
    text_rect = return_text.get_rect(center=return_button.center) #creates a rectangle around text where position is aligned 
    screen.blit(return_text, text_rect) #displays text and rectangle around it

    # Display messages
    for i, message in enumerate(messages):
        message_text = font.render(message, True, "black")
        screen.blit(message_text, (400, 100 + i * 30))  # Adjusted x-offset for the message
def handle_shop():
    global gold, background_x

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
        # Scroll the background
    background_x -= 1   #causes that scrolling effect / subtracting 1 from x co-ords

    # Reset background position to create a looping effect
    if background_x <= -background_width:   #once the co-ord becomes less than or equal to negative of the width value 
        background_x = 0                    # of bg_x reset to 0 to create looping
    if mouse_click[0]:
        # Check if return button is clicked
        if pygame.Rect(200, 500, 400, 50).collidepoint(mouse_pos):
            launch_main_menu()
        # Check if any bird is clicked
        y_offset = 100
        for bird, price in bird_prices.items():
            if pygame.Rect(50, y_offset, 200, 50).collidepoint(mouse_pos):
                if bird in birds_bought:
                    messages.clear()  # Clear previous messages
                    messages.append("You already own this bird")
                    break
                elif gold >= price:
                    gold -= price
                    birds_bought.append(bird)
                    messages.clear()  # Clear previous messages
                    messages.append(f"Bought {bird} for {price} gold")
                    conn = sqlite3.connect('user_data.db')
                    cursor = conn.cursor()
                    cursor.execute('UPDATE  users SET gold=? WHERE username=?', (gold,username))
                    conn.commit()
                    conn.close()
                else:
                    messages.clear()  # Clear previous messages
                    messages.append("Insufficient funds")
                break
            y_offset += 100
            #updated gold
def main():
    global gold
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        gold = load_gold(username)
        draw_shop()
        handle_shop()

        pygame.display.update()
        clock.tick(30)

main()