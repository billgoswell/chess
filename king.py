from piece import Piece
import pygame

class King(Piece):

    def __init__(self, color, x, y, size):
        super().__init__(color, x, y, size)
        self.image = self.get_img(size, 0)
        
    def possible_moves(self, board):
        self.moves = []
        if self.x+1 <= 7:
            if board[self.y][self.x+1] == None:
                self.moves.append((self.x+1, self.y))
            elif board[self.y][self.x+1].color != self.color:
                self.moves.append((self.x+1, self.y))
            if self.y+1 <= 7:
                if board[self.y+1][self.x+1] == None:
                    self.moves.append((self.x+1, self.y+1))
                elif board[self.y+1][self.x+1].color != self.color:
                    self.moves.append((self.x+1, self.y+1))
            if self.y-1 >= 0:
                if board[self.y-1][self.x+1] == None:
                    self.moves.append((self.x+1, self.y-1))
                elif board[self.y-1][self.x+1].color != self.color:
                    self.moves.append((self.x+1, self.y-1))
        if self.x-1 >= 0:
            if board[self.y][self.x-1] == None:
                self.moves.append((self.x-1, self.y))
            elif board[self.y][self.x-1].color != self.color:
                self.moves.append((self.x-1, self.y))
            if self.y+1 <= 7:
                if board[self.y+1][self.x-1] == None:
                    self.moves.append((self.x-1, self.y+1))
                elif board[self.y+1][self.x-1].color != self.color:
                    self.moves.append((self.x-1, self.y+1))
            if self.y-1 >= 0:
                if board[self.y-1][self.x-1] == None:
                    self.moves.append((self.x-1, self.y-1))
                elif board[self.y-1][self.x-1].color != self.color:
                    self.moves.append((self.x-1, self.y-1))

        if self.y+1 <= 7:
            if board[self.y+1][self.x] == None:
                self.moves.append((self.x, self.y+1))
            elif board[self.y+1][self.x].color != self.color:
                self.moves.append((self.x, self.y+1))
        if self.y-1 >= 0:
            if board[self.y-1][self.x] == None:
                self.moves.append((self.x, self.y-1))
            elif board[self.y-1][self.x].color != self.color:
                self.moves.append((self.x, self.y-1))
        return self.moves
