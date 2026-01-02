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
    CASTLE_KING = "castle_king"
    CASTLE_QUEEN = "castle_queen"

@dataclass
class Move:
    piece: str
    from_idx: int
    to_idx: int
    move_type: MoveType
    prev_halfmove_clock: int
    captured: str | None  = None
    promotion_piece: str | None = None
    castling_rights: tuple | None = None

class GameState():
    def __init__(self):
        self.board = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR",
                      "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp",
                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
                      "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ",
                      "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp",
                      "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
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
        self.white_king = 60 
        self.black_king = 4
        self.moves = []
        self.checkmate = False
        self.stalemate = False
        self.game_over = False
        self.winner = None
        self.white_king_moved = False
        self.white_rook_kingside_moved = False
        self.white_rook_queenside_moved = False
        self.black_king_moved = False
        self.black_rook_kingside_moved = False
        self.black_rook_queenside_moved = False
        self.halfmove_clock = 0
        
    def create_move(self, piece: str, from_idx: int, to_idx: int, move_type: MoveType,
                     captured: str | None = None, promotion_piece: str | None = None) -> Move:
        return Move(piece, from_idx, to_idx, move_type, self.halfmove_clock, captured, promotion_piece,
                    castling_rights=(self.white_king_moved,
                                     self.white_rook_kingside_moved,
                                     self.white_rook_queenside_moved,
                                     self.black_king_moved,
                                     self.black_rook_kingside_moved,
                                     self.black_rook_queenside_moved))

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

    def get_white_moves(self, include_castling: bool = True) -> list[Move]:
        all_white_moves = []
        for i in range(64):
            if self.board[i][0] == WHITE:
                all_white_moves.extend(self.get_moves(self.board[i], i, include_castling))
        return all_white_moves

    def get_black_moves(self, include_castling: bool = True) -> list[Move]:
        all_black_moves = []
        for i in range(64):
            if self.board[i][0] == BLACK:
                all_black_moves.extend(self.get_moves(self.board[i], i, include_castling))
        return all_black_moves

    def click_move(self, loc: int, moves: list[Move]):
        for move in moves:
            if move.to_idx == loc:
                self.make_move(move)
                self.move_history.append(move)
                self.switch_turn()
                
    def make_move(self, move: Move):
        if move.piece[1] == Pieces.PAWN or move.move_type == MoveType.CAPTURE:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
        if move.piece == "wK":
            self.white_king_moved = True
            self.white_king = move.to_idx
        elif move.piece == "bK":
            self.black_king_moved = True
            self.black_king = move.to_idx
        elif move.piece == "wR":
            if move.from_idx == 63:
                self.white_rook_kingside_moved = True
            elif move.from_idx == 56:
                self.white_rook_queenside_moved = True
        elif move.piece == "bR":
            if move.from_idx == 7:
                self.black_rook_kingside_moved = True
            elif move.from_idx == 0:
                self.black_rook_queenside_moved = True
        if move.move_type == MoveType.CAPTURE:
            self.captured_pieces.append(self.board[move.to_idx])
        if move.move_type == MoveType.EN_PASSANT:
            if self.white_turn:
                self.captured_pieces.append(self.board[move.to_idx+8])
                self.board[move.to_idx+8] = "  "
            else:
                self.captured_pieces.append(self.board[move.to_idx-8])
                self.board[move.to_idx-8] = "  "
        if move.move_type == MoveType.CASTLE_KING:
            if move.piece == "wK":
                self.board[61] = "wR"
                self.board[63] = "  "
            if move.piece == "bK":
                self.board[5] = "bR"
                self.board[7] = "  "
        if move.move_type == MoveType.CASTLE_QUEEN:
            if move.piece == "wK":
                self.board[59] = "wR"
                self.board[56] = "  "
            if move.piece == "bK":
                self.board[3] = "bR"
                self.board[0] = "  "
        self.board[move.to_idx] = move.piece
        self.board[move.from_idx] = "  "
        if move.move_type == MoveType.PROMOTION:
            if move.piece[0] == WHITE:
                self.board[move.to_idx] = "wQ"
            if move.piece[0] == BLACK:
                self.board[move.to_idx] = "bQ"

    def undo_move(self, move: Move):
        if move.castling_rights:
            (self.white_king_moved,
             self.white_rook_kingside_moved,
             self.white_rook_queenside_moved,
             self.black_king_moved,
             self.black_rook_kingside_moved,
             self.black_rook_queenside_moved) = move.castling_rights
        self.halfmove_clock = move.prev_halfmove_clock
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
        if move.move_type == MoveType.CASTLE_KING:
            if move.piece == "wK":
                self.board[63] = "wR"
                self.board[61] = "  "
            if move.piece == "bK":
                self.board[7] = "bR"
                self.board[5] = "  "
        if move.move_type == MoveType.CASTLE_QUEEN:
            if move.piece == "wK":
                self.board[56] = "wR"
                self.board[59] = "  "
            if move.piece == "bK":
                self.board[0] = "bR"
                self.board[3] = "  "

    def handle_click(self, loc: int) -> list[Move]:
        piece = self.board[loc]
        if (piece[0] == BLACK) and self.white_turn:
            return [] 
        if (piece[0] == WHITE) and not self.white_turn: 
            return []
        moves = self.get_moves(piece, loc)
        verified_moves = self.verify_moves(moves)
        return verified_moves

        
    def get_moves(self, piece: str, loc: int, include_castling: bool = True) -> list[Move]:
        moves = [] 
        match piece[1]:
            case " ":
                return [] 
            case Pieces.PAWN:
                if piece[0] == WHITE:
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
                moves = self.king_moves(piece, loc, include_castling)
            case Pieces.KNIGHT:
                moves = self.knight_moves(piece, loc)
        return moves

    def move(self, piece: str, loc1: int, loc2: int, moves: list[Move]) -> tuple[list[Move], bool]:
        b = False
        if self.board[loc2] == "  ":
            moves.append(self.create_move(piece, loc1, loc2, MoveType.MOVE))
        elif self.board[loc2][0] != piece[0]:
            moves.append(self.create_move(piece, loc1, loc2, MoveType.CAPTURE, self.board[loc2]))
            b = True
        else:
            b = True
        return moves, b

    def switch_turn(self):
        self.white_turn = not self.white_turn
        if self.white_turn:
            moves = self.get_white_moves()
        else:
            moves = self.get_black_moves()
        self.moves = self.verify_moves(moves)
        if len(self.moves) == 0:
            self.game_over = True
            if self.is_in_check(self.white_turn):
                self.checkmate = True
                self.winner = "b" if self.white_turn else "w"
            else:
                self.stalemate = True
        if self.is_fifty_move_draw():
            self.game_over = True

    def is_fifty_move_draw(self) -> bool:
        return self.halfmove_clock >= 100

    def is_square_attacked(self, idx: int, by_white: bool) -> bool:
        if by_white:
            enemy_moves = self.get_white_moves(False)
        else:
            enemy_moves = self.get_black_moves(False)
        for m in enemy_moves:
            if m.to_idx == idx:
                return True
        return False

    def is_in_check(self, white_king: bool) -> bool:
        if white_king:
            king_idx = self.white_king
        else:
            king_idx = self.black_king
        return self.is_square_attacked(king_idx, by_white = not white_king)

    def knight_moves(self, piece: str, loc: int) -> list[Move]:
        moves = []
        row, col = idx_to_row_col(loc)
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
        row, col = idx_to_row_col(loc)
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
        row, col = idx_to_row_col(loc)
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

    def king_moves(self, piece: str, loc: int, include_castling: bool = True) -> list[Move]:
        moves = []
        row, col = idx_to_row_col(loc)
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
        if piece[0] == WHITE and not self.white_king_moved and include_castling:
            if (not self.white_rook_kingside_moved
                and self.board[61] == "  " and self.board[62] == "  "
                and not self.is_square_attacked(60, False)
                and not self.is_square_attacked(61, False)
                and not self.is_square_attacked(62, False)
            ):
                moves.append(self.create_move("wK", 60, 62, MoveType.CASTLE_KING))
            if (not self.white_rook_queenside_moved
                and self.board[58] == "  "
                and self.board[57] == "  "
                and self.board[59] == "  "
                and not self.is_square_attacked(59, False)
                and not self.is_square_attacked(58, False)
                and not self.is_square_attacked(57, False)
            ):
                moves.append(self.create_move("wK", 60, 58, MoveType.CASTLE_QUEEN))
        if piece[0] == BLACK and not self.black_king_moved:
            if (not self.black_rook_kingside_moved
                and self.board[5] == "  " and self.board[6] == "  "
                and not self.is_square_attacked(6, True)
                and not self.is_square_attacked(4, True)
                and not self.is_square_attacked(5, True)
            ):
                moves.append(self.create_move("bK", 4, 6, MoveType.CASTLE_KING))
            if (not self.black_rook_queenside_moved
                and self.board[1] == "  "
                and self.board[2] == "  "
                and self.board[3] == "  "
                and not self.is_square_attacked(1, True)
                and not self.is_square_attacked(2, True)
                and not self.is_square_attacked(3, True)
            ):
                moves.append(self.create_move("bK", 4, 2, MoveType.CASTLE_QUEEN))

        return moves

    def wp_moves(self, piece, loc):
        moves = []
        row, col = idx_to_row_col(loc)
        if self.board[loc-8] == "  ":
            if row == 1:
                moves.extend(self.get_promo_moves(piece, loc, loc-8))
            else:
                moves.append(self.create_move(piece, loc, loc-8, MoveType.MOVE))
                if row == 6:
                    if self.board[loc-16] == "  ":
                        moves.append(self.create_move(piece, loc, loc-16, MoveType.DOUBLE))
        if col < 7:
            if self.board[loc-7][0] == BLACK:
                if row == 1:
                    moves.extend(self.get_promo_moves(piece, loc, loc-7, self.board[loc-7]))
                else:
                    moves.append(self.create_move(piece, loc, loc-7, MoveType.CAPTURE, self.board[loc-7]))
        if col > 0:
            if self.board[loc-9][0] == BLACK:
                if row == 1:
                    moves.extend(self.get_promo_moves(piece, loc, loc-9, self.board[loc-9]))
                else:
                    moves.append(self.create_move(piece, loc, loc-9, MoveType.CAPTURE, self.board[loc-9]))
        if row == 3:
            if self.move_history[-1].move_type == MoveType.DOUBLE:
                l = self.move_history[-1].to_idx
                if loc+1 == l:
                    moves.append(self.create_move(piece, loc, loc-7, MoveType.EN_PASSANT))
                if loc-1 == l:
                    moves.append(self.create_move(piece, loc, loc-9, MoveType.EN_PASSANT))
        return moves
        
                        
    def bp_moves(self, piece: str, loc: int) -> list[Move]:
        moves = []
        row, col = idx_to_row_col(loc)
        if self.board[loc+8] == "  ":
            if row == 6:
                moves.extend(self.get_promo_moves(piece, loc, loc+8))
            else:
                moves.append(self.create_move(piece, loc, loc+8, MoveType.MOVE))
                if row == 1:
                    if self.board[loc+16] == "  ":
                        moves.append(self.create_move(piece, loc, loc+16, MoveType.DOUBLE))
        if col < 7:
            if self.board[loc+9][0] == WHITE:
                if row == 6:
                    moves.extend(self.get_promo_moves(piece, loc, loc+9, self.board[loc+9]))
                else:
                    moves.append(self.create_move(piece, loc, loc+9, MoveType.CAPTURE, self.board[loc+9]))
        if col > 0:
            if self.board[loc+7][0] == WHITE:
                if row == 6:
                    moves.extend(self.get_promo_moves(piece, loc, loc+7, self.board[loc+7]))
                else:
                    moves.append(self.create_move(piece, loc, loc+7, MoveType.CAPTURE, self.board[loc+7]))
        if row == 4:
            if self.move_history[-1].move_type == MoveType.DOUBLE:
                l = self.move_history[-1].to_idx
                if loc+1 == l:
                    moves.append(self.create_move(piece, loc, loc+9, MoveType.EN_PASSANT))
                if loc-1 == l:
                    moves.append(self.create_move(piece, loc, loc+7, MoveType.EN_PASSANT))
        return moves

    def get_promo_moves(self, piece: str, loc: int, to_loc: int, captured: str | None = None) -> list[Move]:
        moves = []
        if piece[0] == WHITE:
            for p in ["wQ", "wR", "wB", "wN"]:
                moves.append(self.create_move(piece, loc, to_loc, MoveType.PROMOTION, captured, p))
        else:
            for p in ["bQ", "bR", "bB", "bN"]:
                moves.append(self.create_move(piece, loc, to_loc, MoveType.PROMOTION, captured, p))
        return moves
    
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

def idx_to_row_col(idx: int) -> tuple[int, int]:
    return idx // 8, idx % 8

