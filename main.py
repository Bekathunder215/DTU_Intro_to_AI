import pygame
import numpy as np

# Constants
GRID_SIZE = 4
CELL_SIZE = 100
GAP_SIZE = 10
WIDTH = HEIGHT = GRID_SIZE * (CELL_SIZE + GAP_SIZE) + GAP_SIZE
BACKGROUND_COLOR = (187, 173, 160)
CELL_COLOR = {0: (205, 193, 180), 2: (238, 228, 218), 4: (237, 224, 200)}  # Add more colors later
TEXT_COLOR = (119, 110, 101)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")
font = pygame.font.Font(None, 50)

# Initialize grid
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

def draw_grid():
    screen.fill(BACKGROUND_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row, col]
            color = CELL_COLOR.get(value, (237, 204, 97))  # Default color for larger numbers
            x, y = col * (CELL_SIZE + GAP_SIZE) + GAP_SIZE, row * (CELL_SIZE + GAP_SIZE) + GAP_SIZE
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE), border_radius=5)
            if value > 0:
                text = font.render(str(value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_grid()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
