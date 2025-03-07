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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move("left")
                elif event.key == pygame.K_RIGHT:
                    game.move("right")
                elif event.key == pygame.K_UP:
                    game.move("up")
                elif event.key == pygame.K_DOWN:
                    game.move("down")
                ui.moves += 1
        ui.update()
    pygame.quit()
    
if __name__ == "__main__":
    main()
