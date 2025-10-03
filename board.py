import pygame

from pawn import Pawn
from king import King
from bishop import Bishop
from rook import Rook
from queen import Queen
from knight import Knight

class Board:
    def __init__(self, window, player_color, board_size):
        self.board_size = board_size
        self.player_color = player_color
        self.white_sq_color = (255,255,255)
        self.black_sq_color = (125,215,100)
        self.border = 20
        self.square_size = (board_size - self.border*2)/8
        self.pieces = [[None]*8 for i in range(8)]
        self.black_pieces = pygame.sprite.Group()
        self.white_pieces = pygame.sprite.Group()
        self.turn = "white"
        self.window = window
        self.current_piece = None
        self.moves = []
        self.move_history = []
        self.black_king = None
        self.white_king = None
        self.all_blackmoves = []
        self.all_whitemoves = []

    def black_moves(self):
        self.all_blackmoves = []
        for piece in self.black_pieces:
            if piece.captured == False:
                moves = piece.possible_moves(self.pieces)
                self.all_blackmoves.extend(moves)

    def white_moves(self):
        self.all_whitemoves = []
        for piece in self.white_pieces:
            if piece.captured == False:
                moves = piece.possible_moves(self.pieces)
                self.all_whitemoves.extend(moves)

    def verify_move(self, move, piece):
        good = True
        x = piece.x
        y = piece.y
        captured_piece = None
        if self.pieces[move[1]][move[0]] != None:
            captured_piece = self.pieces[move[1]][move[0]]
            captured_piece.captured = True
        self.pieces[y][x] = None
        self.pieces[move[1]][move[0]] = piece
        if piece.color  == "white":
            king_loc = (self.white_king.x, self.white_king.y)
            self.black_moves()
            enemy_moves = self.all_blackmoves
        else:
            king_loc = (self.black_king.x, self.black_king.y)
            self.white_moves()
            enemy_moves = self.all_whitemoves
        if isinstance(piece, King):
            king_loc = move

        for m in enemy_moves:
            if m == king_loc:
                good = False
                break
        if captured_piece != None:
            captured_piece.captured = False
        self.pieces[move[1]][move[0]] = captured_piece
        self.pieces[y][x] = piece
        return good
        
    def draw(self):
        if self.player_color == "white":
            color = self.white_sq_color
        else:
            color = self.black_sq_color
        for i in range(8):
            x_val = self.border + i*self.square_size
            for j in range(8):
                y_val = self.border + j*self.square_size
                pygame.draw.rect(self.window, color, (x_val, y_val, self.square_size, self.square_size))
                if j == 7:
                    break
                elif color == self.white_sq_color:
                    color = self.black_sq_color
                else:
                    color = self.white_sq_color
        self.black_pieces.draw(self.window)

        self.white_pieces.draw(self.window)

    def draw_moves(self, piece):
        if piece == None:
            return
        for move in piece.moves:
            x_val = self.border + move[0]*self.square_size
            y_val = self.border + move[1]*self.square_size
            alpha_surface = pygame.Surface((self.board_size, self.board_size), pygame.SRCALPHA)
            pygame.draw.rect(alpha_surface, (0,0,0,128), (x_val, y_val, self.square_size, self.square_size))
            self.window.blit(alpha_surface, (0, 0))

    def update_pieces(self, piece, move):
        if self.pieces[move[1]][move[0]] != None:
            captured_piece = self.pieces[move[1]][move[0]]
            captured_piece.kill()
        self.pieces[piece.y][piece.x] = None
        self.pieces[move[1]][move[0]] = piece
        piece.update(move, self.square_size)

    def handle_mouseclick(self):
        if self.turn == "white":
            pieces = self.white_pieces
        else:
            pieces = self.black_pieces
        pos = pygame.mouse.get_pos()
        self.current_piece = None
        for piece in pieces:
            if piece.rect.collidepoint(pos):
                self.current_piece = piece
        self.draw()
        self.draw_moves(self.current_piece)

    def make_move(self):
        pos = pygame.mouse.get_pos()
        print(self.current_piece)
        if self.current_piece == None:
            return
        for move in self.current_piece.moves:
            x_pos = move[0]*self.square_size+20
            y_pos = move[1]*self.square_size+20
            sq = pygame.Rect(x_pos, y_pos, self.square_size, self.square_size)
            if sq.collidepoint(pos):
                self.update_pieces(self.current_piece, move)
                self.move_history.append(move)
                self.switch_turn()
#                if self.turn == "white":
#                    self.turn = "black"
#                else:
#                    self.turn = "white"
#                self.white_moves()
#                self.black_moves()
        self.moves = []
        self.current_piece = None
        self.draw()

    def switch_turn(self):
        if self.turn == "white":
            self.turn = "black"
            for piece in self.black_pieces:
                verified_moves = []
                moves = piece.possible_moves(self.pieces)
                for move in moves:
                    if self.verify_move(move, piece):
                        verified_moves.append(move)
                piece.moves = verified_moves
                self.all_blackmoves.extend(verified_moves)
        else:
            self.turn = "white"
            for piece in self.white_pieces:
                verified_moves = []
                moves = piece.possible_moves(self.pieces)
                for move in moves:
                    if self.verify_move(move, piece):
                        verified_moves.append(move)
                piece.moves = verified_moves
                self.all_whitemoves.extend(verified_moves)


    def new_game(self):
        self.move_history = []
        self.pieces = [[None]*8 for i in range(8)]
        for i in range(8):
            self.pieces[6][i] = Pawn("white", i, 6, self.square_size)
            self.pieces[1][i] = Pawn("black", i, 1, self.square_size)
        
        self.pieces[0][4] = King("black", 4, 0, self.square_size)
        self.pieces[7][4] = King("white", 4, 7, self.square_size)
        self.white_king = self.pieces[7][4]
        self.black_king = self.pieces[0][4]

        self.pieces[0][3] = Queen("black", 3, 0, self.square_size)
        self.pieces[7][3] = Queen("white", 3, 7, self.square_size)

        self.pieces[0][0] = Rook("black", 0, 0, self.square_size)
        self.pieces[0][7] = Rook("black", 7, 0, self.square_size)
        self.pieces[7][0] = Rook("white", 0, 7, self.square_size)
        self.pieces[7][7] = Rook("white", 7, 7, self.square_size)

        self.pieces[0][2] = Bishop("black", 2, 0, self.square_size)
        self.pieces[0][5] = Bishop("black", 5, 0, self.square_size)
        self.pieces[7][2] = Bishop("white", 2, 7, self.square_size)
        self.pieces[7][5] = Bishop("white", 5, 7, self.square_size)

        self.pieces[0][1] = Knight("black", 1, 0, self.square_size)
        self.pieces[0][6] = Knight("black", 6, 0, self.square_size)
        self.pieces[7][1] = Knight("white", 1, 7, self.square_size)
        self.pieces[7][6] = Knight("white", 6, 7, self.square_size)
        
        for i in range(8):
            for j in range(8):
                if self.pieces[i][j] != None:
                    if self.pieces[i][j].color == "black":
                        self.black_pieces.add(self.pieces[i][j])
                    else:
                        self.white_pieces.add(self.pieces[i][j])

        self.black_moves()
        self.white_moves()

