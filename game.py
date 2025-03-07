import pygame
import numpy as np
from constants import GRID_SIZE, CELL_SIZE, GAP_SIZE, WIDTH, HEIGHT, BACKGROUND_COLOR, TEXT_COLOR, CELL_COLOR

class Game:
    def __init__(self):
        self.score = 0
        self.moves = 0
        self.resetgame()
    
    def score_function(self):
        return np.sum(self.grid)

    def resetgame(self):
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.grid[GRID_SIZE-1, GRID_SIZE-1] = 2
        self.moves = 0
        self.score = 0

    def add_tile(self):
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r, c] == 0]
        
        if empty_cells:
            r, c = empty_cells[np.random.randint(len(empty_cells))]
            # On the lines bellow we call np.random each time we do a check to introduce independent probabilities

            # Low score: 2 or 4
            if self.score < 100:
                self.grid[r, c] = 2 if np.random.random() < 0.9 else 4
            
            # Medium score: 2, 4, or 8
            elif self.score < 500:
                self.grid[r, c] = 2 if np.random.random() < 0.7 else (4 if np.random.random() < 0.6 else 8)
            
            # High score: 2, 4, 8, or 16
            elif self.score < 1000:
                self.grid[r, c] = 2 if np.random.random() < 0.6 else (4 if np.random.random() < 0.5 else (8 if np.random.random() < 0.4 else 16))
            
            # Very high score: 2, 4, 8, 16, or 32
            else:
                self.grid[r, c] = 2 if np.random.random() < 0.5 else (4 if np.random.random() < 0.4 else (8 if np.random.random() < 0.3 else (16 if np.random.random() < 0.2 else 32)))


    def move(self, direction):
        def slide_and_merge(row):
            non_zero = [num for num in row if num != 0]  # Remove zeros
            new_row = []
            skip = False
            for i in range(len(non_zero)):
                if skip:
                    skip = False
                    continue
                if i < len(non_zero) - 1 and non_zero[i] == non_zero[i + 1]:
                    new_row.append(non_zero[i] * 2)
                    skip = True  # Skip the next tile since it's merged
                else:
                    new_row.append(non_zero[i])
            return new_row + [0] * (GRID_SIZE - len(new_row))  # Fill with zeros
        
        old_grid = self.grid.copy()
        if direction == "left":
            self.grid = np.array([slide_and_merge(row) for row in self.grid])
        elif direction == "right":
            self.grid = np.array([slide_and_merge(row[::-1])[::-1] for row in self.grid])
        elif direction == "up":
            self.grid = np.transpose([slide_and_merge(row) for row in self.grid.T])
        elif direction == "down":
            self.grid = np.transpose([slide_and_merge(row[::-1])[::-1] for row in self.grid.T])

        if not np.array_equal(old_grid, self.grid):
            self.moves +=1
            self.score = self.score_function()
            self.add_tile()