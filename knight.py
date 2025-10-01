from piece import Piece
import pygame

class Knight(Piece):
    def __init__(self, color, x, y, size):
        super().__init__(color, x, y, size)
        self.image = self.get_img(size,3)
               
    def possible_moves(self, board):
        moves = []
        if (self.x+2) <= 7:
            if (self.y-1) >= 0:
                if board[self.y-1][self.x+2] == None:
                    moves.append((self.x+2, self.y-1))
                elif board[self.y-1][self.x+2].color != self.color:
                    moves.append((self.x+2, self.y-1))
            if (self.y+1) <= 7:
                if board[self.y+1][self.x+2] == None:
                    moves.append((self.x+2, self.y+1))
                elif board[self.y+1][self.x+2].color != self.color:
                        moves.append((self.x+2, self.y+1))
        if (self.x-2) >= 0:
            if (self.y-1) >= 0:
                if board[self.y-1][self.x-2] == None:
                    moves.append((self.x-2, self.y-1))
                elif board[self.y-1][self.x-2].color != self.color:
                    moves.append((self.x-2, self.y-1))
            if (self.y+1) <= 7:
                if board[self.y+1][self.x-2] == None:
                    moves.append((self.x-2, self.y+1))
                elif board[self.y+1][self.x-2].color != self.color:
                    moves.append((self.x-2, self.y+1))
        if (self.y+2) <= 7:
            if (self.x-1) >= 0:
                if board[self.y+2][self.x-1] == None:
                    moves.append((self.x-1, self.y+2))
                elif board[self.y+2][self.x-1].color != self.color:
                    moves.append((self.x-1, self.y+2))
            if (self.x+1) <= 7:
                if board[self.y+2][self.x+1] == None:
                    moves.append((self.x+1, self.y+2))
                elif board[self.y+2][self.x+1].color != self.color:
                        moves.append((self.x+1, self.y+2))
        if (self.y-2) >= 0:
            if (self.x-1) >= 0:
                if board[self.y-2][self.x-1] == None:
                    moves.append((self.x-1, self.y-2))
                elif board[self.y-2][self.x-1].color != self.color:
                    moves.append((self.x-1, self.y-2))
            if (self.x+1) <= 7:
                if board[self.y-2][self.x+1] == None:
                    moves.append((self.x+1, self.y-2))
                elif board[self.y-2][self.x+1].color != self.color:
                    moves.append((self.x+1, self.y-2))
        return moves
