"""
🐍 Snake Game - Christmas Edition 🎄
A festive two-player snake game with Christmas decorations, multiple themes, and dynamic difficulty.

Features:
- Single player and two-player modes
- 5 customizable color themes
- Progressive difficulty (levels increase speed and add obstacles)
- Golden food for bonus points
- Lives system with visual hearts
- Animated Christmas tree decorations with twinkling lights
- Pause and restart functionality

Controls:
- Player 1: WASD keys
- Player 2: Arrow keys
- Space: Start game
- P: Pause/Unpause
- R: Return to menu (after game over)
- 1-5: Select theme or game mode
"""

import turtle
import time
import random


# Scor
delay = 0.1          # Delay pentru frame-urile sarpelui
score = 0            # Jucatorul 1 - scor
high_score = 0       # Cel mai mare scor pentru 1-player mode
score_p2 = 0         # Jucatorul 1 - scor

# Statutul jocului
game_state = "menu"  # "menu", "start", "playing", "paused", or "game_over"
game_mode = None     # "1player" or "2player"

# Vieti si levelul-dificultatea
lives = 3            # Vieti ramase player 1
lives_p2 = 3         # Vieti ramase player 2
level = 1            # Level curent

# Mancare de aur - pt 50 pct
golden_food_active = False  # True/False daca este pe harta sau nu
golden_food_timer = 0       # Mancarea de aur ramane pe harta doar pt cateva secunde

# Luminile pentru bradul de Craciun
lights = []          # Lista luminilor
light_timer = 0      # Timer pentru culori

# culorile
# Culoarea selectata de user
selected_theme = 0

# Culori pentru personalizarea serpilor
# Culori pentru ambii jucatori
color_themes = [
    {"name": "Christmas", "p1": "#39ff14", "p1_body": "#2bff00", "p2": "#00d9ff", "p2_body": "#00a8cc"},
    {"name": "Fire & Ice", "p1": "#FF4500", "p1_body": "#FF6347", "p2": "#00FFFF", "p2_body": "#4169E1"},
    {"name": "Neon", "p1": "#FF1493", "p1_body": "#FF69B4", "p2": "#00FF00", "p2_body": "#7FFF00"},
    {"name": "Royal", "p1": "#FFD700", "p1_body": "#FFA500", "p2": "#9400D3", "p2_body": "#8A2BE2"},
    {"name": "Sunset", "p1": "#FF6347", "p1_body": "#FF7F50", "p2": "#FFA500", "p2_body": "#FFB347"},
]


# setup
screen = turtle.Screen()
screen.title("🐍 Snake Game - Christmas Edition 🎄")
screen.bgcolor("#0a0e27")  # Background
screen.setup(width=1000, height=800)  # Mai mare putin sa incapa brazii de Craciun
screen.tracer(0)  


# bradul de craciun
def create_christmas_tree(x_offset, y_offset):
    """
    Deseneaza un brad de Craciun la anumite pozitii.
    
    Args:
        x_offset: Pozitia orizontala a centrului bradului
        y_offset: Pozitia verticala a centrului bradului
        
    Returns:
        List(x,y) - Pozitiile unde pot fi luminitile
    """
    tree = turtle.Turtle()
    tree.speed(0)
    tree.hideturtle()
    tree.penup()
    
    # Baza bradului
    tree.goto(x_offset, y_offset - 160)
    tree.color("#8B4513")
    tree.begin_fill()
    tree.goto(x_offset - 20, y_offset - 160)
    tree.goto(x_offset - 20, y_offset - 100)
    tree.goto(x_offset + 20, y_offset - 100)
    tree.goto(x_offset + 20, y_offset - 160)
    tree.end_fill()
    
    # Vom desena 3 triunghiuri verzi peste baza maro
    tree.color("#0a5f0a") 
    
    # Primul layer
    tree.goto(x_offset, y_offset - 40)
    tree.begin_fill()
    tree.goto(x_offset - 80, y_offset - 100)
    tree.goto(x_offset + 80, y_offset - 100)
    tree.goto(x_offset, y_offset - 40)
    tree.end_fill()
    
    # Al doilea layer
    tree.goto(x_offset, y_offset + 30)
    tree.begin_fill()
    tree.goto(x_offset - 65, y_offset - 40)
    tree.goto(x_offset + 65, y_offset - 40)
    tree.goto(x_offset, y_offset + 30)
    tree.end_fill()
    
    # Al treilea layer - cel mai mic
    tree.goto(x_offset, y_offset + 100)
    tree.begin_fill()
    tree.goto(x_offset - 50, y_offset + 30)
    tree.goto(x_offset + 50, y_offset + 30)
    tree.goto(x_offset, y_offset + 100)
    tree.end_fill()
    
    # Stea de aur
    tree.goto(x_offset, y_offset + 115)
    tree.color("#FFD700")
    tree.dot(25)
    
    # Luminitile puse simetric
    ornament_positions = [
        (x_offset - 50, y_offset - 88),
        (x_offset - 25, y_offset - 88),
        (x_offset, y_offset - 88),
        (x_offset + 25, y_offset - 88),
        (x_offset + 50, y_offset - 88),
        
        (x_offset - 35, y_offset - 70),
        (x_offset, y_offset - 70),
        (x_offset + 35, y_offset - 70),
        
        (x_offset - 18, y_offset - 52),
        (x_offset + 18, y_offset - 52),
        
        (x_offset - 40, y_offset - 25),
        (x_offset - 20, y_offset - 25),
        (x_offset, y_offset - 25),
        (x_offset + 20, y_offset - 25),
        (x_offset + 40, y_offset - 25),
        
        (x_offset - 22, y_offset + 3),
        (x_offset, y_offset + 8),
        (x_offset + 22, y_offset + 3),
        
        (x_offset - 28, y_offset + 45),
        (x_offset, y_offset + 45),
        (x_offset + 28, y_offset + 45),

        (x_offset - 15, y_offset + 70),
        (x_offset + 15, y_offset + 70),
    ]
    
    return ornament_positions

def create_light(x, y, color, light_index):
    light = turtle.Turtle()
    light.speed(0)
    light.shape("circle")
    light.shapesize(0.6, 0.6) 
    light.penup()
    light.goto(x, y)
    light.color(color)
    light.base_color = color 
    light.light_index = light_index
    light.color_sequence_index = 0 
    return light

