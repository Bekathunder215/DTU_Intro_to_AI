import pygame
import numpy as np
from constants import GRID_SIZE, CELL_SIZE, GAP_SIZE, WIDTH, HEIGHT, BACKGROUND_COLOR, TEXT_COLOR, CELL_COLOR

class UI:
    def __init__(self, game):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048 Game")
        self.font = pygame.font.Font(None, 50)
        self.game = game

    def draw_grid(self):
        self.screen.fill(BACKGROUND_COLOR)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = self.game.grid[row, col]
                color = CELL_COLOR.get(value, (237, 204, 97))
                x, y = col * (CELL_SIZE + GAP_SIZE) + GAP_SIZE, row * (CELL_SIZE + GAP_SIZE) + GAP_SIZE
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE), border_radius=5)
                if value > 0:
                    text = self.font.render(str(value), True, TEXT_COLOR)
                    text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    self.screen.blit(text, text_rect)
        
    def update(self):
        self.draw_grid()
        pygame.display.flip()
