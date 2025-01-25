import os
import pygame
import sys
import threading
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import time
import random
import webbrowser
from canvasapi import Canvas
import pyperclip

API_URL = "https://canvas.eee.uci.edu"
api_token_url = "https://canvas.eee.uci.edu/profile/settings"

def wait_for_valid_token():
    print("Waiting for a valid API token. Copy the token to your clipboard.")
    while True:
        # Wait for the user to copy something to the clipboard
        token = pyperclip.paste()
        if token.strip():  # Ensure the token is not empty
            print(f"Checking token: {token}")
            if connect_to_canvas(token):  # Validate the token
                print("Successfully connected to Canvas!")
                return token
            else:
                print("Invalid token. Please copy a valid token to the clipboard.")
        time.sleep(1)  # Wait a second before checking the clipboard again

def create_image():
    size = 64
    color = "blue"
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, size, size), fill=color)
    return image

def on_tray_click(icon, item):
    global running, minimized
    minimized = False
    pygame.display.set_mode((400, 400))
    icon.stop()

def quit_app(icon, item):
    global running
    running = False
    icon.stop()

def run_tray():
    tray_image = create_image()
    menu = Menu(
        MenuItem("Open", on_tray_click),
        MenuItem("Quit", quit_app)
    )
    tray_icon = Icon("Tamagotchi", tray_image, "Tamagotchi Anteater", menu)
    tray_icon.run()
    
def connect_to_canvas(api_key):
    canvas = Canvas(API_URL, api_key)
    try:
        user = canvas.get_user('self')
        print(f"Connected as {user.name}")
        return True
    except Exception as e:
        print(f"Failed to connect: {e}")
        return False
    
def resize_to_aspect_ratio(img, width, height):
    img_rect = img.get_rect()
    aspect_ratio = img_rect.width / img_rect.height
    if img_rect.width > img_rect.height:
        new_width = width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = height
        new_width = int(new_height * aspect_ratio)
    return pygame.transform.scale(img, (new_width, new_height))

screen_width, screen_height = 400, 400
image_width, image_height = int(screen_width * 0.25), int(screen_height * 0.25)

#images will be reinitialized to correct pngs later by change mood
stand_img=pygame.image.load("pet_assets\stand.png")
walk1_left_img = pygame.image.load("pet_assets\stand.png")
walk2_left_img = pygame.image.load("pet_assets\stand.png")
walk1_right_img =pygame.image.load("pet_assets\stand.png")
walk2_right_img = pygame.image.load("pet_assets\stand.png")

#switch walk cycle
def change_mood(stand, walk1_left, walk2_left, walk1_right, walk2_right):   
    global stand_img, walk1_left_img, walk2_left_img, walk1_right_img, walk2_right_img
    stand_img = pygame.image.load(stand)
    walk1_left_img = pygame.image.load(walk1_left)
    walk2_left_img = pygame.image.load(walk2_left)
    walk1_right_img = pygame.image.load(walk1_right)
    walk2_right_img = pygame.image.load(walk2_right)

    stand_img = resize_to_aspect_ratio(stand_img, image_width, image_height)
    walk1_left_img = resize_to_aspect_ratio(walk1_left_img, image_width, image_height)
    walk2_left_img = resize_to_aspect_ratio(walk2_left_img, image_width, image_height)
    walk1_right_img = resize_to_aspect_ratio(walk1_right_img, image_width, image_height)
    walk2_right_img = resize_to_aspect_ratio(walk2_right_img, image_width, image_height)

pygame.init()

change_mood("pet_assets/stand.png","pet_assets/walk1_left.png","pet_assets/walk2_left.png","pet_assets/walk1_right.png","pet_assets/walk2_right.png")
pixel_font = pygame.font.Font("PressStart2P.ttf", 20)

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption("Tamagotchi Anteater")
clock = pygame.time.Clock()

running = True
minimized = False
anteater_color = (150, 75, 0)
square_pos = [150, 150]
square_speed = 1
move_counter = 0
window_pos = [500, 500]
target_pos = [150, 150]
target_reach_threshold = 5
move_delay = random.randint(2, 5)
last_move_time = time.time()
image_switch_delay = 0.4
last_image_switch_time = time.time()

# Variables for the API token input
input_text = ""
input_active = False
font = pygame.font.Font(None, 30)

def random_target():
    x = random.randint(0, 300)
    y = random.randint(0, 300)
    return [x, y]

