from piece import Piece
import pygame

class King(Piece):

    def __init__(self, color, x, y, size):
        super().__init__(color, x, y, size)
        self.image = self.get_img(size, 0)
        
    def possible_moves(self, board):
        moves = []
        return moves
