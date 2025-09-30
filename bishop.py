from piece import Piece
import pygame

class Bishop(Piece):
    def __init__(self, color, x, y, size):
        super().__init__(color, x, y, size)
        self.image = self.get_img(size, 2)

    
    def possible_moves(self, board):
        return self.diag_moves(board)