def update_lights():
    """
    Coloram luminile circular intr-un vector. Initial, am facut sa fie random. Problema a fost ca jocul avea mult lag.
    """
    global light_timer
    light_timer += 1
    
    if light_timer % 6 == 0:
        for light in lights:
            light.color_sequence_index = (light.color_sequence_index + 1) % len(light.color_sequence)
            new_color = light.color_sequence[light.color_sequence_index]
            light.color(new_color)

border = turtle.Turtle()
border.speed(0)
border.color("#00d9ff")  # Cyan
border.penup()
border.hideturtle()
border.goto(-340, 300)
border.pendown()
border.pensize(4)
for _ in range(4):
    border.forward(680)
    border.right(90)
border.penup()

border.goto(-330, 290)
border.pensize(1)
border.color("#1e3a5f")
for _ in range(4):
    border.forward(660)
    border.right(90)
border.penup()

# Creeaza cei 2 brazi de Craciun in stanga si dreapta
left_tree_positions = create_christmas_tree(-450, 0)
right_tree_positions = create_christmas_tree(450, 0)

# Define color sequences for light animation
# Each light cycles through these colors to create variety
color_sequences = [
    ["#FF0000", "#FFD700", "#0000FF", "#00FF00", "#FF00FF"],  # Red, Gold, Blue, Green, Magenta
    ["#FFD700", "#0000FF", "#00FF00", "#FF00FF", "#FF0000"],  # Gold, Blue, Green, Magenta, Red
    ["#0000FF", "#00FF00", "#FF00FF", "#FF0000", "#FFD700"],  # Blue, Green, Magenta, Red, Gold
    ["#00FF00", "#FF00FF", "#FF0000", "#FFD700", "#0000FF"],  # Green, Magenta, Red, Gold, Blue
    ["#FF00FF", "#FF0000", "#FFD700", "#0000FF", "#00FF00"],  # Magenta, Red, Gold, Blue, Green
]

# Create all ornament lights with unique starting colors and sequences
lights = []
light_index = 0

# Create lights for left tree
for pos in left_tree_positions:
    color = color_sequences[light_index % 5][0]  # Start with first color in sequence
    light = create_light(pos[0], pos[1], color, light_index)
    light.color_sequence = color_sequences[light_index % 5]  # Assign color cycle
    lights.append(light)
    light_index += 1

# Create lights for right tree (offset sequence for variety)
for pos in right_tree_positions:
    color = color_sequences[light_index % 5][2]  # Start with third color for variation
    light = create_light(pos[0], pos[1], color, light_index)
    light.color_sequence = color_sequences[light_index % 5]
    lights.append(light)
    light_index += 1


# player 1
# Player 1 snake head (circular)
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.shapesize(1.4, 1.4)  # Larger than body segments
head.color("#39ff14")  # Bright green (default theme)
head.penup()
head.goto(1000, 1000)  # Start off-screen
head.direction = "stop"  # Current movement direction

# Player 1 eyes (two white dots for visual appeal)
eye1_p1 = turtle.Turtle()
eye1_p1.speed(0)
eye1_p1.shape("circle")
eye1_p1.shapesize(0.3, 0.3)  # Small dots
eye1_p1.color("white")
eye1_p1.penup()
eye1_p1.goto(1000, 1000)  # Start off-screen

eye2_p1 = turtle.Turtle()
eye2_p1.speed(0)
eye2_p1.shape("circle")
eye2_p1.shapesize(0.3, 0.3)
eye2_p1.color("white")
eye2_p1.penup()
eye2_p1.goto(1000, 1000)

# Player 1 body segments (added dynamically during gameplay)
segments = []


# player 2
# Player 2 snake head (cyan colored to differentiate from P1)
head_p2 = turtle.Turtle()
head_p2.speed(0)
head_p2.shape("circle")
head_p2.shapesize(1.4, 1.4)
head_p2.color("#00d9ff")  # Cyan (default theme)
head_p2.penup()
head_p2.goto(1000, 1000)
head_p2.direction = "stop"

# Player 2 eyes
eye1_p2 = turtle.Turtle()
eye1_p2.speed(0)
eye1_p2.shape("circle")
eye1_p2.shapesize(0.3, 0.3)
eye1_p2.color("white")
eye1_p2.penup()
eye1_p2.goto(1000, 1000)

eye2_p2 = turtle.Turtle()
eye2_p2.speed(0)
eye2_p2.shape("circle")
eye2_p2.shapesize(0.3, 0.3)
eye2_p2.color("white")
eye2_p2.penup()
eye2_p2.goto(1000, 1000)

# Player 2 body segments
segments_p2 = []


# food
# Regular food (pink circles worth 10 points)
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.shapesize(1.3, 1.3)
food.color("#ff006e")  # Pink
food.penup()
food.goto(1000, 1000)

# Second food item (for 2-player mode to increase food availability)
food2 = turtle.Turtle()
food2.speed(0)
food2.shape("circle")
food2.shapesize(1.3, 1.3)
food2.color("#ff006e")
food2.penup()
food2.goto(1000, 1000)

# Special golden food (worth 50 points, appears randomly and temporarily)
golden_food = turtle.Turtle()
golden_food.speed(0)
golden_food.shape("circle")
golden_food.shapesize(1.5, 1.5)  # Slightly larger than regular food
golden_food.color("#ffd700")  # Gold
golden_food.penup()
golden_food.goto(1000, 1000)


# OBSTACOLE
# List to store obstacle objects (red squares that cause death on collision)
obstacles = []


# DISPLAY ELEM

# Score display (center top) - shows score and high score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("#00d9ff")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(0, 320)

# Player 2 score display (used in 2-player mode)
score_pen_p2 = turtle.Turtle()
score_pen_p2.speed(0)
score_pen_p2.color("#00d9ff")
score_pen_p2.penup()
score_pen_p2.hideturtle()
score_pen_p2.goto(0, 340)

# Lives display (left side) - shows hearts for remaining lives
lives_pen = turtle.Turtle()
lives_pen.speed(0)
lives_pen.color("#ff006e")
lives_pen.penup()
lives_pen.hideturtle()
lives_pen.goto(-350, 320)

# Level display (right side) - shows current difficulty level
level_pen = turtle.Turtle()
level_pen.speed(0)
level_pen.color("#ffd700")
level_pen.penup()
level_pen.hideturtle()
level_pen.goto(250, 320)

