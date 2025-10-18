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
        
    def make_move(self, loc, moves):
        for move in moves:
            if move[2] == loc:
                if move[3] == "c":
                    self.captured_pieces.append(self.board[move[2]])
                if move[3] == "e":
                    if self.white_turn:
                        self.captured_pieces.append(self.board[loc+8])
                        self.board[loc+8] = "  "
                    else:
                        self.captured_pieces.append(self.board[loc-8])
                        self.board[loc-8] = "  "
                self.board[move[2]] = move[0]
                self.board[move[1]] = "  "
                self.white_turn = not self.white_turn
                self.move_history.append(move)
                return

    def get_move(self, loc):
        piece = self.board[loc]
        if (piece[0] == "b") and self.white_turn:
            return []
        if (piece[0] == "w") and not self.white_turn: 
            return []
        match piece[1]:
            case " ":
                return []
            case "p":
                if piece[0] == "w":
                    return self.wp_moves(piece, loc)
                else:
                    return self.bp_moves(piece, loc)
            case "R":
                return self.rook_moves(piece, loc)
            case "B":
                return self.bishop_moves(piece, loc)
            case "Q":
                return self.queen_moves(piece, loc)
            case "K":
                return self.king_moves(piece, loc)
            case "N":
                return self.knight_moves(piece, loc)

    def move(self, piece, loc1, loc2, moves):
        b = False
        if self.board[loc2] == "  ":
            moves.append((piece, loc1, loc2, "m"))
        elif self.board[loc2][0] != piece[0]:
            moves.append((piece, loc1, loc2, "c"))
        else:
            b = True
        return moves, b

    def knight_moves(self, piece, loc):
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

    def rook_moves(self, piece, loc):
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

    def bishop_moves(self, piece, loc):
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

    def queen_moves(self, piece, loc):
        moves = self.bishop_moves(piece, loc)
        moves.extend(self.rook_moves(piece, loc))
        return moves

    def king_moves(self, piece, loc):
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
            pass
        if self.board[loc-8] == "  ":
            moves.append((piece, loc, loc-8, "m"))
            if row == 6:
                if self.board[loc-16] == "  ":
                    moves.append((piece, loc, loc-16, "d"))
        if col < 7:
            if self.board[loc-7][0] == "b":
                moves.append((piece, loc, loc-7, "c"))
        if col > 0:
            if self.board[loc-9][0] == "b":
                moves.append((piece, loc, loc-9, "c"))
        if row == 3:
            if self.move_history[-1][3] == "d":
                l = self.move_history[-1][2]
                if loc+1 == l:
                    moves.append((piece, loc, loc-7, "e"))
                if loc-1 == l:
                    moves.append((piece, loc, loc-9, "e"))
        return moves
        
                        
    def bp_moves(self, piece, loc):
        moves = []
        row = loc//8
        col = loc%8
        if row == 6:
            pass
        if self.board[loc+8] == "  ":
            moves.append((piece, loc, loc+8, "m"))
            if row == 1:
                if self.board[loc+16] == "  ":
                    moves.append((piece, loc, loc+16, "d"))
        if col < 7:
            if self.board[loc+9][0] == "w":
                moves.append((piece, loc, loc+9, "c"))
        if col > 0:
            if self.board[loc+7][0] == "w":
                moves.append((piece, loc, loc+7, "c"))
        if row == 4:
            if self.move_history[-1][3] == "d":
                l = self.move_history[-1][2]
                if loc+1 == l:
                    moves.append((piece, loc, loc+9, "e"))
                if loc-1 == l:
                    moves.append((piece, loc, loc+7, "e"))
        return moves

