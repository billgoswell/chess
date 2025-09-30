import pygame

class Board:
    def __init__(self, player_color, board_size):
        self.player_color = player_color
        self.white_sq_color = (255,255,255)
        self.black_sq_color = (125,215,100)
        self.border = 20
        self.square_size = (board_size - self.border*2)/8
        self.pieces = [[None]*8 for i in range(8)]

    def draw(self, window):
        if self.player_color == "white":
            color = self.white_sq_color
        else:
            color = self.black_sq_color
        for i in range(8):
            x_val = self.border + i*self.square_size
            for j in range(8):
                y_val = self.border + j*self.square_size
                pygame.draw.rect(window, color, (x_val, y_val, self.square_size, self.square_size))
                if j == 7:
                    break
                elif color == self.white_sq_color:
                    color = self.black_sq_color
                else:
                    color = self.white_sq_color

    def draw_moves(self, window, moves):
        for move in moves:
            x_val = self.border + move[0]*self.square_size
            y_val = self.border + move[1]*self.square_size
            pygame.draw.rect(window, 'red', (x_val, y_val, self.square_size, self.square_size))

    def update_pieces(self, piece, move):
        if self.pieces[move[1]][move[0]] != None:
            captured_piece = self.pieces[move[1]][move[0]]
            captured_piece.kill()
        self.pieces[piece.y][piece.x] = None
        self.pieces[move[1]][move[0]] = piece
        piece.update(move, self.square_size)

