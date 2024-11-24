import pygame
import sys
import random 

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
pygame.mouse.set_visible(False)

# Set up initial resolution
WIDTH, HEIGHT = 1920, 1080
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
BORDER_COLOR = (50,50,50)

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
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT * 0.4 + i * 160))
        
        pygame.display.flip()

def dino_game():
    global state
    randlower = 20
    randupper = 60
    clock = pygame.time.Clock()
    ground_y = HEIGHT - 100
    dino_y = ground_y - 60  # Dino height is 60, place it above the ground
    dino_velocity = 0
    gravity = 1.5
    is_jumping = False
    obstacles = []  # List to store obstacle positions
    obstacle_speed = 15
    score = 0

    min_distance = 300  # Minimum distance between consecutive obstacles
    spawn_timer = 0  # Timer to control obstacle spawning
    spawn_interval = 60  # Initial spawn interval (frames)

    # Colors
      # Example color for the ground (brown)

    def retry():
        dino_game()  # Restart the game

    def draw_pixelated_dino(surface, x, y, color):
        dino_pixels = [
            (0, 0), (1, 0),         # Top row (head)
            (0, 1),                 # Body
            (0, 2), (1, 2)          # Legs
        ]
        pixel_size = 20  # Increase size for better visibility

        for px, py in dino_pixels:
            pygame.draw.rect(surface, color, (x + px * pixel_size, y + py * pixel_size, pixel_size, pixel_size))

    def draw_pixelated_cactus(surface, x, y):
        cactus_pixels = [
            (0, 0),                  # Top
            (0, 1),                  # Middle
            (0, 2)                   # Base
        ]
        pixel_size = 20  # Larger cactus pixels

        for px, py in cactus_pixels:
            color = DARK_GREEN if py % 2 == 0 else GREEN  # Alternate colors for texture
            pygame.draw.rect(surface, color, (x + px * pixel_size, y + py * pixel_size, pixel_size, pixel_size))

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
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not is_jumping:
            is_jumping = True
            dino_velocity = -30

        if is_jumping:
            dino_y += dino_velocity
            dino_velocity += gravity
            if keys[pygame.K_DOWN]:
                dino_velocity += 10
            if dino_y >= ground_y - 60:  # Adjust to Dino's height
                dino_y = ground_y - 60
                is_jumping = False

        # Spawn obstacles at intervals
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            if not obstacles or WIDTH - obstacles[-1][0] > min_distance - 100:
                obstacles.append([WIDTH, ground_y - 60, False])  # Adjust obstacle height
                spawn_interval = random.randint(randlower, randupper)  # Randomize spawn interval

        # Move and manage obstacles
        for obstacle in obstacles:
            obstacle[0] -= obstacle_speed  # Move obstacle to the left

            # Update score if obstacle passed the Dino
            if obstacle[0] + 50 < 100 and not obstacle[2]:
                score += 1
                obstacle[2] = True  # Mark as passed to avoid double counting

        # Remove off-screen obstacles
        obstacles = [obs for obs in obstacles if obs[0] > -50]

        # Increase speed gradually based on score
        if score % 5 == 0 and score > 0:
            obstacle_speed += 0.1  # Smooth speed increase

        # Collision detection
        dino_rect = pygame.Rect(100, dino_y, 40, 60)  # Adjusted size for new Dino
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], 20, 60)  # Adjusted size for new Cactus
            if dino_rect.colliderect(obstacle_rect):
                show_scoreboard(score, retry, False)
                state = "menu"
                return

        # Draw game
        screen.fill(BLACK)

        # Draw ground
        pygame.draw.rect(screen, BORDER_COLOR, (0, ground_y, WIDTH, 100))

        # Draw pixelated Dino
        draw_pixelated_dino(screen, 100, dino_y, WHITE)

        # Draw pixelated Cactus obstacles
        for obstacle in obstacles:
            draw_pixelated_cactus(screen, obstacle[0], obstacle[1])

        # Display score
        font = get_scaled_font(int(HEIGHT * 0.05))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)


def snake_game():
    global state
    GRID_SIZE = 30  # Size of each grid cell
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
            show_scoreboard(score, snake_game)  # Allow retry by passing snake_game
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
    last_fall_time = pygame.time.get_ticks()

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
                    result = pause_menu()
                    if result == "menu":
                        state = "menu"
                        return
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        new_position = [piece_position[0], piece_position[1] - 1]
                        if not check_collision(current_piece, new_position):
                            piece_position = new_position
                    elif event.key == pygame.K_RIGHT:
                        new_position = [piece_position[0], piece_position[1] + 1]
                        if not check_collision(current_piece, new_position):
                            piece_position = new_position
                    elif event.key == pygame.K_DOWN:
                        new_position = [piece_position[0] + 1, piece_position[1]]
                        if not check_collision(current_piece, new_position):
                            piece_position = new_position
                    elif event.key == pygame.K_SPACE:
                        rotated = list(zip(*current_piece[::-1]))
                        if not check_collision(rotated, piece_position):
                            current_piece = rotated

        if not game_over:
            # Timer-based downward movement
            current_time = pygame.time.get_ticks()
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
            show_scoreboard(winner_text, tetris_game,True)
            state = "menu"
            return

        pygame.display.flip()
        clock.tick(60)

