import pygame
import sys
import random 

"""

Current Status :

Added a layered approach for UI.
Main Screen (Game Selection Screen) is resizable. Pause Menu and Game Menu is not resizable.
Added modularized codes for a pause menu and scoreboard.

Suggest checking out all the screens.

"""
# Initialize Pygame
pygame.init()
pygame.mouse.set_visible(False)

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
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
DARK_GREEN = (21,71,52)
BORDER_COLOR = (194, 178, 128)
SKY_BLUE = (135, 206, 235)


# Load game icons (ensure you have these images in the correct directory)
def load_icon(image_path, width, height):
    icon = pygame.image.load(image_path)
    return pygame.transform.scale(icon, (width, height))

# Game icons (replace these paths with actual paths to your game icons)
game_icons = [
    load_icon('dino_icon.png', 100, 100),  # Dino Game icon
    load_icon('snake_icon.png', 100, 100),  # Game 1 icon
    load_icon('tetris_icon.png', 100, 100),  # Game 2 icon
    load_icon('bird.png', 100, 100),  # Game 3 icon
    load_icon('tictactoe_icon.png', 100, 100),  # Game 4 icon
]

# Fonts
def get_scaled_font(size):
    return pygame.font.Font(None, size)

def pause_menu(game):
    pause_options = ["Resume", "Return to Main Menu", "Help"]
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
                    elif pause_options[selected_pause_option] == "Help":
                        help("game",game)
        
        pause_font = get_scaled_font(int(HEIGHT * 0.08))
        total_text_height = len(pause_options) * pause_font.get_height()  # Total height of all lines
        start_y = (HEIGHT) / 2 - total_text_height + HEIGHT * 0.1  # Adjust start position to center vertically below title

        for i, line in enumerate(pause_options):
            color = HIGHLIGHT if i == selected_pause_option else WHITE
            text_surface = pause_font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(WIDTH / 2, start_y + i * (pause_font.get_height() + 25*HEIGHT/800) ))  # Each line below the previous one
            screen.blit(text_surface, text_rect)
            
            
            
        
        
        pygame.display.flip()
        
def show_scoreboard(final_score, retry_callback,custom):
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
        score_text = font.render(f"Final Score: {final_score}", True, WHITE) if (not custom) else font.render(f"{final_score}",True,WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT * 0.2))
        
        for i, option in enumerate(scoreboard_options):
            color = HIGHLIGHT if i == selected_option else WHITE
            text = get_scaled_font(int(HEIGHT * 0.07)).render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT * 0.4 + i * 80))
        
        pygame.display.flip()
# Load and scale images to 3 blocks size (60x60 pixels)


def dino_game():
    
    block_size = 60*WIDTH/1000
    dino_img = pygame.image.load('dino_icon.png')
    cactus_img = pygame.image.load('cactus.png')

    dino_img = pygame.transform.scale(dino_img, (block_size, 60))  # 3 blocks wide and tall
    cactus_img = pygame.transform.scale(cactus_img, (60, 60))
    global state
    randlower = 20
    randupper = 60
    clock = pygame.time.Clock()
    ground_y = HEIGHT - 100
    dino_y = ground_y - 60  # Adjusted for Dino height
    dino_velocity = 0
    gravity = 2*WIDTH/800
    is_jumping = False  
    obstacles = []  # List to store obstacle positions
    obstacle_speed = 10  # Starting speed
    score = 0

    min_distance = 300  # Minimum distance between consecutive obstacles
    spawn_timer = 0
    spawn_interval = 60

    def retry():
        dino_game()  # Restart the game

    while state == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = pause_menu("dino")  # Call pause menu if defined
                    if result == "menu":
                        state = "menu"
                        return

        # Game Logic
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not is_jumping:
            is_jumping = True
            dino_velocity = -25*WIDTH/800  # Jump strength

        if is_jumping:
            dino_y += dino_velocity
            dino_velocity += gravity
            if keys[pygame.K_DOWN]:  # Fast fall
                dino_velocity += 5
            if dino_y >= ground_y - 60: 
                dino_y = ground_y - 60
                is_jumping = False

        # Spawn and move obstacles
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            if not obstacles or WIDTH - obstacles[-1][0] > min_distance - 100:
                obstacles.append([WIDTH, ground_y - 60, False])  # False indicates not passed yet
                spawn_interval = random.randint(randlower, randupper)

        for obstacle in obstacles:
            obstacle[0] -= obstacle_speed  # Move obstacles left

            # Update score if Dino passes the obstacle
            if obstacle[0] + 60 < 100 and not obstacle[2]:
                score += 1
                obstacle[2] = True  # Mark as passed

        # Remove off-screen obstacles
        obstacles = [obs for obs in obstacles if obs[0] > -60]

        # Increase speed gradually based on score
        if score > 0 and score % 5 == 0:
            obstacle_speed += 0.01  # Smooth speed increase

        # Collision detection
        dino_rect = pygame.Rect(100, dino_y, 60, 60)  # Dino rectangle
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], 60, 60)
            if dino_rect.colliderect(obstacle_rect):
                show_scoreboard(score, retry, False)  # Call scoreboard
                state = "menu"
                return

        # Draw game elements
        screen.fill(BLACK)
        pygame.draw.rect(screen, BORDER_COLOR, (0, ground_y, WIDTH, 100))  # Ground

        # Draw Dino and obstacles
        screen.blit(dino_img, (100, dino_y))  # Draw scaled Dino
        for obstacle in obstacles:
            screen.blit(cactus_img, (obstacle[0], obstacle[1]))  # Draw scaled Cactus

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)



