import pygame
import Canvas
import CanvasFinalGrds
# Happiness variables
happiness = 100
happiness_decay_rate = 0.1
happiness_increase = 10

def update_happiness(delta_time):
    """Decrease happiness over time."""
    global happiness
    happiness -= happiness_decay_rate * delta_time
    # Keep happiness between 0 and avg final course grade
    # If token does not exist, then assume average scores are 100
    avgScores = 100
    tkn = Canvas.get_saved_token
    if (Canvas.check_valid_token(tkn)):
        scoreDict = CanvasFinalGrds.finalGradesDict(tkn)
        # Accumulator to count number of courses with final grds
        totalGrds = 0
        numOfGrds = 0
        for score in scoreDict.values():
            if (score != None):
                totalGrds += score
                numOfGrds += 1
        if (numOfGrds != 0):
            avgScores = int(totalGrds / numOfGrds)
            
        print('bruh')
    happiness = max(0, min(happiness, avgScores))  

def increase_happiness(amount):
    """Increase happiness by a given amount."""
    global happiness
    happiness += amount
    happiness = min(happiness, 100)  # Cap happiness at 100

def draw_happiness_meter(screen, screen_width, screen_height):
    """Render the happiness meter on the screen."""
    global happiness

    # Define bar dimensions
    bar_width = 200
    bar_height = 20
    bar_x = (screen_width - bar_width) // 2
    bar_y = screen_height - 50

    # Background bar (gray)
    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

    # Foreground bar (green for current happiness)
    happiness_width = int((happiness / 100) * bar_width)
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, happiness_width, bar_height))

    # Happiness text
    font = pygame.font.Font("PressStart2p.ttf", 8)
    text = font.render(f"Happiness: {int(happiness)}", True, (255, 255, 255))
    screen.blit(text, (bar_x, bar_y - 15))