def space_game():
    global state
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    
    # Player
    player_width = 50
    player_height = 15
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 10
    player_speed = 7

    # Bullets
    bullets = []
    bullet_speed = -8
    bullet_width = 5
    bullet_height = 10

    # Enemies - Dynamic shapes
    def create_enemies():
     
        enemies = []
        for row in range(enemy_rows):
            row_enemies = []
            for col in range(enemy_cols):
                shape_type = random.choice(['rectangle', 'circle', 'triangle'])
                size = random.randint(25, 40)
                x = col * (size + 10) + 60
                y = row * (size + 10) + 50
                row_enemies.append({
                    'shape': shape_type,
                    'size': size,
                    'x': x,
                    'y': y,
                    'color': random.choice([RED, GREEN, BLUE])
                })
            enemies.append(row_enemies)
        return enemies
    
    enemy_rows = 4
    enemy_cols = 8
    enemy_speed = 20  
    enemy_direction = 1
    enemy_y_down = 10
    enemies = create_enemies()

    # Game variables
    score = 0
    game_over = False
    font = get_scaled_font(int(HEIGHT * 0.05))


    def draw_player():
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

    def draw_bullets():
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, bullet)

    def draw_enemies():
        for row in enemies:
            for enemy in row:
                if enemy['shape'] == 'rectangle':
                    pygame.draw.rect(screen, enemy['color'], (enemy['x'], enemy['y'], enemy['size'], enemy['size']))
                elif enemy['shape'] == 'circle':
                    pygame.draw.circle(screen, enemy['color'], (enemy['x'] + enemy['size'] // 2, enemy['y'] + enemy['size'] // 2), enemy['size'] // 2)
                elif enemy['shape'] == 'triangle':
                    points = [
                        (enemy['x'], enemy['y'] + enemy['size']),
                        (enemy['x'] + enemy['size'], enemy['y'] + enemy['size']),
                        (enemy['x'] + enemy['size'] // 2, enemy['y'])
                    ]
                    pygame.draw.polygon(screen, enemy['color'], points)

    def move_enemies():
        nonlocal enemy_direction, game_over
        edge_reached = False
        for row in enemies:
            for enemy in row:
                enemy['x'] += enemy_speed * enemy_direction
                if enemy['x'] <= 0 or enemy['x'] + enemy['size'] >= WIDTH:
                    edge_reached = True

        if edge_reached:
            enemy_direction *= -1
            for row in enemies:
                for enemy in row:
                    enemy['y'] += enemy_y_down
                    if enemy['y'] + enemy['size'] >= player_y:
                        game_over = True

    def handle_bullet_collisions():
        nonlocal score
        for bullet in bullets[:]:
            for row in enemies:
                for enemy in row[:]:
                    if pygame.Rect(bullet.x, bullet.y, bullet_width, bullet_height).colliderect(pygame.Rect(enemy['x'], enemy['y'], enemy['size'], enemy['size'])):
                        bullets.remove(bullet)
                        row.remove(enemy)
                        score += 10
                        break

    def reset_game():
        nonlocal enemies, score, game_over
        enemies = create_enemies()
        game_over = False

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
                elif event.key == pygame.K_SPACE:
                    if not game_over:
                        bullets.append(pygame.Rect(player_x + player_width // 2 - bullet_width // 2,
                                                   player_y - bullet_height, bullet_width, bullet_height))

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x + player_width < WIDTH:
                player_x += player_speed

        # Update bullets
        if not game_over:
            bullets = [bullet.move(0, bullet_speed) for bullet in bullets if bullet.y > 0]

            # Check collisions
            handle_bullet_collisions()

            # Move enemies
            move_enemies()

            # Check if all enemies are defeated
            if all(not row for row in enemies):
                reset_game()

        # Drawing
        screen.fill(BLACK)
        draw_player()
        draw_bullets()
        draw_enemies()

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Game Over screen
        if game_over:
            winner_text = f" Score: {score}"
            show_scoreboard(winner_text, space_game)
            state = "menu"
            return

        pygame.display.flip()
        clock.tick(60)


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
                    result = pause_menu()
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
