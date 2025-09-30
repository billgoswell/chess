from piece import Piece
import pygame

class Rook(Piece):
    def __init__(self, color, x, y, size):
        super().__init__(color, x, y, size)
        self.image = self.get_img(size, 4)
