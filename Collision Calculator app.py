import pygame
import sys
import random
#-----------------------------------------

# Function to calculate the collision time and distances
def calculate_collision_time(total_distance, rate1, rate2):
    time = total_distance / (rate1 + rate2)
    distance1 = rate1 * time
    distance2 = rate2 * time
    return time, distance1, distance2

# Function to reset the positions of the objects and input fields
def reset_positions():
    global x1, x2, start, exploded, explosion_particles
    global total_distance, rate1, rate2
    x1, x2 = radius, WIDTH - radius
    start = False
    exploded = False
    explosion_particles = []

    # Recalculate distances and times based on default values
    time, distance1, distance2 = calculate_collision_time(total_distance, rate1, rate2)
    speed1 = (distance1 / total_distance) * total_distance_pixels / (time * FPS)
    speed2 = (distance2 / total_distance) * total_distance_pixels / (time * FPS)
    
    return time, distance1, distance2, speed1, speed2
#------------------------------------------------------------------------------------------

# Initialize Pygame
pygame.init()
#-------------------------------

# Constants
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 60
EXPLOSION_PARTICLES = 50
FONT_SIZE = 36
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 40
CURSOR_WIDTH = 2
BLINK_RATE = 500  # Cursor blink rate in milliseconds

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Calculator")

# Font setup
font = pygame.font.Font(None, FONT_SIZE)
hint_font = pygame.font.Font(None, FONT_SIZE - 10)  
#-------------------------------------------------------

# Object properties
radius = 20
x1, y1 = radius, HEIGHT // 2
x2, y2 = WIDTH - radius, HEIGHT // 2

# Default values
total_distance = 1
rate1 = 1
rate2 = 1
#---------------------------------------------------------

# Calculate initial collision time and distances
time, distance1, distance2 = calculate_collision_time(total_distance, rate1, rate2)

# Calculate the pixels per frame movement
total_distance_pixels = WIDTH - 2 * radius
speed1 = (distance1 / total_distance) * total_distance_pixels / (time * FPS)
speed2 = (distance2 / total_distance) * total_distance_pixels / (time * FPS)
#--------------------------------------------------------------------------------

# Create input boxes
input_boxes = {
    'total_distance': pygame.Rect(10, 370, 200, 30),
    'rate1': pygame.Rect(215, 370, 160, 30),
    'rate2': pygame.Rect(380, 370, 160, 30)
}

# Labels for input boxes
labels = {
    'total_distance': "Distance(miles)",
    'rate1': "Rate 1(mph)",
    'rate2': "Rate 2(mph)"
}

# Hint text for input boxes
hints = {
    'total_distance': "Enter distance (miles)",
    'rate1': "Enter rate 1 (mph)",
    'rate2': "Enter rate 2 (mph)"
}

# Input box properties
input_texts = {
    'total_distance': '',
    'rate1': '',
    'rate2': ''
}

active_box = None
#------------------------------------------------------------------

# Explosion particles list
explosion_particles = []

# Main loop variables
clock = pygame.time.Clock()
running = True
start = False
exploded = False
last_blink_time = pygame.time.get_ticks()
#---------------------------------------

# Initialize positions and speeds
time, distance1, distance2, speed1, speed2 = reset_positions()
#---------------------------------------------------------------

