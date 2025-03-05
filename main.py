import pygame
import numpy as np
from constants import GRID_SIZE, CELL_SIZE, GAP_SIZE, WIDTH, HEIGHT, BACKGROUND_COLOR, TEXT_COLOR, CELL_COLOR
from game import Game
from ui import UI

def main():
    game = Game()
    ui = UI(game)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        ui.update()
    pygame.quit()

if __name__ == "__main__":
    main()
