import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
LINE_WIDTH = 10
BOARD_SIZE = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Calculate cell size
CELL_WIDTH = WIDTH // BOARD_SIZE
CELL_HEIGHT = HEIGHT // BOARD_SIZE

# Initialize the board
board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Fonts
font = pygame.font.Font(None, 100)

# Game variables
current_player = "X"
game_over = False
cursor_position = [0, 0]  # Row and Column


def check_winner():
    """Check if there's a winner or if the game is a draw."""
    global game_over

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


# def reset_game():
#     """Reset the game state."""
#     global board, current_player, game_over, cursor_position
#     board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
#     current_player = "X"
#     game_over = False
#     cursor_position = [0, 0]


# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
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


    """Draw the Tic Tac Toe grid."""
    screen.fill(WHITE)

    # Vertical lines
    for x in range(1, BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (x * CELL_WIDTH, 0), (x * CELL_WIDTH, HEIGHT), LINE_WIDTH)

    # Horizontal lines
    for y in range(1, BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (0, y * CELL_HEIGHT), (WIDTH, y * CELL_HEIGHT), LINE_WIDTH)

    # Draw the pieces (X and O)
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

    if game_over:
        winner_text = "Draw!" if winner == "Draw" else f"{winner} wins!"
        text = font.render(winner_text, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
