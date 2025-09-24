import pygame
from board import Board

def main():
    pygame.init()
    window = pygame.display.set_mode((720,720))
    board = Board("black")
    running = True
    board.draw(window)
    board.draw_pawn(window, 0, 1)
    board.draw_bishop(window, 0, 2)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            pygame.display.update()

if __name__ == "__main__":
    main()