def snake_game():
    global state
    GRID_SIZE = int(30*WIDTH/1080)  # Size of each grid cell
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Initial snake setup: size of 3
    snake = [[5, 5], [4, 5], [3, 5]]  # Starting with 3 segments
    direction = [1, 0]  # Moving to the right initially
    food = [random.randint(1, (WIDTH // GRID_SIZE) - 2), random.randint(1, (HEIGHT // GRID_SIZE) - 2)]
    score = 0
    game_over = False

    def place_food():
        """Randomly place the food, ensuring it does not overlap with the snake or border."""
        while True:
            new_food = [random.randint(1, (WIDTH // GRID_SIZE) - 2),
                        random.randint(1, (HEIGHT // GRID_SIZE) - 2)]
            if new_food not in snake:
                return new_food

    while state == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = pause_menu("snake")
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

            # Check for collisions with self or border
            if (new_head in snake[1:] or
                new_head[0] <= 0 or new_head[1] <= 0 or
                new_head[0] >= WIDTH // GRID_SIZE - 1 or
                new_head[1] >= HEIGHT // GRID_SIZE - 1):
                game_over = True

            # Check for food
            if new_head == food:
                score += 1
                food = place_food()
            else:
                snake.pop()  # Remove the tail unless eating food

        # Drawing
        screen.fill(BLACK)

        # Draw the border
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.rect(screen, BORDER_COLOR, (x, 0, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BORDER_COLOR, (x, HEIGHT - GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.rect(screen, BORDER_COLOR, (0, y, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BORDER_COLOR, (WIDTH - GRID_SIZE, y, GRID_SIZE, GRID_SIZE))

        # Draw the snake
        for i, segment in enumerate(snake):
            if i == 0:  # Head of the snake
                pygame.draw.rect(screen, DARK_GREEN,
                                 (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            else:  # Body of the snake
                pygame.draw.rect(screen, GREEN,
                                 (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw the food
        pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Display score
        font = get_scaled_font(int(HEIGHT * 0.04))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            show_scoreboard(score, snake_game,False)  # Allow retry by passing snake_game
            state = "menu"  # Go back to menu after showing scoreboard 
            return

        pygame.display.flip()
        clock.tick(10)

def tetris_game():
    global state
    GRID_SIZE = 30  # Size of each block
    COLS = WIDTH // GRID_SIZE
    ROWS = HEIGHT // GRID_SIZE
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED]

    # Tetromino shapes
    TETROMINOES = [
        [[1, 1, 1, 1]],  # I
        [[2, 2], [2, 2]],  # O
        [[0, 3, 0], [3, 3, 3]],  # T
        [[0, 4, 4], [4, 4, 0]],  # S
        [[5, 5, 0], [0, 5, 5]],  # Z
        [[6, 6, 6], [6, 0, 0]],  # L
        [[7, 7, 7], [0, 0, 7]],  # J
    ]

    # Game variables
    grid = [[0] * COLS for _ in range(ROWS)]
    current_piece = None
    piece_position = [0, COLS // 2 - 2]
    score = 0
    game_over = False

    fall_speed = 500  # Milliseconds between automatic downward moves
    move_speed = 100  # Milliseconds between horizontal/vertical moves
    last_fall_time = pygame.time.get_ticks()
    last_move_time = pygame.time.get_ticks()

    def spawn_piece():
        return random.choice(TETROMINOES)

    def draw_grid():
        for row in range(ROWS):
            for col in range(COLS):
                if grid[row][col] != 0:
                    pygame.draw.rect(screen, COLORS[grid[row][col] - 1],
                                     (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)

    def draw_piece(piece, position):
        for i, row in enumerate(piece):
            for j, cell in enumerate(row):
                if cell != 0:
                    pygame.draw.rect(screen, COLORS[cell - 1],
                                     ((position[1] + j) * GRID_SIZE, (position[0] + i) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(screen, (0, 0, 0),
                                     ((position[1] + j) * GRID_SIZE, (position[0] + i) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)

    def check_collision(piece, position):
        for i, row in enumerate(piece):
            for j, cell in enumerate(row):
                if cell != 0:
                    x, y = position[1] + j, position[0] + i
                    if x < 0 or x >= COLS or y >= ROWS or (y >= 0 and grid[y][x] != 0):
                        return True
        return False

    def lock_piece(piece, position):
        nonlocal score
        for i, row in enumerate(piece):
            for j, cell in enumerate(row):
                if cell != 0:
                    grid[position[0] + i][position[1] + j] = cell

        cleared_rows = 0
        for i in range(ROWS):
            if all(grid[i]):
                del grid[i]
                grid.insert(0, [0] * COLS)
                cleared_rows += 1

        score += cleared_rows ** 2

    current_piece = spawn_piece()

    while state == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = pause_menu("tetris")
                    if result == "menu":
                        state = "menu"
                        return
                if not game_over and event.key == pygame.K_SPACE:
                    # Rotate the piece once per keypress
                    rotated = list(zip(*current_piece[::-1]))
                    if not check_collision(rotated, piece_position):
                        current_piece = rotated

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if not game_over:
            # Continuous movement for left, right, and down keys
            if keys[pygame.K_LEFT] and current_time - last_move_time > move_speed:
                new_position = [piece_position[0], piece_position[1] - 1]
                if not check_collision(current_piece, new_position):
                    piece_position = new_position
                last_move_time = current_time
            if keys[pygame.K_RIGHT] and current_time - last_move_time > move_speed:
                new_position = [piece_position[0], piece_position[1] + 1]
                if not check_collision(current_piece, new_position):
                    piece_position = new_position
                last_move_time = current_time
            if keys[pygame.K_DOWN] and current_time - last_move_time > move_speed:
                new_position = [piece_position[0] + 1, piece_position[1]]
                if not check_collision(current_piece, new_position):
                    piece_position = new_position
                last_move_time = current_time

            # Timer-based downward movement
            if current_time - last_fall_time > fall_speed:
                last_fall_time = current_time
                new_position = [piece_position[0] + 1, piece_position[1]]
                if check_collision(current_piece, new_position):
                    lock_piece(current_piece, piece_position)
                    current_piece = spawn_piece()
                    piece_position = [0, COLS // 2 - 2]
                    if check_collision(current_piece, piece_position):
                        game_over = True
                else:
                    piece_position = new_position

        screen.fill((0, 0, 0))
        draw_grid()
        draw_piece(current_piece, piece_position)

        font = get_scaled_font(int(HEIGHT * 0.05))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            winner_text = f"Game Over! Score: {score}"
            show_scoreboard(winner_text, tetris_game, True)
            state = "menu"
            return

        pygame.display.flip()
        clock.tick(60)



def flappy_bird():
    global state
    gravity = 0.5
    bird_y = HEIGHT // 2
    bird_velocity = 0
    flap_strength = -10
    pipes = []  # List to store pipe positions
    pipe_speed = 5
    pipe_gap = 200
    score = 0
    spawn_timer = 0
    spawn_interval = 120
    clock = pygame.time.Clock()

    # Load bird image
    bird_img = pygame.image.load('bird.png')  # Replace with the path to your bird PNG
    bird_img = pygame.transform.flip(bird_img, True, False)  # Flip the bird image
    bird_img = pygame.transform.scale(bird_img, (50, 50))  # Resize the image

    def retry():
        flappy_bird()  # Restart the game

    def draw_pipe(surface, x, height, inverted=False,pipe_gap=200):
        pipe_color = GREEN
        outline_color = BLACK
        pipe_width = 80
        if inverted:
            # Top pipe with outline
            outer_rect = pygame.Rect(x - 2, -2, pipe_width + 4, height + 4)  # Border dimensions
            inner_rect = pygame.Rect(x, 0, pipe_width, height)  # Pipe dimensions
            pygame.draw.rect(surface, outline_color, outer_rect)  # Draw black outline
            pygame.draw.rect(surface, pipe_color, inner_rect)  # Fill pipe color
        else:
            # Bottom pipe with outline
            outer_rect = pygame.Rect(x - 2, height + pipe_gap - 2, pipe_width + 4, HEIGHT - height - pipe_gap + 4)
            inner_rect = pygame.Rect(x, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
            pygame.draw.rect(surface, outline_color, outer_rect)  # Draw black outline
            pygame.draw.rect(surface, pipe_color, inner_rect)  # Fill pipe color

    while state == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = pause_menu("flappy")
                    if result == "menu":
                        state = "menu"
                        return  # Return to main menu

        # Game Logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            bird_velocity = flap_strength

        bird_y += bird_velocity
        bird_velocity += gravity

        # Prevent bird from going off-screen
        if bird_y < 0:
            bird_y = 0
            bird_velocity = 0
        elif bird_y > HEIGHT - 50:
            show_scoreboard(score, retry, False)
            state = "menu"
            return

        # Spawn pipes at intervals
        
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            pipe_height = random.randint(100, HEIGHT - pipe_gap - 100)
            pipes.append([WIDTH, pipe_height, False])

        # Move and manage pipes
        for pipe in pipes:
            pipe[0] -= pipe_speed

            # Update score if bird passes the pipe
            if pipe[0] + 80 < 100 and not pipe[2]:  # Adjusted pipe size
                score += 1
                pipe[2] = True  # Mark as passed

        # Gradually increase pipe speed based on score
        pipe_speed = 10 + score // 5
        spawn_interval = spawn_interval - score // 5

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe[0] > -80]

        # Collision detection
        bird_rect = pygame.Rect(100, bird_y, 50, 50)  # Match bird image size
        for pipe in pipes:
            top_pipe_rect = pygame.Rect(pipe[0], 0, 80, pipe[1])
            bottom_pipe_rect = pygame.Rect(pipe[0], pipe[1] + pipe_gap, 80, HEIGHT - pipe[1] - pipe_gap)
            if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                show_scoreboard(score, retry, False)
                state = "menu"
                return

        # Draw game
        screen.fill(SKY_BLUE)

        # Draw bird
        screen.blit(bird_img, (100, bird_y))

        # Draw pipes
        for pipe in pipes:
            draw_pipe(screen, pipe[0], pipe[1], inverted=True,pipe_gap=pipe_gap)  # Top pipe
            draw_pipe(screen, pipe[0], pipe[1],pipe_gap = pipe_gap)  # Bottom pipe

        # Display score
        font = get_scaled_font(int(HEIGHT * 0.05))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)  # Set game to run at 60 FPS


def tictactoe_game():
    global state
    BOARD_SIZE = 3
    CELL_WIDTH = WIDTH // BOARD_SIZE
    CELL_HEIGHT = HEIGHT // BOARD_SIZE
    LINE_WIDTH = 10
    board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    font = get_scaled_font(int(HEIGHT * 0.08))

    # Game variables
    current_player = random.choice(["X", "O"])  # Randomly choose starter (X for Player, O for AI)
    game_over = False
    cursor_position = [0, 0]  

    def check_winner():
      
        nonlocal game_over

        # Check rows
        for row in board:
            if row[0] == row[1] == row[2] != "":
                return row[0]

        # Check columns
        for col in range(BOARD_SIZE):
            if board[0][col] == board[1][col] == board[2][col] != "":
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
        tictactoe_game()

    def ai_move():
       
        # Try to win or block a win
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == "":
                    # Simulate the AI making a move
                    board[row][col] = "O"
                    if check_winner() == "O":
                        return
                    board[row][col] = ""  # Undo move

                    # Simulate the AI blocking the player's win
                    board[row][col] = "X"
                    if check_winner() == "X":
                        board[row][col] = "O"
                        return
                    board[row][col] = ""  # Undo move

        # Play in the first available cell
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == "":
                    board[row][col] = "O"
                    return

    while state == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = pause_menu("tictactoe")
                    if result == "menu":
                        state = "menu"
                        return  # Return to main menu

                if not game_over and current_player == "X":  # Player controls only on their turn
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
                                
                            current_player = "O" if current_player == "X" else "X"

                if event.key == pygame.K_r:  # Reset game with 'R'
                    reset_game()

        # AI's turn
        if not game_over and current_player == "O":
            pygame.time.wait(500)  # Add a slight delay for AI's move
            ai_move()
            winner = check_winner()
            if winner:
                game_over = True
                
            current_player = "X"

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
        if not game_over and current_player == "X":  # Highlight only for the player's turn
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
            show_scoreboard(winner_text, reset_game,True)
            state = "menu"  # Go back to menu after showing scoreboard
            return

        pygame.display.flip()
  
    
# Main Menu Logic
games = [
    {"name": "Dino Game", "func": dino_game, "icon": game_icons[0]},
    {"name": "Snake Game", "func": snake_game, "icon": game_icons[1]},
    {"name": "Tetris", "func": tetris_game , "icon": game_icons[2]},
    {"name": "Flappy Bird", "func": flappy_bird, "icon": game_icons[3]},
    {"name": "Tic-Tac-Toe", "func": tictactoe_game, "icon": game_icons[4]},
]

def help(state,game=None):
    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
        if state == "menu":
            text_lines = [
                "Welcome to the Gameboy!",
                "Use arrow keys to navigate the menu.",
                "Press Enter to select an option",
                "Press Escape in-game to view the pause menu.",
                "Help for games is available in pause menu.",
            ]
        elif state == "game":
            if game == "dino":
                text_lines = [
                    "Dino Game Instructions:",
                    "Press Space or Up Arrow to jump.",
                    "Press Down Arrow while falling to fast fall.",
                    "Avoid obstacles to score points.",
                    "Pressing Left Arrow or Right Arrow does nothing.",
                    
                ]
            elif game == "snake":
                text_lines = [
                    "Snake Game Instructions:",
                    "Use arrow keys to move the snake.",
                    "Eat food to grow longer.",
                    "Avoid hitting the walls or yourself.",
                    "More food you eat, higher your score."
                ]
            elif game == "flappy":
                text_lines = [
                    "Flappy Bird Instructions:",
                    "Press Space to flap.",
                    "Avoid obstacles to keep flying.",
                    "Score points by passing through gaps."
                ]
            elif game == "tetris":
                text_lines = [
                    "Tetris Instructions:",
                    "Use arrow keys to move blocks.",
                    "Press Space to rotate blocks.",
                    "Complete rows to score points."
                ]
            elif game == "tictactoe":
                text_lines = [
                    "Tic-Tac-Toe Instructions:",
                    "Use arrow keys to select a cell.",
                    "Press Enter or Space to place your mark.",
                    "First to get three in a row wins!"
                ]
            else:
                text_lines = ["Invalid game selected!"]
        screen.fill(BLACK)
        title_font = get_scaled_font(int(HEIGHT * 0.08))
        content_font = get_scaled_font(int(HEIGHT * 0.06))
        
        title_surface = title_font.render("Help ", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH / 2, HEIGHT * 0.1))  # Title at 10% from top
        screen.blit(title_surface, title_rect)
        
        total_text_height = len(text_lines) * content_font.get_height()  # Total height of all lines
        start_y = (HEIGHT) / 2 - total_text_height + HEIGHT * 0.1  # Adjust start position to center vertically below title

        for i, line in enumerate(text_lines):
            text_surface = content_font.render(line, True, WHITE if i==0 else HIGHLIGHT)
            text_rect = text_surface.get_rect(center=(WIDTH / 2, start_y + i * (content_font.get_height() + 10) - (50 if i==0 else 0)))  # Each line below the previous one
            screen.blit(text_surface, text_rect)
   
       
        pygame.display.flip()
        pygame.time.Clock().tick(30) # Limit to 30 FPS

state = "menu"
selected_game = 0
selected_option = 0
quit_selected = True

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
    quit_text = quit_font.render("Quit", True, HIGHLIGHT if (selected_option == 1 and quit_selected)  else WHITE)
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() - 100, HEIGHT * 0.85))
    help_font = get_scaled_font(int(HEIGHT * 0.07))
    help_text = help_font.render("Help", True, HIGHLIGHT if (selected_option == 1 and not quit_selected)  else WHITE)
    screen.blit(help_text, (WIDTH // 2 - quit_text.get_width() + 100*WIDTH/800, HEIGHT * 0.85))# Placing at 85% of the height

    pygame.display.flip()
    pygame.time.Clock().tick(30)  # Limit to 30 FPS

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
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) and selected_option == 1:
                quit_selected = not quit_selected
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
                    if(quit_selected):
                        pygame.quit()
                        sys.exit()
                    else:
                        help(state)
                        
                        

