import pickle
import pygame
import pyperclip
import random
import threading
import time
import webbrowser

from Button import Button
from TextLabel import TextLabel
from Tray import *
from Canvas import *
from PopupWindow import PopupWindow

pygame.init()
clock = pygame.time.Clock()

# Check to see if the user has already logged in 
token = get_saved_token()

def random_target():
    x = random.randint(0, 300)
    y = random.randint(0, 300)
    return [x, y]

def move_towards_target():
    global pet_pos, last_image_switch_time, walk1_left_img, walk2_left_img, walk1_right_img, walk2_right_img
    target_x, target_y = target_pos
    direction_x = target_x - pet_pos[0]
    direction_y = target_y - pet_pos[1]
    distance = (direction_x**2 + direction_y**2) ** 0.5
    if distance > 0:
        direction_x /= distance
        direction_y /= distance
    pet_pos[0] += direction_x * pet_speed
    pet_pos[1] += direction_y * pet_speed
    if direction_x < 0:
        if time.time() - last_image_switch_time > image_switch_delay:
            walk1_left_img, walk2_left_img = walk2_left_img, walk1_left_img
            last_image_switch_time = time.time()
    elif direction_x > 0:
        if time.time() - last_image_switch_time > image_switch_delay:
            walk1_right_img, walk2_right_img = walk2_right_img, walk1_right_img
            last_image_switch_time = time.time()

def resize(img, width, height):
    img_rect = img.get_rect()
    aspect_ratio = img_rect.width / img_rect.height
    if img_rect.width > img_rect.height:
        new_width = width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = height
        new_width = int(new_height * aspect_ratio)
    return pygame.transform.scale(img, (new_width, new_height))

def start_game(): 
    buttons.remove(canvas_button)
    login_message = TextLabel(f"Logged in as: {get_username(token)}", pygame.font.Font("PressStart2p.ttf", 8), '#FFFFFF', (10, screen_height - 20))
    texts.append(login_message)

stand_img = pygame.image.load("pet_assets/stand.png")
walk1_left_img = pygame.image.load("pet_assets/walk1_left.png")
walk2_left_img = pygame.image.load("pet_assets/walk2_left.png")
walk1_right_img = pygame.image.load("pet_assets/walk1_right.png")
walk2_right_img = pygame.image.load("pet_assets/walk2_right.png")

screen_width, screen_height = 400, 400
screen = pygame.display.set_mode((screen_width, screen_height), pygame. NOFRAME)
pygame.display.set_caption("Tamagotchi Anteater")
image_width, image_height = int(screen_width * 0.25), int(screen_height * 0.25)

stand_img = resize(stand_img, image_width, image_height)
walk1_left_img = resize(walk1_left_img, image_width, image_height)
walk2_left_img = resize(walk2_left_img, image_width, image_height)
walk1_right_img = resize(walk1_right_img, image_width, image_height)
walk2_right_img = resize(walk2_right_img, image_width, image_height)

running = True
minimized = False
anteater_color = (150, 75, 0)
pet_pos = [150, 150]
pet_speed = 1

move_counter = 0
window_pos = [500, 500]
target_pos = [150, 150]
target_reach_threshold = 5
move_delay = random.randint(2, 5)
last_move_time = time.time()
image_switch_delay = 0.4
last_image_switch_time = time.time()

buttons = [] 
canvas_button = Button("Connect to Canvas", 200, 50, (screen_width // 2 - 200 // 2, screen_height // 2 - 50 // 2 - 100), 5, pygame.font.Font("PressStart2p.ttf", 8))
todo_button = Button("To-Do", 50, 50, (screen_width - 50, 10), 5, pygame.font.Font("PressStart2p.ttf", 8))
buttons.append(canvas_button)
buttons.append(todo_button)

texts = []

if not token == "":
    start_game()

# Main Game Loop
while running:
    # Handling Keyboard Events 
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                stand_img = pygame.image.load("pet_assets/lebronhappy.png")
                walk1_left_img = pygame.image.load("pet_assets/lebronhappy.png")
                walk2_left_img = pygame.image.load("pet_assets/lebronhappy.png")
                walk1_right_img = pygame.image.load("pet_assets/lebronhappy.png")
                walk2_right_img = pygame.image.load("pet_assets/lebronhappy.png")
                stand_img = resize(stand_img, image_width, image_height)
                walk1_left_img = resize(walk1_left_img, image_width, image_height)
                walk2_left_img = resize(walk2_left_img, image_width, image_height)
                walk1_right_img = resize(walk1_right_img, image_width, image_height)
                walk2_right_img = resize(walk2_right_img, image_width, image_height)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            canvas_button.check_click()
            todo_button.check_click()
            if canvas_button.pressed:
                if check_valid_token(token):
                    print("Token found. Proceeding with the game...")
                else: 
                    print("Connecting to Canvas...")
                    webbrowser.open(api_token_url)
                    token = pyperclip.paste()
                    while not check_valid_token(token):
                        token = pyperclip.paste()
                    write_token(token)
                    start_game()
                    print(f"Token received: {token}")
            
            if todo_button.pressed:
                todo = get_to_do_list(token)
                todo_popup = PopupWindow(screen, "Todo List", todo)
                todo_popup.show()

    if time.time() - last_move_time > move_delay:
        move_towards_target()
        target_x, target_y = target_pos
        if abs(pet_pos[0] - target_x) < target_reach_threshold and abs(pet_pos[1] - target_y) < target_reach_threshold:
            target_pos = random_target()
            last_move_time = time.time()
            move_delay = random.randint(2, 5)

    if not minimized:
        screen.fill((0, 0, 0))

        if pet_pos[0] > target_pos[0]:
            screen.blit(walk1_left_img, (pet_pos[0], pet_pos[1]))
        elif pet_pos[0] < target_pos[0]:
            screen.blit(walk1_right_img, (pet_pos[0], pet_pos[1]))
        else:
            screen.blit(stand_img, (pet_pos[0], pet_pos[1]))
        
        for button in buttons:
            button.draw(screen)
            
        for text in texts:
            text.draw(screen)  
            
        pygame.display.flip()

    clock.tick(120)

pygame.quit()