# Info display below game border - shows controls and point values
info_pen = turtle.Turtle()
info_pen.speed(0)
info_pen.color("#ff006e")
info_pen.penup()
info_pen.hideturtle()
info_pen.goto(0, -345)

# Title display (used in menus)
title = turtle.Turtle()
title.speed(0)
title.color("#39ff14")
title.penup()
title.hideturtle()
title.goto(0, 140)

# Message display (used for various text messages)
message = turtle.Turtle()
message.speed(0)
message.color("white")
message.penup()
message.hideturtle()
message.goto(0, 30)

# Instructions display (gray text for less prominent info)
instructions = turtle.Turtle()
instructions.speed(0)
instructions.color("#8b949e")
instructions.penup()
instructions.hideturtle()
instructions.goto(0, -80)

# Countdown display (large numbers before game starts: 3, 2, 1, GO!)
countdown_display = turtle.Turtle()
countdown_display.speed(0)
countdown_display.color("#FFD700")
countdown_display.penup()
countdown_display.hideturtle()
countdown_display.goto(0, 0)


# UPDATE FUNCTIONS
def update_score_display():
    """
    Update the score, lives, and level displays based on current game mode.
    Displays differently for single-player vs two-player modes.
    """
    if game_mode == "2player":
        # Two player mode - show both players' scores and lives
        score_pen.clear()
        score_pen.goto(0, 340)
        score_pen.write(f"P1: {score} | Lives: {'❤️' * lives}", 
                        align="center", font=("Arial", 14, "bold"))
        
        score_pen_p2.clear()
        score_pen_p2.goto(0, 320)
        score_pen_p2.write(f"P2: {score_p2} | Lives: {'❤️' * lives_p2}", 
                          align="center", font=("Arial", 14, "bold"))
        
        lives_pen.clear()  # Hide single player lives display
        level_pen.clear()
        level_pen.goto(250, 340)
        level_pen.write(f"Level: {level}", 
                       align="right", font=("Arial", 14, "bold"))
    else:
        # Single player mode - original display format
        score_pen.clear()
        score_pen.goto(0, 320)
        score_pen.write(f"Score: {score}  High: {high_score}", 
                        align="center", font=("Arial", 16, "bold"))
        
        lives_pen.clear()
        lives_pen.write(f"Lives: {'❤️ ' * lives}", 
                        align="left", font=("Arial", 14, "bold"))
        
        level_pen.clear()
        level_pen.goto(250, 320)
        level_pen.write(f"Level: {level}", 
                        align="right", font=("Arial", 14, "bold"))
        
        score_pen_p2.clear()  # Hide player 2 score
    
    # Always show control info below border during gameplay
    if game_state == "playing":
        info_pen.clear()
        info_pen.write("🔴 Red = 10 pts  |  🟡 Golden = 50 pts  |  ❤️3 Lives  |  P: Pause  |  R: Restart", 
                      align="center", font=("Arial", 13, "bold"))

# ============================================================================
# SCREEN DISPLAY FUNCTIONS
# ============================================================================

def show_menu():
    """
    Display the main menu where players choose between 1-player or 2-player mode.
    """
    # Clear all previous text
    title.clear()
    message.clear()
    instructions.clear()
    info_pen.clear()
    
    # Hide snakes and eyes off-screen
    head.goto(1000, 1000)
    head_p2.goto(1000, 1000)
    eye1_p1.goto(1000, 1000)
    eye2_p1.goto(1000, 1000)
    eye1_p2.goto(1000, 1000)
    eye2_p2.goto(1000, 1000)
    
    # Display Christmas-themed title
    title.goto(0, 140)
    title.color("#FF0000")
    title.write("🎄 SNAKE GAME 🎄", align="center", font=("Arial", 52, "bold"))
    
    # Display subtitle
    message.goto(0, 70)
    message.color("#00d9ff")
    message.write("Christmas Edition", align="center", font=("Arial", 20, "italic"))
    
    # Display game mode options
    message.goto(0, 10)
    message.color("#39ff14")
    message.write("Press 1 for Single Player", align="center", font=("Arial", 24, "bold"))
    
    instructions.goto(0, -40)
    instructions.color("#FFD700")
    instructions.write("Press 2 for Two Players", align="center", font=("Arial", 24, "bold"))
    
    # Show control info below border
    info_pen.goto(0, -345)
    info_pen.color("#ff006e")
    info_pen.write("P1: WASD  |  P2: Arrow Keys  |  🔴 Red = 10 pts  |  🟡 Golden = 50 pts", 
                  align="center", font=("Arial", 13, "bold"))

def show_start_screen():
    """
    Display the start screen where players can customize their snake colors
    before starting the game.
    """
    # Clear all previous displays
    title.clear()
    message.clear()
    instructions.clear()
    info_pen.clear()
    countdown_display.clear()
    
    # Hide snakes and eyes
    head.goto(1000, 1000)
    head_p2.goto(1000, 1000)
    eye1_p1.goto(1000, 1000)
    eye2_p1.goto(1000, 1000)
    eye1_p2.goto(1000, 1000)
    eye2_p2.goto(1000, 1000)
    
    # Display title
    title.goto(0, 180)
    title.color("#FF0000")
    title.write("🎄 SNAKE GAME 🎄", align="center", font=("Arial", 52, "bold"))
    
    # Display subtitle
    message.goto(0, 120)
    message.color("#00d9ff")
    message.write("Christmas Edition", align="center", font=("Arial", 20, "italic"))
    
    # Show current color theme selection
    message.goto(0, 70)
    message.color("#FFD700")
    message.write(f"Color Theme: {color_themes[selected_theme]['name']}", 
                  align="center", font=("Arial", 20, "bold"))
    
    # Show theme change instructions
    message.goto(0, 40)
    message.color("#8b949e")
    message.write("Press 1-5 to change theme", align="center", font=("Arial", 14, "normal"))
    
    # Show movement controls
    message.goto(0, 10)
    message.color("#00d9ff")
    if game_mode == "1player":
        message.write("Use WASD to move", align="center", font=("Arial", 16, "normal"))
    else:
        message.write("P1: WASD  |  P2: Arrow Keys", align="center", font=("Arial", 16, "normal"))
    
    # Show start instruction
    instructions.goto(0, -30)
    instructions.color("#FFD700")
    instructions.write("Press SPACE to Start", align="center", font=("Arial", 28, "bold"))
    
    # Show preview of snake colors
    preview_y = -80
    if game_mode == "2player":
        # Show both players' snake colors
        message.goto(-100, preview_y)
        message.color(color_themes[selected_theme]['p1'])
        message.write("P1 ●", align="center", font=("Arial", 24, "bold"))
        
        message.goto(100, preview_y)
        message.color(color_themes[selected_theme]['p2'])
        message.write("P2 ●", align="center", font=("Arial", 24, "bold"))
    else:
        # Show single player snake color
        message.goto(0, preview_y)
        message.color(color_themes[selected_theme]['p1'])
        message.write("Your Snake ●", align="center", font=("Arial", 24, "bold"))
    
    # Show info below border
    info_pen.goto(0, -345)
    info_pen.color("#ff006e")
    info_pen.write("🔴 Red = 10 pts  |  🟡 Golden = 50 pts  |  ❤️3 Lives  |  P: Pause  |  R: Restart", 
                  align="center", font=("Arial", 13, "bold"))

