import pygame
import numpy as np
from constants import GRID_SIZE, CELL_SIZE, GAP_SIZE, WIDTH, HEIGHT, BACKGROUND_COLOR, TEXT_COLOR, CELL_COLOR

class UI:
    def __init__(self, game):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048 Game")
        self.font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 30)
        self.game = game
        self.start_time = None
        self.moves = 0

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
    
    def draw_button(self, text, x, y, width, height, color, action=None):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect, border_radius=5)

        # Render text
        text_surf = self.font.render(text, True, (0, 0, 0))  # Black text
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

        # Check for click event
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(event.pos):
                if action:
                    action()


    def reset(self):
        self.game.grid = np.zeroes((GRID_SIZE,GRID_SIZE), dtype=int)
        self.start_time = None
        self.moves = 0
    
    def benchmark(self):
        if self.start_time is None:
            self.start_time = time.time()
        
        time = time.time() - self.start_time
        print(f"Time: {elapsed_time:.2f} sec, Moves: {self.moves}")
    
    def ai(self):
        print("USE AI")

    def update(self):
        self.draw_grid()
        self.draw_button("Use AI", 50, HEIGHT + 20, 100, 50, (150, 150, 255), self.use_ai)
        self.draw_button("Reset", WIDTH // 2 - 50, HEIGHT + 20, 100, 50, (255, 100, 100), self.reset_game)
        self.draw_button("Benchmark", WIDTH - 150, HEIGHT + 20, 120, 50, (100, 255, 100), self.benchmark)
        pygame.display.flip()

