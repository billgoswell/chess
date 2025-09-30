from piece import Piece
import pygame

class Queen(Piece):
    def __init__(self, color, x, y, size):
        super().__init__(color, x, y, size)
        self.image = self.get_img(size, 1)

    def possible_moves(self, board):
        moves = self.diag_moves(board)
        moves.extend(self.horz_moves(board))
        return moves
