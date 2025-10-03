import pygame
from board import Board

def main():
    pygame.init()
    window_size = 700 
    window = pygame.display.set_mode((window_size,window_size))
    window.fill('grey')
    board = Board(window, "white", window_size)
    running = True
    board.new_game()
    board.draw()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.handle_mouseclick()
            if event.type == pygame.MOUSEBUTTONUP:
                board.make_move()
            if event.type == pygame.QUIT:
                running = False
                break
            pygame.display.update()

if __name__ == "__main__":
    main()
