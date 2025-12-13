import random
from dataclasses import dataclass
from enum import Enum

WHITE = "w"
BLACK = "b"

class Pieces:
    ROOK = "R"
    KNIGHT = "N"
    BISHOP = "B"
    KING = "K"
    QUEEN = "Q"
    PAWN = "p"

class MoveType(Enum):
    MOVE = "move"
    CAPTURE = "capture"
    DOUBLE = "double"
    EN_PASSANT = "en_passant"
    PROMOTION = "promotion"

@dataclass
class Move:
    piece: str
    from_idx: int
    to_idx: int
    move_type: MoveType
    captured: str | None  = None

class GameState():
    def __init__(self):
        self.board = ["bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR",
                      "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp",
                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
                      "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp",
                      "wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR"]
#        self.board = [
#                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
#                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
#                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
#                      "  ", "  ", "  ", "wN", "  ", "  ", "  ", "  ",
#                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
#                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
#                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
#                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "
#                    ]
        self.white_turn = True
        self.move_history = []
        self.captured_pieces = []
        self.white_king = 59 
        self.black_king = 3
        self.moves = []
        self.checkmate = False
        
    def verify_moves(self, moves: list[Move]) -> list[Move]:
        verified_moves = []
        if len(moves) == 0:
            return []
        for move in moves:
            if self.verify_move(move):
                verified_moves.append(move)
        return verified_moves

    def verify_move(self, move: Move) -> bool:
        legal = True
        self.make_move(move)
        if self.white_turn:
            enemy_moves = self.get_black_moves()
            king_loc = self.white_king
        else:
            enemy_moves = self.get_white_moves()
            king_loc = self.black_king
        for m in enemy_moves:
            if m.to_idx == king_loc:
                legal = False
                break
        self.undo_move(move)
        return legal

    def get_white_moves(self) -> list[Move]:
        all_white_moves = []
        for i in range(64):
            if self.board[i][0] == WHITE:
                all_white_moves.extend(self.get_moves(self.board[i], i))
        return all_white_moves

    def get_black_moves(self) -> list[Move]:
        all_black_moves = []
        for i in range(64):
            if self.board[i][0] == BLACK:
                all_black_moves.extend(self.get_moves(self.board[i], i))
        return all_black_moves

    def click_move(self, loc: int, moves: list[Move]):
        for move in moves:
            if move.to_idx == loc:
                self.make_move(move)
                self.move_history.append(move)
                self.switch_turn()
                
    def make_move(self, move: Move):
            if move.move_type == MoveType.CAPTURE:
                self.captured_pieces.append(self.board[move.to_idx])
            if move.move_type == MoveType.EN_PASSANT:
                if self.white_turn:
                    self.captured_pieces.append(self.board[move.to_idx+8])
                    self.board[move.to_idx+8] = "  "
                else:
                    self.captured_pieces.append(self.board[move.to_idx-8])
                    self.board[move.to_idx-8] = "  "
            if move.piece[1] == Pieces.KING:
                if move.piece[0] == WHITE:
                    self.white_king = move.to_idx
                else:
                    self.black_king = move.to_idx
            self.board[move.to_idx] = move.piece
            self.board[move.from_idx] = "  "

    def undo_move(self, move: Move):
        self.board[move.from_idx] = move.piece
        self.board[move.to_idx] = "  "
        if move.piece[1] == Pieces.KING:
            if move.piece[0] == WHITE:
                self.white_king = move.from_idx
            else:
                self.black_king = move.from_idx
        if move.move_type == MoveType.CAPTURE:
            self.board[move.to_idx] = self.captured_pieces.pop()
        if move.move_type == MoveType.EN_PASSANT:
            if move.piece == "wp":
                self.board[move.to_idx+8] = self.captured_pieces.pop()
            if move.piece == "bp":
                self.board[move.to_idx-8] = self.captured_pieces.pop()

    def handle_click(self, loc: int) -> list[Move]:
        piece = self.board[loc]
        if (piece[0] == BLACK) and self.white_turn:
            return [] 
        if (piece[0] == WHITE) and not self.white_turn: 
            return []
        moves = self.get_moves(piece, loc)
        verified_moves = self.verify_moves(moves)
        return verified_moves

        
    def get_moves(self, piece: str, loc: int) -> list[Move]:
        moves = [] 
        match piece[1]:
            case " ":
                return [] 
            case Pieces.PAWN:
                if piece[0] == "w":
                    moves =  self.wp_moves(piece, loc)
                else:
                    moves = self.bp_moves(piece, loc)
            case Pieces.ROOK:
                moves = self.rook_moves(piece, loc)
            case Pieces.BISHOP:
                moves = self.bishop_moves(piece, loc)
            case Pieces.QUEEN:
                moves =  self.queen_moves(piece, loc)
            case Pieces.KING:
                moves = self.king_moves(piece, loc)
            case Pieces.KNIGHT:
                moves = self.knight_moves(piece, loc)
        return moves

    def move(self, piece: str, loc1: int, loc2: int, moves: list[Move]) -> tuple[list[Move], bool]:
        b = False
        if self.board[loc2] == "  ":
            moves.append(Move(piece, loc1, loc2, MoveType.MOVE))
        elif self.board[loc2][0] != piece[0]:
            moves.append(Move(piece, loc1, loc2, MoveType.CAPTURE))
            b = True
        else:
            b = True
        return moves, b

    def knight_moves(self, piece: str, loc: int) -> list[Move]:
        moves = []
        row = loc//8
        col = loc%8
        if row+2 <= 7:
            if col+1 <= 7:
                moves, _ = self.move(piece, loc, loc+17, moves)
            if col-1 >= 0:
                moves, _ = self.move(piece, loc, loc+15, moves)
        if row-2 >= 0:
            if col+1 <= 7:
                moves, _ = self.move(piece, loc, loc-15, moves)
            if col-1 >= 0:
                moves, _ = self.move(piece, loc, loc-17, moves)
        if col+2 <= 7:
            if row+1 <= 7:
                moves, _ = self.move(piece, loc, loc+10, moves)
            if row-1 >= 0:
                moves, _ = self.move(piece, loc, loc-6, moves)
        if col-2 >= 0:
            if row+1 <= 7:
                moves, _ = self.move(piece, loc, loc+6, moves)
            if row-1 >= 0:
                moves, _ = self.move(piece, loc, loc-10, moves)
        return moves

    def rook_moves(self, piece: str, loc: int) -> list[Move]:
        moves = []
        row = loc//8
        col = loc%8
        for i in range(1, 8-col):
            moves, b = self.move(piece, loc, loc+i, moves)
            if b:
                break
        for i in range(1, col+1):
            moves, b = self.move(piece, loc, loc-i, moves)
            if b:
                break
        for i in range(1, 8-row):
            moves, b = self.move(piece, loc, loc+i*8, moves)
            if b:
                break
        for i in range(1, row+1):
            moves, b = self.move(piece, loc, loc-i*8, moves)
            if b:
                break
        return moves

    def bishop_moves(self, piece: str, loc: int) -> list[Move]:
        moves = []
        row = loc//8
        col = loc%8
        for i in range(1, 8-max(row,col)):
            moves, b = self.move(piece, loc, loc+i*9, moves)
            if b:
                break
        for i in range(1, min(row+1, 8-col)):
            moves, b = self.move(piece, loc, loc-i*7, moves)
            if b:
                break
        for i in range(1, min(8-row, col+1)):
            moves, b = self.move(piece, loc, loc+i*7, moves)
            if b:
                break
        for i in range(1, min(row, col)+1):
            moves, b = self.move(piece, loc, loc-i*9, moves)
            if b:
                break
        return moves

    def queen_moves(self, piece: str, loc: int) -> list[Move]:
        moves = self.bishop_moves(piece, loc)
        moves.extend(self.rook_moves(piece, loc))
        return moves

    def king_moves(self, piece: str, loc: int) -> list[Move]:
        moves = []
        row = loc//8
        col = loc%8
        if row-1 >= 0:
            moves, _ = self.move(piece, loc, loc-8, moves)
            if col-1 >= 0:
                moves, _ = self.move(piece, loc, loc-9, moves)
            if col+1 <= 7:
                moves, _ = self.move(piece, loc, loc-7, moves)
        if row+1 <= 7:
            moves, _ = self.move(piece, loc, loc+8, moves)
            if col-1 >= 0:
                moves, _ = self.move(piece, loc, loc+7, moves)
            if col+1 <= 7:
                moves, _ = self.move(piece, loc, loc+9, moves)
        if col-1 >= 0:
            moves, _ = self.move(piece, loc, loc-1, moves)
        if col+1 <= 7:
            moves, _ = self.move(piece, loc, loc+1, moves)
        return moves

    def wp_moves(self, piece, loc):
        moves = []
        row = loc//8
        col = loc%8
        if row == 1:
            return self.check_promo(piece, loc)
        if self.board[loc-8] == "  ":
            moves.append(Move(piece, loc, loc-8, MoveType.MOVE))
            if row == 6:
                if self.board[loc-16] == "  ":
                    moves.append(Move(piece, loc, loc-16, MoveType.DOUBLE))
        if col < 7:
            if self.board[loc-7][0] == "b":
                moves.append(Move(piece, loc, loc-7, MoveType.CAPTURE))
        if col > 0:
            if self.board[loc-9][0] == "b":
                moves.append(Move(piece, loc, loc-9, MoveType.CAPTURE))
        if row == 3:
            if self.move_history[-1].move_type == MoveType.DOUBLE:
                l = self.move_history[-1].to_idx
                if loc+1 == l:
                    moves.append(Move(piece, loc, loc-7, MoveType.EN_PASSANT))
                if loc-1 == l:
                    moves.append(Move(piece, loc, loc-9, MoveType.EN_PASSANT))
        return moves
        
                        
    def bp_moves(self, piece: str, loc: int) -> list[Move]:
        moves = []
        row = loc//8
        col = loc%8
        if row == 6:
            return self.check_promo(piece, loc)
        if self.board[loc+8] == "  ":
            moves.append(Move(piece, loc, loc+8, MoveType.MOVE))
            if row == 1:
                if self.board[loc+16] == "  ":
                    moves.append(Move(piece, loc, loc+16, MoveType.DOUBLE))
        if col < 7:
            if self.board[loc+9][0] == "w":
                moves.append(Move(piece, loc, loc+9, MoveType.CAPTURE))
        if col > 0:
            if self.board[loc+7][0] == "w":
                moves.append(Move(piece, loc, loc+7, MoveType.CAPTURE))
        if row == 4:
            if self.move_history[-1].move_type == MoveType.DOUBLE:
                l = self.move_history[-1].to_idx
                if loc+1 == l:
                    moves.append(Move(piece, loc, loc+9, MoveType.EN_PASSANT))
                if loc-1 == l:
                    moves.append(Move(piece, loc, loc+7, MoveType.EN_PASSANT))
        return moves

    def check_promo(self, piece: str, loc: int) -> Move:
        pass
    
    def bot_move(self):
        if len(self.moves) == 0:
            return
        self.easy_bot()

    def easy_bot(self):
        captures = []
        for move in self.moves:
            if move.move_type == MoveType.CAPTURE:
                captures.append(move)
        if len(captures) != 0:
            self.rand_move(captures)
        else:
            self.rand_move(self.moves)

    def rand_move(self, moves: list[Move]):
        move = random.choice(moves)
        self.make_move(move)
        self.switch_turn()

    def switch_turn(self):
        self.white_turn = not self.white_turn
        if self.white_turn:
            moves = self.get_white_moves()
        else:
            moves = self.get_black_moves()
        self.moves = self.verify_moves(moves)
        if len(self.moves) == 0:
            self.checkmate = True

