import pygame
import sys

"""

Current Status :

Added a layered approach for UI.
Main Screen (Game Selection Screen) is resizable. Pause Menu and Game Menu is not resizable.
Added modularized codes for a pause menu and scoreboard.
Only Dino Game (Ultra basic) works Others dont really do anything.
Suggest checking out all the screens.

"""
# Initialize Pygame
pygame.init()

# Set up initial resolution
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("GameBoy")
pygame.display.set_icon(pygame.image.load("gameboy.png"))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
HIGHLIGHT = (255, 0, 0)
OBSTACLE_COLOR = (200, 200, 200)

# Load game icons (ensure you have these images in the correct directory)
def load_icon(image_path, width, height):
    icon = pygame.image.load(image_path)
    return pygame.transform.scale(icon, (width, height))

# Game icons (replace these paths with actual paths to your game icons)
game_icons = [
    load_icon('dino_icon.png', 100, 100),  # Dino Game icon
    load_icon('snake_icon.png', 100, 100),  # Game 1 icon
    load_icon('tetris_icon.png', 100, 100),  # Game 2 icon
    load_icon('space_invaders_icon.png', 100, 100),  # Game 3 icon
    load_icon('tictactoe_icon.png', 100, 100),  # Game 4 icon
]

# Fonts
def get_scaled_font(size):
    return pygame.font.Font(None, size)

def pause_menu():
    pause_options = ["Resume", "Return to Main Menu"]
    selected_pause_option = 0
    
    while True:
        screen.fill(BLACK)
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
            color = HIGHLIGHT if i == selected_pause_option else WHITE
            text = pause_font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT * 0.4 + i * 60))
        
        pygame.display.flip()
        
def show_scoreboard(final_score, retry_callback):
    scoreboard_options = ["Retry", "Return to Main Menu"]
    selected_option = 0
    
    while True:
        screen.fill(BLACK)
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
        score_text = font.render(f"Final Score: {final_score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT * 0.2))
        
        for i, option in enumerate(scoreboard_options):
            color = HIGHLIGHT if i == selected_option else WHITE
            text = get_scaled_font(int(HEIGHT * 0.07)).render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT * 0.4 + i * 80))
        
        pygame.display.flip()

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
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (100, dino_y, 50, 50))  # Dino
        pygame.draw.rect(screen, OBSTACLE_COLOR, (obstacle_x, HEIGHT - 100, 50, 50))  # Obstacle
        
        # Display score
        font = get_scaled_font(int(HEIGHT * 0.05))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(30)

import pygame
import sys
import random