def show_pause_screen():
    """
    Display the pause screen overlay when player pauses the game.
    """
    message.goto(0, 0)
    message.clear()
    message.color("#00d9ff")
    message.write("⏸  PAUSED\n\nPress P to Continue", 
                  align="center", font=("Arial", 36, "bold"))

def show_game_over_screen():
    """
    Display the game over screen showing final scores and winner (if 2-player).
    """
    info_pen.clear()
    
    # Display "GAME OVER" title
    title.goto(0, 170)
    title.clear()
    title.color("#ff006e")
    title.write("GAME OVER!", align="center", font=("Arial", 48, "bold"))
    
    message.goto(0, 80)
    message.clear()
    message.color("#39ff14")
    
    # Display results based on game mode
    if game_mode == "2player":
        # Determine winner based on final scores
        if score > score_p2:
            message.write(f"Player 1 WINS!\nP1 Score: {score}  |  P2 Score: {score_p2}\nLevel: {level}", 
                          align="center", font=("Arial", 24, "bold"))
        elif score_p2 > score:
            message.write(f"Player 2 WINS!\nP1 Score: {score}  |  P2 Score: {score_p2}\nLevel: {level}", 
                          align="center", font=("Arial", 24, "bold"))
        else:
            message.write(f"TIE GAME!\nP1 Score: {score}  |  P2 Score: {score_p2}\nLevel: {level}", 
                          align="center", font=("Arial", 24, "bold"))
    else:
        # Single player - show final score and level
        message.write(f"Final Score: {score}\nLevel Reached: {level}", 
                      align="center", font=("Arial", 28, "bold"))
    
    # Show restart instructions and high score message if applicable
    instructions.goto(0, -20)
    instructions.clear()
    if game_mode != "2player" and score > high_score:
        instructions.color("#ffd700")
        instructions.write("🏆 NEW HIGH SCORE! 🏆\n\nPress R to Return to Menu", 
                          align="center", font=("Arial", 22, "bold"))
    else:
        instructions.color("white")
        instructions.write("Press R to Return to Menu", 
                          align="center", font=("Arial", 22, "normal"))

def show_countdown():
    """
    Display a 3-2-1-GO countdown sequence before the game starts.
    Also initializes snake positions and spawns food.
    """
    global game_state
    
    # Clear previous screens
    title.clear()
    message.clear()
    instructions.clear()
    
    # Apply selected color theme to both snakes
    theme = color_themes[selected_theme]
    head.color(theme['p1'])
    head_p2.color(theme['p2'])
    
    if game_mode == "2player":
        # Position both snakes (left and right)
        head.goto(-100, 0)
        head_p2.goto(100, 0)
        # Show eyes for both snakes
        eye1_p1.goto(-105, 5)
        eye2_p1.goto(-95, 5)
        eye1_p2.goto(95, 5)
        eye2_p2.goto(105, 5)
        # Spawn 2 food items for 2-player mode
        x = random.randint(-300, 300)
        y = random.randint(-240, 240)
        food.goto(x, y)
        x2 = random.randint(-300, 300)
        y2 = random.randint(-240, 240)
        food2.goto(x2, y2)
    else:
        # Position single snake in center
        head.goto(0, 0)
        head_p2.goto(1000, 1000)  # Hide P2 snake
        # Show P1 eyes only
        eye1_p1.goto(-5, 5)
        eye2_p1.goto(5, 5)
        # Hide P2 eyes
        eye1_p2.goto(1000, 1000)
        eye2_p2.goto(1000, 1000)
        # Spawn 1 food for single player
        x = random.randint(-300, 300)
        y = random.randint(-240, 240)
        food.goto(x, y)
        food2.goto(1000, 1000)  # Hide second food
    
    # Update score display and create obstacles
    update_score_display()
    create_obstacles()
    
    # Display countdown: 3, 2, 1
    for count in [3, 2, 1]:
        countdown_display.clear()
        countdown_display.goto(0, 0)
        countdown_display.color("#FFD700")
        countdown_display.write(str(count), align="center", font=("Arial", 100, "bold"))
        screen.update()
        time.sleep(0.8)
    
    # Display "GO!" message
    countdown_display.clear()
    countdown_display.goto(0, 0)
    countdown_display.color("#00FF00")
    countdown_display.write("GO!", align="center", font=("Arial", 100, "bold"))
    screen.update()
    time.sleep(0.5)
    countdown_display.clear()
    
    # Start the game
    game_state = "playing"

# ============================================================================
# GAME MECHANICS FUNCTIONS
# ============================================================================

def spawn_golden_food():
    """
    Randomly spawn golden food (20% chance when called).
    Golden food gives 50 points and disappears after a timer expires.
    """
    global golden_food_active, golden_food_timer
    if not golden_food_active and random.randint(1, 5) == 1:  # 20% chance
        golden_food_active = True
        golden_food_timer = 100  # Frames before it disappears
        x = random.randint(-300, 300)
        y = random.randint(-260, 260)
        golden_food.goto(x, y)

