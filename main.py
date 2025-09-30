import pygame
from pawn import Pawn
from board import Board
from king import King
from bishop import Bishop
from rook import Rook
from queen import Queen
from knight import Knight

def main():
    pygame.init()
    window_size = 1400
    window = pygame.display.set_mode((window_size,window_size))
    window.fill('grey')
    board = Board("white", window_size)
    running = True
    turn = "white"
    white_pieces = pygame.sprite.Group()
    black_pieces = pygame.sprite.Group()
    board.draw(window)
    new_game(board, white_pieces, black_pieces)
    white_pieces.draw(window)   
    black_pieces.draw(window)
    for i in range(8): 
        print(board.pieces[i])
    
    current_piece = None
    moves = []
    while running:
        for event in pygame.event.get():
            if turn == "white":
                pieces = white_pieces
            else:
                pieces = black_pieces
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for piece in pieces:
                    if piece.rect.collidepoint(pos):
                        moves = piece.possible_moves(board.pieces)
                        current_piece = piece
                
                board.draw(window)
                if len(moves) > 0:
                    board.draw_moves(window, moves)
                        #current_piece = (piece.x, piece.y)
                white_pieces.draw(window)
                black_pieces.draw(window)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for move in moves:
                    x_pos = move[0]*board.square_size+20
                    y_pos = move[1]*board.square_size+20
                    sq = pygame.Rect(x_pos, y_pos, board.square_size, board.square_size)
                    if sq.collidepoint(pos):
                        board.update_pieces(current_piece, move)
                        #current_piece.update(move, board.square_size)
                        moves = []
                        current_piece = None
                        if turn == "white":
                            turn = "black"
                        else:
                            turn = "white"
                        break
                board.draw(window)
                white_pieces.draw(window)
                black_pieces.draw(window)
            if event.type == pygame.QUIT:
                running = False
                break
            pygame.display.update()

    
def new_game(board, white_pieces, black_pieces):
    board.pieces[1][0] = Pawn("black", 0, 1, board.square_size)
    board.pieces[1][1] = Pawn("black", 1, 1, board.square_size)
    board.pieces[1][2] = Pawn("black", 2, 1, board.square_size)
    board.pieces[1][3] = Pawn("black", 3, 1, board.square_size)
    board.pieces[1][4] = Pawn("black", 4, 1, board.square_size)
    board.pieces[1][5] = Pawn("black", 5, 1, board.square_size)
    board.pieces[1][6] = Pawn("black", 6, 1, board.square_size)
    board.pieces[1][7] = Pawn("black", 7, 1, board.square_size)
                                           
    board.pieces[6][0] = Pawn("white", 0, 6, board.square_size)
    board.pieces[6][1] = Pawn("white", 1, 6, board.square_size)
    board.pieces[6][2] = Pawn("white", 2, 6, board.square_size)
    board.pieces[6][3] = Pawn("white", 3, 6, board.square_size)
    board.pieces[6][4] = Pawn("white", 4, 6, board.square_size)
    board.pieces[6][5] = Pawn("white", 5, 6, board.square_size)
    board.pieces[6][6] = Pawn("white", 6, 6, board.square_size)
    board.pieces[6][7] = Pawn("white", 7, 6, board.square_size)

    board.pieces[0][4] = King("black", 4, 0, board.square_size)
    board.pieces[7][4] = King("white", 4, 7, board.square_size)

    board.pieces[0][3] = Queen("black", 3, 0, board.square_size)
    board.pieces[7][3] = Queen("white", 3, 7, board.square_size)

    board.pieces[0][0] = Rook("black", 0, 0, board.square_size)
    board.pieces[0][7] = Rook("black", 7, 0, board.square_size)
    board.pieces[7][0] = Rook("white", 0, 7, board.square_size)
    board.pieces[7][7] = Rook("white", 7, 7, board.square_size)

    board.pieces[0][2] = Bishop("black", 2, 0, board.square_size)
    board.pieces[0][5] = Bishop("black", 5, 0, board.square_size)
    board.pieces[7][2] = Bishop("white", 2, 7, board.square_size)
    board.pieces[7][5] = Bishop("white", 5, 7, board.square_size)

    board.pieces[0][1] = Knight("black", 1, 0, board.square_size)
    board.pieces[0][6] = Knight("black", 6, 0, board.square_size)
    board.pieces[7][1] = Knight("white", 1, 7, board.square_size)
    board.pieces[7][6] = Knight("white", 6, 7, board.square_size)
    
    for i in range(8):
        for j in range(8):
            if board.pieces[i][j] != None:
                if board.pieces[i][j].color == "black":
                    black_pieces.add(board.pieces[i][j])
                else:
                    white_pieces.add(board.pieces[i][j])


if __name__ == "__main__":
    main()
