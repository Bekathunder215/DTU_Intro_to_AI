import pygame
import numpy as np
from constants import GRID_SIZE, CELL_SIZE, GAP_SIZE, WIDTH, HEIGHT, BACKGROUND_COLOR, TEXT_COLOR, CELL_COLOR
from game import Game, AI
from ui import UI

def main():
    pygame.init()
    game = Game()
    ai = AI(game)
    ui = UI(game, ai)
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
        if ui.ai_running:
            best_move = ai.find_best_move(game.grid, 4)
            game.move(best_move)
        ui.update()
    pygame.quit()
    
if __name__ == "__main__":
    main()
