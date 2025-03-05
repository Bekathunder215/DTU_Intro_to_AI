import pygame
import numpy as np
from constants import GRID_SIZE, CELL_SIZE, GAP_SIZE, WIDTH, HEIGHT, BACKGROUND_COLOR, TEXT_COLOR, CELL_COLOR

class Game:
    def __init__(self):
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    
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
        
        if direction == "left":
            self.grid = np.array([slide_and_merge(row) for row in self.grid])
        elif direction == "right":
            self.grid = np.array([slide_and_merge(row[::-1])[::-1] for row in self.grid])
        elif direction == "up":
            self.grid = np.transpose([slide_and_merge(row) for row in self.grid.T])
        elif direction == "down":
            self.grid = np.transpose([slide_and_merge(row[::-1])[::-1] for row in self.grid.T])
