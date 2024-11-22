import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up initial resolution
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Game Selector")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (0, 128, 255)
OBSTACLE_COLOR = (255, 0, 0)

# Load game icons (ensure you have these images in the correct directory)
def load_icon(image_path, width, height):
    icon = pygame.image.load(image_path)
    return pygame.transform.scale(icon, (width, height))

# Game icons (replace these paths with actual paths to your game icons)
game_icons = [
    load_icon('dino_icon.png', 100, 100),  # Dino Game icon
    load_icon('game1_icon.png', 100, 100),  # Game 1 icon
    load_icon('game2_icon.png', 100, 100),  # Game 2 icon
    load_icon('game3_icon.png', 100, 100),  # Game 3 icon
    load_icon('game4_icon.png', 100, 100),  # Game 4 icon
]

# Fonts
def get_scaled_font(size):
    return pygame.font.Font(None, size)

# Modular Pause Menu Function
def pause_menu():
    pause_options = ["Resume", "Return to Main Menu"]
    selected_pause_option = 0
    
    while True:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_pause_option = (selected_pause_option + 1) % len(pause_options)
                elif event.key == pygame.K_UP:
                    selected_pause_option = (selected_pause_option - 1) % len(pause_options)
                elif event.key == pygame.K_RETURN:
                    if pause_options[selected_pause_option] == "Resume":
                        return "resume"
                    elif pause_options[selected_pause_option] == "Return to Main Menu":
                        return "menu"
        
        pause_font = get_scaled_font(int(HEIGHT * 0.07))
        for i, option in enumerate(pause_options):
            color = HIGHLIGHT if i == selected_pause_option else BLACK
            text = pause_font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT * 0.4 + i * 60))
        
        pygame.display.flip()

# Modular Scoreboard Function
def show_scoreboard(final_score, retry_callback):
    scoreboard_options = ["Retry", "Return to Main Menu"]
    selected_option = 0
    
    while True:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(scoreboard_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(scoreboard_options)
                elif event.key == pygame.K_RETURN:
                    if scoreboard_options[selected_option] == "Retry":
                        retry_callback()  # Restart the game
                        return
                    elif scoreboard_options[selected_option] == "Return to Main Menu":
                        return
        
        font = get_scaled_font(int(HEIGHT * 0.08))
        score_text = font.render(f"Final Score: {final_score}", True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT * 0.2))
        
        for i, option in enumerate(scoreboard_options):
            color = HIGHLIGHT if i == selected_option else BLACK
            text = get_scaled_font(int(HEIGHT * 0.07)).render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT * 0.4 + i * 80))
        
        pygame.display.flip()

# Example Game Function
def dino_game():
    global state
    clock = pygame.time.Clock()
    dino_y = HEIGHT - 100
    dino_velocity = 0
    gravity = 1
    is_jumping = False
    obstacle_x = WIDTH
    obstacle_speed = 10
    score = 0
    
    def retry():
        dino_game()  # Restart the game
    
    while state == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = pause_menu()
                    if result == "menu":
                        state = "menu"
                        return  # Return to main menu
        
        # Game Logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not is_jumping:
            is_jumping = True
            dino_velocity = -20
        
        if is_jumping:
            dino_y += dino_velocity
            dino_velocity += gravity
            if dino_y >= HEIGHT - 100:
                dino_y = HEIGHT - 100
                is_jumping = False
        
        # Move obstacle
        obstacle_x -= obstacle_speed
        if obstacle_x < 0:
            obstacle_x = WIDTH
            score += 1
        
        # Collision detection
        dino_rect = pygame.Rect(100, dino_y, 50, 50)
        obstacle_rect = pygame.Rect(obstacle_x, HEIGHT - 100, 50, 50)
        if dino_rect.colliderect(obstacle_rect):
            show_scoreboard(score, retry)
            state = "menu"
            return
        
        # Draw game
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (100, dino_y, 50, 50))  # Dino
        pygame.draw.rect(screen, OBSTACLE_COLOR, (obstacle_x, HEIGHT - 100, 50, 50))  # Obstacle
        
        # Display score
        font = get_scaled_font(int(HEIGHT * 0.05))
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(30)

# Placeholder Games
def game1():
    print("Game 1 Placeholder")

def game2():
    print("Game 2 Placeholder")

def game3():
    print("Game 3 Placeholder")

def game4():
    print("Game 4 Placeholder")

# Main Menu Logic
games = [
    {"name": "Dino Game", "func": dino_game, "icon": game_icons[0]},
    {"name": "Game 1", "func": game1, "icon": game_icons[1]},
    {"name": "Game 2", "func": game2, "icon": game_icons[2]},
    {"name": "Game 3", "func": game3, "icon": game_icons[3]},
    {"name": "Game 4", "func": game4, "icon": game_icons[4]},
]

state = "menu"
selected_game = 0
selected_option = 0  # 0 for games, 1 for quit

# Main loop
while state == "menu":
    screen.fill(WHITE)
    WIDTH, HEIGHT = screen.get_size()
    
    title_font = get_scaled_font(int(HEIGHT * 0.08))
    game_font = get_scaled_font(int(HEIGHT * 0.05))
    
    # Draw Title
    title_text = title_font.render("Choose Game", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT * 0.1))
    
    # Horizontal Game Options
    game_spacing = WIDTH // len(games)
    start_x = (WIDTH - game_spacing * (len(games) - 1)) // 2
    
    for i, game in enumerate(games):
        # Highlighting icon instead of name
        icon_color = HIGHLIGHT if i == selected_game else BLACK
        icon = pygame.Surface(game["icon"].get_size())  # Create surface for icon highlight
        icon.fill(icon_color)
        screen.blit(icon, (start_x + i * game_spacing - icon.get_width() // 2, HEIGHT * 0.4 - 10))
        screen.blit(game["icon"], (start_x + i * game_spacing - game["icon"].get_width() // 2, HEIGHT * 0.4))

        # Display Game Name
        game_name_text = game_font.render(game["name"], True, icon_color)
        screen.blit(game_name_text, (start_x + i * game_spacing - game_name_text.get_width() // 2, HEIGHT * 0.55))

    # Draw Quit Option
    quit_font = get_scaled_font(int(HEIGHT * 0.07))
    quit_text = quit_font.render("Quit", True, BLACK)
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT * 0.8))
    
    pygame.display.flip()

    # Handle Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                selected_game = (selected_game - 1) % len(games)
            elif event.key == pygame.K_RIGHT:
                selected_game = (selected_game + 1) % len(games)
            elif event.key == pygame.K_DOWN:
                selected_option = 1
            elif event.key == pygame.K_UP:
                selected_option = 0
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:
                    state = "game"
                    games[selected_game]["func"]()  # Start the selected game
                elif selected_option == 1:
                    pygame.quit()
                    sys.exit()