def create_obstacles():
    """
    Create red obstacle squares based on current level.
    Number of obstacles increases with level (1 per level, max 8).
    Obstacles cause instant death on collision.
    """
    # Remove old obstacles
    for obstacle in obstacles:
        obstacle.hideturtle()
    obstacles.clear()
    
    # Create new obstacles based on level (1 obstacle per level, max 8)
    num_obstacles = min(level, 8)
    for _ in range(num_obstacles):
        obstacle = turtle.Turtle()
        obstacle.speed(0)
        obstacle.shape("square")
        obstacle.color("#ff3333")  # Red
        obstacle.penup()
        # Random position within play area
        x = random.randint(-300, 300)
        y = random.randint(-240, 240)
        obstacle.goto(x, y)
        obstacles.append(obstacle)

def check_level_up():
    """
    Check if player(s) have earned enough points to advance to next level.
    Increases speed and creates new obstacles when leveling up.
    """
    global level, delay
    
    if game_mode == "2player":
        # Combined score for 2-player mode
        combined_score = score + score_p2
        new_level = (combined_score // 50) + 1  # Level up every 50 combined points
    else:
        new_level = (score // 30) + 1  # Level up every 30 points for single player
    
    # If level increased, update speed and obstacles
    if new_level > level:
        level = new_level
        # Decrease delay (increase speed), with minimum of 0.05
        delay = max(0.05, 0.1 - (level - 1) * 0.015)
        update_score_display()
        create_obstacles()

# def reset_after_death():
#     """
#     Reset snake positions and clear segments after a death.
#     Only resets snakes that still have lives remaining.
#     """
#     global delay, golden_food_active, golden_food_timer
    
#     # Reset based on game mode and remaining lives
#     if game_mode == "2player":
#         # Reset P1 if they have lives
#         if lives > 0:
#             head.goto(-100, 0)
#             head.direction = "stop"
#             for segment in segments:
#                 segment.hideturtle()
#             segments.clear()
        
#         # Reset P2 if they have lives
#         if lives_p2 > 0:
#             head_p2.goto(100, 0)
#             head_p2.direction = "stop"
#             for segment in segments_p2:
#                 segment.hideturtle()
#             segments_p2.clear()
#     else:
#         # Single player reset
#         head.goto(0, 0)
#         head.direction = "stop"
#         for segment in segments:
#             segment.hideturtle()
#         segments.clear()
    
#     # Remove golden food
#     golden_food_active = False
#     golden_food_timer = 0
#     golden_food.goto(1000, 1000)
    
#     # Reset speed based on level
#     delay = max(0.05, 0.1 - (level - 1) * 0.015)

def game_over():
    """
    End the game and display final results.
    Updates high score if needed and shows game over screen.
    """
    global game_state, high_score
    
    game_state = "game_over"
    
    # Hide snakes, eyes, food, and obstacles off-screen
    head.goto(1000, 1000)
    head_p2.goto(1000, 1000)
    eye1_p1.goto(1000, 1000)
    eye2_p1.goto(1000, 1000)
    eye1_p2.goto(1000, 1000)
    eye2_p2.goto(1000, 1000)
    
    food.goto(1000, 1000)
    food2.goto(1000, 1000)
    golden_food.goto(1000, 1000)
    
    for segment in segments:
        segment.goto(1000, 1000)
    
    for segment in segments_p2:
        segment.goto(1000, 1000)
    
    for obstacle in obstacles:
        obstacle.goto(1000, 1000)
    
    # Update high score if current score is higher (single player only)
    if score > high_score:
        high_score = score
    
    update_score_display()
    show_game_over_screen()

# ============================================================================
# PLAYER MOVEMENT FUNCTIONS
# ============================================================================

# Player 1 movement (WASD keys)
def go_up():
    """Change P1 snake direction to up (prevents 180-degree turns)."""
    if head.direction != "down" and game_state == "playing":
        head.direction = "up"

def go_down():
    """Change P1 snake direction to down (prevents 180-degree turns)."""
    if head.direction != "up" and game_state == "playing":
        head.direction = "down"

def go_left():
    """Change P1 snake direction to left (prevents 180-degree turns)."""
    if head.direction != "right" and game_state == "playing":
        head.direction = "left"

def go_right():
    """Change P1 snake direction to right (prevents 180-degree turns)."""
    if head.direction != "left" and game_state == "playing":
        head.direction = "right"

# Player 2 movement (Arrow keys)
def go_up_p2():
    """Change P2 snake direction to up (prevents 180-degree turns)."""
    if head_p2.direction != "down" and game_state == "playing" and game_mode == "2player":
        head_p2.direction = "up"

def go_down_p2():
    """Change P2 snake direction to down (prevents 180-degree turns)."""
    if head_p2.direction != "up" and game_state == "playing" and game_mode == "2player":
        head_p2.direction = "down"

def go_left_p2():
    """Change P2 snake direction to left (prevents 180-degree turns)."""
    if head_p2.direction != "right" and game_state == "playing" and game_mode == "2player":
        head_p2.direction = "left"

def go_right_p2():
    """Change P2 snake direction to right (prevents 180-degree turns)."""
    if head_p2.direction != "left" and game_state == "playing" and game_mode == "2player":
        head_p2.direction = "right"

def move():
    """
    Move Player 1 snake head in current direction and update eye positions.
    Eyes are positioned relative to head to indicate facing direction.
    """
    if head.direction == "up":
        head.sety(head.ycor() + 20)
        # Position eyes for upward facing
        eye1_p1.goto(head.xcor() - 5, head.ycor() + 5)
        eye2_p1.goto(head.xcor() + 5, head.ycor() + 5)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
        # Position eyes for downward facing
        eye1_p1.goto(head.xcor() - 5, head.ycor() - 5)
        eye2_p1.goto(head.xcor() + 5, head.ycor() - 5)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
        # Position eyes for left facing
        eye1_p1.goto(head.xcor() - 5, head.ycor() + 5)
        eye2_p1.goto(head.xcor() - 5, head.ycor() - 5)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)
        # Position eyes for right facing
        eye1_p1.goto(head.xcor() + 5, head.ycor() + 5)
        eye2_p1.goto(head.xcor() + 5, head.ycor() - 5)

def move_p2():
    """
    Move Player 2 snake head in current direction and update eye positions.
    Eyes are positioned relative to head to indicate facing direction.
    """
    if head_p2.direction == "up":
        head_p2.sety(head_p2.ycor() + 20)
        # Position eyes for upward facing
        eye1_p2.goto(head_p2.xcor() - 5, head_p2.ycor() + 5)
        eye2_p2.goto(head_p2.xcor() + 5, head_p2.ycor() + 5)
    elif head_p2.direction == "down":
        head_p2.sety(head_p2.ycor() - 20)
        # Position eyes for downward facing
        eye1_p2.goto(head_p2.xcor() - 5, head_p2.ycor() - 5)
        eye2_p2.goto(head_p2.xcor() + 5, head_p2.ycor() - 5)
    elif head_p2.direction == "left":
        head_p2.setx(head_p2.xcor() - 20)
        # Position eyes for left facing
        eye1_p2.goto(head_p2.xcor() - 5, head_p2.ycor() + 5)
        eye2_p2.goto(head_p2.xcor() - 5, head_p2.ycor() - 5)
    elif head_p2.direction == "right":
        head_p2.setx(head_p2.xcor() + 20)
        # Position eyes for right facing
        eye1_p2.goto(head_p2.xcor() + 5, head_p2.ycor() + 5)
        eye2_p2.goto(head_p2.xcor() + 5, head_p2.ycor() - 5)

# ============================================================================
# GAME STATE CONTROL FUNCTIONS
# ============================================================================

def select_1player():
    """Select single-player mode from main menu."""
    global game_state, game_mode
    if game_state == "menu":
        game_mode = "1player"
        game_state = "start"
        show_start_screen()

def select_2player():
    """Select two-player mode from main menu."""
    global game_state, game_mode
    if game_state == "menu":
        game_mode = "2player"
        game_state = "start"
        show_start_screen()

def change_theme(theme_number):
    """
    Change the color theme for snakes.
    
    Args:
        theme_number: Theme number (1-5) to switch to
    """
    global selected_theme
    if game_state == "start":
        selected_theme = theme_number - 1  # Convert 1-5 to 0-4 (array index)
        show_start_screen()  # Refresh screen with new theme preview

def start_game():
    """
    Initialize a new game with starting values and show countdown.
    Called when player presses SPACE on start screen.
    """
    global game_state, lives, level, score, delay, lives_p2, score_p2
    if game_state == "start":
        # Reset all game variables to starting values
        lives = 3
        level = 1
        score = 0
        delay = 0.1
        
        if game_mode == "2player":
            lives_p2 = 3
            score_p2 = 0
        
        show_countdown()

def pause_game():
    """
    Toggle between playing and paused states.
    Called when player presses P key.
    """
    global game_state
    if game_state == "playing":
        game_state = "paused"
        show_pause_screen()
    elif game_state == "paused":
        game_state = "playing"
        message.clear()
        update_score_display()

def restart_game():
    """
    Return to main menu from game over screen.
    Resets all game variables and clears the screen.
    """
    global score, delay, game_state, lives, level, golden_food_active, golden_food_timer, game_mode, score_p2, lives_p2
    
    if game_state == "game_over":
        # Reset to menu state
        game_state = "menu"
        game_mode = None
        
        # Reset all game variables
        lives = 3
        level = 1
        score = 0
        score_p2 = 0
        lives_p2 = 3
        delay = 0.1
        golden_food_active = False
        golden_food_timer = 0
        
        # Hide all game objects off-screen
        head.goto(1000, 1000)
        head.direction = "stop"
        head_p2.goto(1000, 1000)
        head_p2.direction = "stop"
        
        # Clear all body segments
        for segment in segments:
            segment.hideturtle()
        segments.clear()
        
        for segment in segments_p2:
            segment.hideturtle()
        segments_p2.clear()
        
        # Hide food and obstacles
        food.goto(1000, 1000)
        food2.goto(1000, 1000)
        golden_food.goto(1000, 1000)
        
        for obstacle in obstacles:
            obstacle.hideturtle()
        obstacles.clear()
        
        # Clear all UI displays
        score_pen.clear()
        score_pen_p2.clear()
        lives_pen.clear()
        level_pen.clear()
        
        # Show main menu
        show_menu()

# ============================================================================
# KEYBOARD BINDINGS
# ============================================================================

screen.listen()

# Player 1 movement - WASD keys
screen.onkeypress(go_up, "w")
screen.onkeypress(go_down, "s")
screen.onkeypress(go_left, "a")
screen.onkeypress(go_right, "d")

# Player 2 movement - Arrow keys
screen.onkeypress(go_up_p2, "Up")
screen.onkeypress(go_down_p2, "Down")
screen.onkeypress(go_left_p2, "Left")
screen.onkeypress(go_right_p2, "Right")

# Game control keys
screen.onkeypress(start_game, "space")
screen.onkeypress(pause_game, "p")
screen.onkeypress(restart_game, "r")

# Dual-purpose key handlers (menu selection OR theme selection)
def handle_key_1():
    """Handle key '1' - select 1-player mode in menu OR change to theme 1."""
    if game_state == "menu":
        select_1player()
    elif game_state == "start":
        change_theme(1)

def handle_key_2():
    """Handle key '2' - select 2-player mode in menu OR change to theme 2."""
    if game_state == "menu":
        select_2player()
    elif game_state == "start":
        change_theme(2)

# Bind number keys
screen.onkeypress(handle_key_1, "1")
screen.onkeypress(handle_key_2, "2")
# Theme selection only (keys 3-5)
screen.onkeypress(lambda: change_theme(3), "3")
screen.onkeypress(lambda: change_theme(4), "4")
screen.onkeypress(lambda: change_theme(5), "5")

# ============================================================================
# INITIAL DISPLAY
# ============================================================================

# Show main menu on startup
show_menu()
screen.update()

# ============================================================================
# MAIN GAME LOOP
# ============================================================================

while True:
    # Always update Christmas tree lights for twinkling effect
    update_lights()
    
    # If not playing, just update screen and continue
    if game_state != "playing":
        screen.update()
        time.sleep(0.05)
        continue

    # ========================================================================
    # COLLISION DETECTION - PLAYER 1
    # ========================================================================
    
    # Only check P1 collisions if P1 has lives remaining
    if lives > 0:
        # Check for collision with border walls
        if head.xcor() > 320 or head.xcor() < -320 or head.ycor() > 280 or head.ycor() < -280:
            lives -= 1
            update_score_display()
            screen.update()
            
            if lives <= 0:
                if game_mode == "2player":
                    if lives_p2 <= 0:
                        # Both players out of lives - game over
                        game_over()
                    else:
                        # P1 is out, but P2 still playing - hide P1
                        head.goto(1000, 1000)
                        head.direction = "stop"
                        eye1_p1.goto(1000, 1000)
                        eye2_p1.goto(1000, 1000)
                        for segment in segments:
                            segment.goto(1000, 1000)
                else:
                    # Single player - game over
                    game_over()
            else:
                # P1 still has lives - respawn P1
                head.goto(-100 if game_mode == "2player" else 0, 0)
                head.direction = "stop"
                # Reset eyes to spawn position
                if game_mode == "2player":
                    eye1_p1.goto(-105, 5)
                    eye2_p1.goto(-95, 5)
                else:
                    eye1_p1.goto(-5, 5)
                    eye2_p1.goto(5, 5)
                for segment in segments:
                    segment.hideturtle()
                segments.clear()
            continue

        # Check collision with obstacles (P1)
        hit_obstacle = False
        for obstacle in obstacles:
            if head.distance(obstacle) < 20:
                hit_obstacle = True
                break
        
        if hit_obstacle:
            lives -= 1
            update_score_display()
            screen.update()
            
            if lives <= 0:
                if game_mode == "2player":
                    if lives_p2 <= 0:
                        # Both players out - game over
                        game_over()
                    else:
                        # P1 is out, P2 continues - hide P1
                        head.goto(1000, 1000)
                        head.direction = "stop"
                        eye1_p1.goto(1000, 1000)
                        eye2_p1.goto(1000, 1000)
                        for segment in segments:
                            segment.goto(1000, 1000)
                else:
                    game_over()
            else:
                # P1 still has lives - respawn P1
                head.goto(-100 if game_mode == "2player" else 0, 0)
                head.direction = "stop"
                # Reset eyes
                if game_mode == "2player":
                    eye1_p1.goto(-105, 5)
                    eye2_p1.goto(-95, 5)
                else:
                    eye1_p1.goto(-5, 5)
                    eye2_p1.goto(5, 5)
                for segment in segments:
                    segment.hideturtle()
                segments.clear()
            continue

    # ========================================================================
    # COLLISION DETECTION - PLAYER 2 (only in 2-player mode)
    # ========================================================================
    
    if game_mode == "2player" and lives_p2 > 0:
        # Check for collision with border walls (P2)
        if head_p2.xcor() > 320 or head_p2.xcor() < -320 or head_p2.ycor() > 280 or head_p2.ycor() < -280:
            lives_p2 -= 1
            update_score_display()
            screen.update()
            
            if lives_p2 <= 0:
                if lives <= 0:
                    # Both players out - game over
                    game_over()
                else:
                    # P2 is out, P1 continues - hide P2
                    head_p2.goto(1000, 1000)
                    head_p2.direction = "stop"
                    eye1_p2.goto(1000, 1000)
                    eye2_p2.goto(1000, 1000)
                    for segment in segments_p2:
                        segment.goto(1000, 1000)
            else:
                # P2 still has lives - respawn P2
                head_p2.goto(100, 0)
                head_p2.direction = "stop"
                # Reset eyes
                eye1_p2.goto(95, 5)
                eye2_p2.goto(105, 5)
                for segment in segments_p2:
                    segment.hideturtle()
                segments_p2.clear()
            continue

        # Check collision with obstacles (P2)
        hit_obstacle_p2 = False
        for obstacle in obstacles:
            if head_p2.distance(obstacle) < 20:
                hit_obstacle_p2 = True
                break
        
        if hit_obstacle_p2:
            lives_p2 -= 1
            update_score_display()
            screen.update()
            
            if lives_p2 <= 0:
                if lives <= 0:
                    # Both players out - game over
                    game_over()
                else:
                    # P2 is out, P1 continues - hide P2
                    head_p2.goto(1000, 1000)
                    head_p2.direction = "stop"
                    eye1_p2.goto(1000, 1000)
                    eye2_p2.goto(1000, 1000)
                    for segment in segments_p2:
                        segment.goto(1000, 1000)
            else:
                # P2 still has lives - respawn P2
                head_p2.goto(100, 0)
                head_p2.direction = "stop"
                # Reset eyes
                eye1_p2.goto(95, 5)
                eye2_p2.goto(105, 5)
                for segment in segments_p2:
                    segment.hideturtle()
                segments_p2.clear()
            continue

    # ========================================================================
    # FOOD COLLISION DETECTION
    # ========================================================================
    
    # Check for collision with regular food (P1)
    if lives > 0 and head.distance(food) < 20:
        # Respawn food at random location
        x = random.randint(-300, 300)
        y = random.randint(-260, 260)
        food.goto(x, y)

        # Add new body segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.shapesize(1.1, 1.1)
        new_segment.color(color_themes[selected_theme]['p1_body'])
        new_segment.penup()
        segments.append(new_segment)

        # Update score
        score += 10
        update_score_display()
        check_level_up()
        spawn_golden_food()

    # Check for collision with food2 (P1 in 2-player mode)
    if game_mode == "2player" and lives > 0 and head.distance(food2) < 20:
        x = random.randint(-300, 300)
        y = random.randint(-260, 260)
        food2.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.shapesize(1.1, 1.1)
        new_segment.color(color_themes[selected_theme]['p1_body'])
        new_segment.penup()
        segments.append(new_segment)

        score += 10
        update_score_display()
        check_level_up()
        spawn_golden_food()

    # Check for collision with regular food (P2)
    if game_mode == "2player" and lives_p2 > 0 and head_p2.distance(food) < 20:
        x = random.randint(-300, 300)
        y = random.randint(-260, 260)
        food.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.shapesize(1.1, 1.1)
        new_segment.color(color_themes[selected_theme]['p2_body'])
        new_segment.penup()
        segments_p2.append(new_segment)

        score_p2 += 10
        update_score_display()
        check_level_up()
        spawn_golden_food()

    # Check for collision with food2 (P2)
    if game_mode == "2player" and lives_p2 > 0 and head_p2.distance(food2) < 20:
        x = random.randint(-300, 300)
        y = random.randint(-260, 260)
        food2.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.shapesize(1.1, 1.1)
        new_segment.color(color_themes[selected_theme]['p2_body'])
        new_segment.penup()
        segments_p2.append(new_segment)

        score_p2 += 10
        update_score_display()
        check_level_up()
        spawn_golden_food()

    # Check for golden food collision (P1)
    if lives > 0 and golden_food_active and head.distance(golden_food) < 20:
        golden_food_active = False
        golden_food.goto(1000, 1000)
        
        score += 50  # Golden food worth 50 points
        update_score_display()
        check_level_up()

    # Check for golden food collision (P2)
    if game_mode == "2player" and lives_p2 > 0 and golden_food_active and head_p2.distance(golden_food) < 20:
        golden_food_active = False
        golden_food.goto(1000, 1000)
        
        score_p2 += 50
        update_score_display()
        check_level_up()

    # Update golden food timer (remove golden food after timer expires)
    if golden_food_active:
        golden_food_timer -= 1
        if golden_food_timer <= 0:
            golden_food_active = False
            golden_food.goto(1000, 1000)

    # ========================================================================
    # BODY SEGMENT MOVEMENT
    # ========================================================================
    
    # Move P1 body segments (each segment follows the one in front)
    if lives > 0:
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        # First segment follows the head
        if len(segments) > 0:
            segments[0].goto(head.xcor(), head.ycor())

    # Move P2 body segments
    if game_mode == "2player" and lives_p2 > 0:
        for index in range(len(segments_p2) - 1, 0, -1):
            x = segments_p2[index - 1].xcor()
            y = segments_p2[index - 1].ycor()
            segments_p2[index].goto(x, y)

        if len(segments_p2) > 0:
            segments_p2[0].goto(head_p2.xcor(), head_p2.ycor())

    # ========================================================================
    # MOVE SNAKE HEADS
    # ========================================================================
    
    if lives > 0:
        move()  # Move P1
    if game_mode == "2player" and lives_p2 > 0:
        move_p2()  # Move P2

    # ========================================================================
    # SELF-COLLISION DETECTION (Snake hitting its own body)
    # ========================================================================
    
    # Check P1 collision with own body (skip first segment)
    if lives > 0:
        for segment in segments[1:]:
            if head.distance(segment) < 15:
                lives -= 1
                update_score_display()
                screen.update()
                
                if lives <= 0:
                    if game_mode == "2player":
                        if lives_p2 <= 0:
                            # Both players out - game over
                            game_over()
                        else:
                            # P1 is out, P2 continues - hide P1
                            head.goto(1000, 1000)
                            head.direction = "stop"
                            eye1_p1.goto(1000, 1000)
                            eye2_p1.goto(1000, 1000)
                            for seg in segments:
                                seg.goto(1000, 1000)
                    else:
                        game_over()
                else:
                    # P1 still has lives - respawn P1
                    head.goto(-100 if game_mode == "2player" else 0, 0)
                    head.direction = "stop"
                    # Reset eyes
                    if game_mode == "2player":
                        eye1_p1.goto(-105, 5)
                        eye2_p1.goto(-95, 5)
                    else:
                        eye1_p1.goto(-5, 5)
                        eye2_p1.goto(5, 5)
                    for seg in segments:
                        seg.hideturtle()
                    segments.clear()
                break

    # Check P2 collision with own body
    if game_mode == "2player" and lives_p2 > 0:
        for segment in segments_p2[1:]:
            if head_p2.distance(segment) < 15:
                lives_p2 -= 1
                update_score_display()
                screen.update()
                
                if lives_p2 <= 0:
                    if lives <= 0:
                        # Both players out - game over
                        game_over()
                    else:
                        # P2 is out, P1 continues - hide P2
                        head_p2.goto(1000, 1000)
                        head_p2.direction = "stop"
                        eye1_p2.goto(1000, 1000)
                        eye2_p2.goto(1000, 1000)
                        for seg in segments_p2:
                            seg.goto(1000, 1000)
                else:
                    # P2 still has lives - respawn P2
                    head_p2.goto(100, 0)
                    head_p2.direction = "stop"
                    # Reset eyes
                    eye1_p2.goto(95, 5)
                    eye2_p2.goto(105, 5)
                    for seg in segments_p2:
                        seg.hideturtle()
                    segments_p2.clear()
                break

        # Check for head-on collision between snakes
        if lives > 0 and head.distance(head_p2) < 15:
            # Both players lose a life
            lives -= 1
            lives_p2 -= 1
            update_score_display()
            screen.update()
            
            if lives <= 0 and lives_p2 <= 0:
                # Both players out - game over
                game_over()
            elif lives <= 0:
                # Only P1 is out - hide P1, respawn P2
                head.goto(1000, 1000)
                head.direction = "stop"
                eye1_p1.goto(1000, 1000)
                eye2_p1.goto(1000, 1000)
                for seg in segments:
                    seg.goto(1000, 1000)
                # Reset P2
                head_p2.goto(100, 0)
                head_p2.direction = "stop"
                eye1_p2.goto(95, 5)
                eye2_p2.goto(105, 5)
                for seg in segments_p2:
                    seg.hideturtle()
                segments_p2.clear()
            elif lives_p2 <= 0:
                # Only P2 is out - hide P2, respawn P1
                head_p2.goto(1000, 1000)
                head_p2.direction = "stop"
                eye1_p2.goto(1000, 1000)
                eye2_p2.goto(1000, 1000)
                for seg in segments_p2:
                    seg.goto(1000, 1000)
                # Reset P1
                head.goto(-100, 0)
                head.direction = "stop"
                eye1_p1.goto(-105, 5)
                eye2_p1.goto(-95, 5)
                for seg in segments:
                    seg.hideturtle()
                segments.clear()
            else:
                # Both still have lives - respawn both
                head.goto(-100, 0)
                head.direction = "stop"
                eye1_p1.goto(-105, 5)
                eye2_p1.goto(-95, 5)
                for seg in segments:
                    seg.hideturtle()
                segments.clear()
                
                head_p2.goto(100, 0)
                head_p2.direction = "stop"
                eye1_p2.goto(95, 5)
                eye2_p2.goto(105, 5)
                for seg in segments_p2:
                    seg.hideturtle()
                segments_p2.clear()

    # Update screen and delay before next frame
    screen.update()
    time.sleep(delay)

# Keep window open (this line is never reached due to infinite loop)
screen.mainloop()