def get_api_token_from_clipboard():
    token = pyperclip.paste()  # Get text from clipboard
    return token

def move_towards_target():
    global square_pos, last_image_switch_time, walk1_left_img, walk2_left_img, walk1_right_img, walk2_right_img
    target_x, target_y = target_pos
    direction_x = target_x - square_pos[0]
    direction_y = target_y - square_pos[1]
    distance = (direction_x**2 + direction_y**2) ** 0.5
    if distance > 0:
        direction_x /= distance
        direction_y /= distance
    square_pos[0] += direction_x * square_speed
    square_pos[1] += direction_y * square_speed
    if direction_x < 0:
        if time.time() - last_image_switch_time > image_switch_delay:
            walk1_left_img, walk2_left_img = walk2_left_img, walk1_left_img
            last_image_switch_time = time.time()
    elif direction_x > 0:
        if time.time() - last_image_switch_time > image_switch_delay:
            walk1_right_img, walk2_right_img = walk2_right_img, walk1_right_img
            last_image_switch_time = time.time()

def get_font_size_for_button(text, width, height, max_font_size=30):
    font_size = max_font_size
    font = pygame.font.Font("PressStart2P.ttf", font_size)
    text_surface = font.render(text, True, (0, 0, 0))
    while text_surface.get_width() > width - 10 or text_surface.get_height() > height - 10:
        font_size -= 1
        font = pygame.font.Font("PressStart2P.ttf", font_size)
        text_surface = font.render(text, True, (0, 0, 0))
        if font_size <= 10:
            break
    return font, text_surface

def draw_rounded_button(text, x, y, width, height, radius=10):
    font, text_surface = get_font_size_for_button(text, width, height)
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), border_radius=radius)
    pygame.draw.rect(screen, (255, 255, 255), (x+2, y+2, width-4, height-4), border_radius=radius)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

# Updated button size to accommodate the text
button_width, button_height = 180, 70  # Increased size for better text fit

# Center the button at the top of the screen
button_x = (screen_width - button_width) // 2
button_y = 20  # A little space from the top

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                minimized = True
                pygame.display.iconify()
                threading.Thread(target=run_tray, daemon=True).start()
            if event.key == pygame.K_l:
                change_mood("pet_assets/lebronhappy.png","pet_assets/lebronhappy.png","pet_assets/lebronhappy.png","pet_assets/lebronhappy.png","pet_assets/lebronhappy.png")
            
            if input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # Handle API token after hitting Enter
                    print(f"Connecting to Canvas with token: {input_text}")
                    while not connect_to_canvas(input_text):
                        input_text = ""
                        print("Invalid token. Please try again.")
                        input_active = True
                else:
                    input_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                print("Connecting to Canvas...")
                webbrowser.open(api_token_url)  # Redirect to the API token page
                # Get API token directly from the clipboard
                api_key = get_api_token_from_clipboard()
                token = wait_for_valid_token()  # Wait for a valid token to be copied to the clipboard
                print(f"Token received: {token}")
                # Try connecting to Canvas with the clipboard token
                while not connect_to_canvas(api_key):
                    print("Invalid token. Please try again.")
                    api_key = get_api_token_from_clipboard()
                    

    if time.time() - last_move_time > move_delay:
        move_towards_target()
        target_x, target_y = target_pos
        if abs(square_pos[0] - target_x) < target_reach_threshold and abs(square_pos[1] - target_y) < target_reach_threshold:
            target_pos = random_target()
            last_move_time = time.time()
            move_delay = random.randint(2, 5)

    if not minimized:
        screen.fill((255, 255, 255))

        if square_pos[0] > target_pos[0]:
            screen.blit(walk1_left_img, (square_pos[0], square_pos[1]))
        elif square_pos[0] < target_pos[0]:
            screen.blit(walk1_right_img, (square_pos[0], square_pos[1]))
        else:
            screen.blit(stand_img, (square_pos[0], square_pos[1]))

        draw_rounded_button("Connect to Canvas", button_x, button_y, button_width, button_height)

        if input_active:
            pygame.draw.rect(screen, (0, 0, 0), (button_x, button_y + button_height + 10, button_width, 30))
            text_surface = font.render(input_text, True, (255, 255, 255))
            screen.blit(text_surface, (button_x + 5, button_y + button_height + 10))

        pygame.display.flip()

    clock.tick(120)

pygame.quit()