while running:
    screen.fill(WHITE)

    # Draw objects or explosion particles
    if not exploded:
        pygame.draw.circle(screen, RED, (int(x1), y1), radius)
        pygame.draw.circle(screen, BLUE, (int(x2), y2), radius)

         # Draw labels inside the objects
        obj1_label = font.render("R1", True, WHITE)
        obj2_label = font.render("R2", True, WHITE)
        screen.blit(obj1_label, (int(x1) - obj1_label.get_width() // 2, y1 - obj1_label.get_height() // 2))
        screen.blit(obj2_label, (int(x2) - obj2_label.get_width() // 2, y2 - obj2_label.get_height() // 2))

    else:
        for particle in explosion_particles:
            pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), int(particle['radius']))
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['radius'] -= 0.1  # Gradually shrink particles

        # Remove particles that are too small
        explosion_particles = [p for p in explosion_particles if p['radius'] > 0]

    # Draw labels and input boxes with text
    for key, rect in input_boxes.items():
        # Draw input box
        pygame.draw.rect(screen, BLACK, rect, 2)
        if key == active_box:
            pygame.draw.rect(screen, RED, rect, 2)  # Highlight active box

        # Draw hint text if the input box is empty and not active
        if not input_texts[key] and active_box != key:
            hint_surface = hint_font.render(hints[key], True, BLACK)
            screen.blit(hint_surface, (rect.x + 5, rect.y + 5))
        else:
            text_surface = font.render(input_texts[key], True, BLACK)
            screen.blit(text_surface, (rect.x + 5, rect.y + 5))

        # Draw the cursor if the box is active
        if key == active_box:
            cursor_x = rect.x + font.size(input_texts[key])[0] + 5
            pygame.draw.line(screen, BLACK, (cursor_x, rect.y + 5), (cursor_x, rect.y + rect.height - 5), CURSOR_WIDTH)

    # Draw the reset button
    reset_button = pygame.Rect(WIDTH - BUTTON_WIDTH - 20, HEIGHT - BUTTON_HEIGHT - 60, BUTTON_WIDTH, BUTTON_HEIGHT)  # Bottom right corner
    pygame.draw.rect(screen, BLACK, reset_button)
    reset_text = font.render("Reset", True, WHITE)
    screen.blit(reset_text, (reset_button.x + (BUTTON_WIDTH - reset_text.get_width()) // 2, reset_button.y + (BUTTON_HEIGHT - reset_text.get_height()) // 2))

    # Draw the collide button
    collide_button = pygame.Rect(WIDTH - BUTTON_WIDTH - 20, HEIGHT - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT)  # Bottom right corner
    pygame.draw.rect(screen, BLACK, collide_button)
    collide_text = font.render("Collide", True, WHITE)
    screen.blit(collide_text, (collide_button.x + (BUTTON_WIDTH - collide_text.get_width()) // 2, collide_button.y + (BUTTON_HEIGHT - collide_text.get_height()) // 2))

    # Draw the results 
    if exploded:
        result_text = [
            f"Time: {time:.6f} hrs",
            f"Distance1: {distance1:.6f} miles",
            f"Distance2: {distance2:.6f} miles"
        ]
        for i, line in enumerate(result_text):
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (20, 20 + i * (FONT_SIZE + 5)))  # Adjust vertical position

    # Start moving objects when spacebar is pressed or collide button is clicked
    if start and not exploded:
        x1 += speed1
        x2 -= speed2
        if x1 + radius >= x2 - radius:  # When the objects meet
            exploded = True

            # Generate explosion particles
            for _ in range(EXPLOSION_PARTICLES):
                particle = {
                    'x': (x1 + x2) // 2,
                    'y': y1,
                    'vx': random.uniform(-5, 5),
                    'vy': random.uniform(-5, 5),
                    'radius': random.uniform(2, 5),
                    'color': random.choice([RED, BLUE])
                }
                explosion_particles.append(particle)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or (event.key == pygame.K_RETURN and collide_button.collidepoint(pygame.mouse.get_pos())):
                start = True
            elif event.key == pygame.K_BACKSPACE:
                if active_box:
                    input_texts[active_box] = input_texts[active_box][:-1]
            elif event.key == pygame.K_TAB:
                if active_box == 'total_distance':
                    active_box = 'rate1'
                elif active_box == 'rate1':
                    active_box = 'rate2'
                else:
                    active_box = 'total_distance'
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                try:
                    total_distance = float(input_texts['total_distance'])
                    rate1 = float(input_texts['rate1'])
                    rate2 = float(input_texts['rate2'])
                    time, distance1, distance2 = calculate_collision_time(total_distance, rate1, rate2)
                    speed1 = (distance1 / total_distance) * total_distance_pixels / (time * FPS)
                    speed2 = (distance2 / total_distance) * total_distance_pixels / (time * FPS)
                    exploded = False  # Reset explosion state
                except ValueError:
                    pass
            elif event.key == pygame.K_0:
                if active_box:
                    input_texts[active_box] += event.unicode
            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_PERIOD):
                if active_box:
                    input_texts[active_box] += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if reset_button.collidepoint(mouse_pos):
                time, distance1, distance2, speed1, speed2 = reset_positions()
                start = False
                exploded = False
            elif collide_button.collidepoint(mouse_pos):
                start = True
                try:
                    total_distance = float(input_texts['total_distance'])
                    rate1 = float(input_texts['rate1'])
                    rate2 = float(input_texts['rate2'])
                    time, distance1, distance2 = calculate_collision_time(total_distance, rate1, rate2)
                    speed1 = (distance1 / total_distance) * total_distance_pixels / (time * FPS)
                    speed2 = (distance2 / total_distance) * total_distance_pixels / (time * FPS)
                    exploded = False  # Reset explosion state
                except ValueError:
                    pass
            else:
                for key, rect in input_boxes.items():
                    if rect.collidepoint(mouse_pos):
                        active_box = key
                    else:
                        if key == active_box and event.type == pygame.MOUSEBUTTONDOWN:
                            active_box = None

    # Handle cursor blink
    current_time = pygame.time.get_ticks()
    if current_time - last_blink_time >= BLINK_RATE:
        last_blink_time = current_time

    pygame.display.flip()
    clock.tick(FPS)
#---------------------------------------------------------------------------------------------
pygame.quit()
sys.exit()
#End