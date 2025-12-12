import pygame
from engine import GameState

def main():
    pygame.init()
    window_size = 1400 
    window = pygame.display.set_mode((window_size,window_size))
    window.fill('grey')
    running = True
    sq_size = window_size // 8
    images = loadImages(sq_size)
    game_state = GameState()
    print(game_state.board)
    redraw = True
    moves = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                loc = get_loc(pygame.mouse.get_pos(), sq_size)
                moves = game_state.handle_click(loc)
                redraw = True
            if event.type == pygame.MOUSEBUTTONUP:
                loc = get_loc(pygame.mouse.get_pos(), sq_size)
                game_state.click_move(loc, moves)
                moves = []
                redraw = True
            if event.type == pygame.QUIT:
                running = False
                break
        if not game_state.white_turn:
            game_state.bot_move()
            redraw = True
        if redraw:
            drawGame(window, sq_size, images, game_state, moves)
            pygame.display.flip()
            redraw = False
        if game_state.checkmate:
            draw_checkmate(window)
            pygame.display.flip()   

def loadImages(sq_size):
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load("assets/" + piece + ".png"), (sq_size, sq_size))
    return images

def drawGame(window, sq_size, images, game_state, moves):
    drawBoard(window, sq_size)
    drawMoves(window, sq_size, moves)
    drawPieces(window, sq_size, images, game_state)

def drawBoard(window, sq_size):
    colors = [(255,255,255), (125,215,100)] 
    for i in range(64):
        row = i // 8
        col = i % 8
        pygame.draw.rect(window, colors[(row+col)%2], (col*sq_size, row*sq_size, sq_size, sq_size)) 

def drawPieces(window, sq_size, image, game_state):
    for i in range(64):
        row = i // 8
        col = i % 8
        current = game_state.board[i]
        if current != "  ":
            window.blit(image[current], (col*sq_size, row*sq_size))

def drawMoves(window, sq_size, moves):
    alpha_surface = pygame.Surface(window.get_size(), pygame.SRCALPHA) 
    for move in moves:
        row, col = get_row_col(move.to_idx)
        pygame.draw.rect(alpha_surface, (0,0,0,128), (col*sq_size, row*sq_size, sq_size, sq_size))
    window.blit(alpha_surface, (0,0))

def draw_checkmate(window):
    font = pygame.font.SysFont("Arial", 50)
    window.blit(font.render("Checkmate", True, "red"), (200, 200))

def get_row_col(loc):
    return loc//8, loc%8

def get_loc(pos, sq_size):
    row = pos[1]//sq_size
    col = pos[0]//sq_size
    return (row*8 + col)

if __name__ == "__main__":
    main()