def snake_game():
    global state
    GRID_SIZE = 20  # Size of each grid cell
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Initial snake and food setup
    snake = [[5, 5]]  # List of [x, y] positions
    direction = [1, 0]  # Moving to the right initially
    food = [random.randint(0, (WIDTH // GRID_SIZE) - 1), random.randint(0, (HEIGHT // GRID_SIZE) - 1)]
    score = 0
    game_over = False
    font = pygame.font.SysFont("Arial", 25)

    def place_food():
        """Randomly place the food, ensuring it does not overlap with the snake."""
        while True:
            new_food = [random.randint(0, (WIDTH // GRID_SIZE) - 1),
                        random.randint(0, (HEIGHT // GRID_SIZE) - 1)]
            if new_food not in snake:
                return new_food

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
                        return
                if not game_over:
                    if event.key == pygame.K_UP and direction != [0, 1]:
                        direction = [0, -1]
                    elif event.key == pygame.K_DOWN and direction != [0, -1]:
                        direction = [0, 1]
                    elif event.key == pygame.K_LEFT and direction != [1, 0]:
                        direction = [-1, 0]
                    elif event.key == pygame.K_RIGHT and direction != [-1, 0]:
                        direction = [1, 0]

        if not game_over:
            # Move the snake
            new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
            snake.insert(0, new_head)

            # Check for collisions
            if (new_head in snake[1:] or
                new_head[0] < 0 or new_head[1] < 0 or
                new_head[0] >= WIDTH // GRID_SIZE or
                new_head[1] >= HEIGHT // GRID_SIZE):
                game_over = True

            # Check for food
            if new_head == food:
                score += 1
                food = place_food()
            else:
                snake.pop()  # Remove the tail unless eating food

        # Drawing
        screen.fill(BLACK)

        # Draw the snake
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw the food
        pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            winner_text = f"Game Over! Score: {score}"
            show_scoreboard(winner_text, snake_game)  # Allow retry by passing snake_game
            state = "menu"  # Go back to menu after showing scoreboard
            return

        pygame.display.flip()
        clock.tick(10)  # Adjust the speed of the game



def tetris_game():
    print("Game 2 Placeholder")

def space_game():
    print("Game 3 Placeholder")

def tictactoe_game():
    global state
    BOARD_SIZE = 3
    CELL_WIDTH = WIDTH // BOARD_SIZE
    CELL_HEIGHT = HEIGHT // BOARD_SIZE
    LINE_WIDTH = 10
    board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    font = get_scaled_font(int(HEIGHT * 0.08))

    # Game variables
    current_player = "X"
    game_over = False
    cursor_position = [0, 0]  

    def check_winner():
        """Check if there's a winner or if the game is a draw."""
        nonlocal game_over

        # Check rows
        for row in board:
            if row[0] == row[1] == row[2] != "":
                return row[0]

        # Check columns
        for col in range(BOARD_SIZE):
            if board[0][col] == board[1][col] == board[2] != "":
                return board[0][col]

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]

        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2]

        # Check for draw
        if all(board[row][col] != "" for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)):
            return "Draw"

        return None

    def reset_game():
        """Reset the game board and variables."""
        nonlocal board, current_player, game_over, cursor_position
        board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        current_player = "X"
        game_over = False
        cursor_position = [0, 0]

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

                if not game_over:
                    if event.key == pygame.K_UP:
                        cursor_position[0] = (cursor_position[0] - 1) % BOARD_SIZE
                    elif event.key == pygame.K_DOWN:
                        cursor_position[0] = (cursor_position[0] + 1) % BOARD_SIZE
                    elif event.key == pygame.K_LEFT:
                        cursor_position[1] = (cursor_position[1] - 1) % BOARD_SIZE
                    elif event.key == pygame.K_RIGHT:
                        cursor_position[1] = (cursor_position[1] + 1) % BOARD_SIZE
                    elif event.key == pygame.K_RETURN:
                        row, col = cursor_position
                        if board[row][col] == "":
                            board[row][col] = current_player
                            winner = check_winner()
                            if winner:
                                game_over = True
                                print(f"{winner} wins!" if winner != "Draw" else "It's a draw!")
                            current_player = "O" if current_player == "X" else "X"

                if event.key == pygame.K_r:  # Reset game with 'R'
                    reset_game()

        # Drawing
        screen.fill(WHITE)

        # Draw grid lines
        for x in range(1, BOARD_SIZE):
            pygame.draw.line(screen, BLACK, (x * CELL_WIDTH, 0), (x * CELL_WIDTH, HEIGHT), LINE_WIDTH)
        for y in range(1, BOARD_SIZE):
            pygame.draw.line(screen, BLACK, (0, y * CELL_HEIGHT), (WIDTH, y * CELL_HEIGHT), LINE_WIDTH)

        # Draw X and O
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] != "":
                    text = font.render(board[row][col], True, BLUE if board[row][col] == "X" else RED)
                    text_rect = text.get_rect(center=((col * CELL_WIDTH + CELL_WIDTH // 2),
                                                      (row * CELL_HEIGHT + CELL_HEIGHT // 2)))
                    screen.blit(text, text_rect)

        # Highlight the current cursor position
        pygame.draw.rect(
            screen,
            RED,
            (
                cursor_position[1] * CELL_WIDTH,
                cursor_position[0] * CELL_HEIGHT,
                CELL_WIDTH,
                CELL_HEIGHT,
            ),
            5,
        )

        # Display winner
        if game_over:
            winner_text = "Draw!" if winner == "Draw" else f"{winner} wins!"
            show_scoreboard(winner_text, reset_game)
            state = "menu"  # Go back to menu after showing scoreboard
            return

        pygame.display.flip()
  
    
# Main Menu Logic
games = [
    {"name": "Dino Game", "func": dino_game, "icon": game_icons[0]},
    {"name": "Snake Game", "func": snake_game, "icon": game_icons[1]},
    {"name": "Tetris", "func": tetris_game , "icon": game_icons[2]},
    {"name": "Space Invaders", "func": space_game, "icon": game_icons[3]},
    {"name": "Tic-Tac-Toe", "func": tictactoe_game, "icon": game_icons[4]},
]



state = "menu"
selected_game = 0
selected_option = 0  # 0 for games, 1 for quit

# Main loop
while state == "menu":
    screen.fill(BLACK)
    WIDTH, HEIGHT = screen.get_size()
    
    title_font = get_scaled_font(int(HEIGHT * 0.08))
    game_font = get_scaled_font(int(HEIGHT * 0.05))
    
    # Draw Title
    title_text = title_font.render("Choose Game", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT * 0.1))
    
    # Horizontal Game Options
    game_spacing = WIDTH // len(games)
    start_x = (WIDTH - game_spacing * (len(games) - 1)) // 2
    
    # Draw the game section (always visible, top section)
     # Game selection section
    for i, game in enumerate(games):
            # Highlighting icon instead of name
            icon_color = HIGHLIGHT if (i == selected_game and selected_option ==0) else WHITE
            icon = pygame.Surface(game["icon"].get_size())  # Create surface for icon highlight
            icon.fill(icon_color)
            screen.blit(game["icon"], (start_x + i * game_spacing - game["icon"].get_width() // 2, HEIGHT * 0.4))

            # Display Game Name
            game_name_text = game_font.render(game["name"], True, icon_color)
            screen.blit(game_name_text, (start_x + i * game_spacing - game_name_text.get_width() // 2, HEIGHT * 0.55))

    # Draw Quit Option (Always visible at the bottom)
    quit_font = get_scaled_font(int(HEIGHT * 0.07))
    quit_text = quit_font.render("Quit", True, HIGHLIGHT if selected_option == 1 else WHITE)
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT * 0.85))  # Placing at 85% of the height

    pygame.display.flip()

    # Handle Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and selected_option == 0:
                selected_game = (selected_game - 1) % len(games)
            elif event.key == pygame.K_RIGHT and selected_option == 0:
                selected_game = (selected_game + 1) % len(games)
            elif event.key == pygame.K_LEFT and selected_option == 1:
                selected_game,selected_option = len(games)-1 , 0
            elif event.key == pygame.K_RIGHT and selected_option == 1:
                selected_game,selected_option = 0 , 0
            elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                if (selected_option == 1):
                    selected_option = 0
                else:
                    selected_option = 1
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:
                    state = "game"
                    games[selected_game]["func"]()
                elif selected_option == 1:
                    pygame.quit()
                    sys.exit()
