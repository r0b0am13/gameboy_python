import pygame
import sys
import random


pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GameBoy")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HIGHLIGHT = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


font = pygame.font.Font(None, 72)


games = ["Snake Game", "Dino Game",]


def draw_main_menu(selected_game):
    screen.fill(WHITE)

    # Static title
    title = font.render("Choose a Game", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

    # Dynamic game options
    for i, game in enumerate(games):
        color = HIGHLIGHT if i == selected_game else GRAY
        game_text = font.render(game, True, BLACK, color)
        screen.blit(game_text, (SCREEN_WIDTH // 2 - game_text.get_width() // 2, 200 + i * 100))

    pygame.display.flip()

# Snake Game
def snake_game():
    # Snake game implementation
    pass

# Dino Game
def dino_game():
    # Dino game implementation
    pass

# Main loop
def main():
    selected_game = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_game = (selected_game - 1) % len(games)
                elif event.key == pygame.K_DOWN:
                    selected_game = (selected_game + 1) % len(games)
                elif event.key == pygame.K_RETURN:
                    if selected_game == 0:
                        snake_game()
                    elif selected_game == 1:
                        dino_game()
                    elif selected_game == 2:
                        pygame.quit()
                        sys.exit()

        draw_main_menu(selected_game)

# Run the main loop
if __name__ == "__main__":
    main()