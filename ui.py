import pygame
import numpy as np
import time
from typing import Optional, Callable
from constants import GRID_SIZE, CELL_SIZE, GAP_SIZE, WIDTH, HEIGHT, BACKGROUND_COLOR, TEXT_COLOR, CELL_COLOR

class UI:
    def __init__(self, game: "Game_class", ai: "AI_class") -> None:
        """
        Initializes the UI for the 2048 game.

        Args:
            game (Game): The game instance.
            ai (AI): The AI instance.
        """
    # def __init__(self, game, ai):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))
        pygame.display.set_caption("2048 Game")
        self.font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 30)
        self.game = game
        self.start_time = None
        self.moves = game.moves
        self.miniai = ai
        self.ai_running = False

    def draw_grid(self) -> None:
        """
        Draws the game grid on the screen.
        """
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
    
    # def draw_button(self, text, x, y, width, height, color, action=None):
    def draw_button(self, text: str, x: int, y: int, width: int, height: int, 
                    color: tuple[int, int, int], action: Optional[Callable[[], None]] = None) -> None:
        """
        Draws a button on the screen and handles clicks.

        Args:
            text (str): The text to display on the button.
            x (int): The x-coordinate of the button.
            y (int): The y-coordinate of the button.
            width (int): The width of the button.
            height (int): The height of the button.
            color (tuple[int, int, int]): The RGB color of the button.
            action (Optional[Callable[[], None]]): The function to call when the button is clicked.
        """
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect, border_radius=5)

        text_surf = self.font.render(text, True, (0, 0, 0))  
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if action:
                action()
                pygame.time.wait(150)  # Small delay to prevent multiple calls
            
    def reset(self) -> None:
        """
        Resets the game to its initial state.
        """
        self.game.__init__()
        self.start_time = None
        self.moves = self.game.moves
        if self.ai_running:
            self.ai_toggle()
    
    def benchmark(self) -> None:
        """
        Measures and prints the elapsed time and number of moves since the AI started.
        """
        if self.start_time is None:
            self.start_time = time.time()
        
        elapsed = time.time() - self.start_time
        print(f"Time: {elapsed:.2f} sec, Moves: {self.moves}")
    
    def ai_toggle(self) -> None:
        """
        Toggles the AI on and off.
        """
        self.ai_running = not self.ai_running
        if self.ai_running:
            print("Enabled")
            pygame.display.set_caption("2048 Game (AI Enabled)")
        else:
            print("Disabled")
            pygame.display.set_caption("2048 Game")


    def update(self) -> None:
        """
        Updates the UI by drawing the grid and buttons, and refreshing the display.
        """
        self.draw_grid()
        self.draw_button("Use AI", 50, HEIGHT + 20, 100, 50, (150, 150, 255), self.ai_toggle)
        self.draw_button("Reset", WIDTH // 2 - 50, HEIGHT + 20, 100, 50, (255, 100, 100), self.reset)
        self.draw_button("Benchmark", WIDTH - 150, HEIGHT + 20, 120, 50, (100, 255, 100), self.benchmark)

        pygame.display.flip()

