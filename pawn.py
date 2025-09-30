from piece import Piece
import pygame

class Pawn(Piece):
    def __init__(self, color, x, y, size):
        super().__init__(color, x, y, size)
        self.image = self.get_img(size, 5)
    
    def possible_moves(self, board):
        moves = []
        if self.color == "white":
            if self.y == 6:
                if board[5][self.x] == None:
                    moves.append((self.x, 5))
                    if board[4][self.x] == None:
                        moves.append((self.x, 4))
            else:
                if board[self.y-1][self.x] == None:
                    moves.append((self.x, self.y-1))

            if self.x < 7:
                if board[self.y-1][self.x+1] != None and board[self.y-1][self.x+1].color == 'black':
                    moves.append((self.x+1, self.y-1))
                
            if self.x > 0:
                if board[self.y-1][self.x-1] != None and board[self.y-1][self.x-1].color == 'black':
                    moves.append((self.x-1, self.y-1))
        
        if self.color == "black":
            if self.y == 1:
                if board[2][self.x] == None:
                    moves.append((self.x, 2))
                    if board[3][self.x] == None:
                        moves.append((self.x, 3))
            else:
                if board[self.y+1][self.x] == None:
                    moves.append((self.x, self.y+1))
            if self.x < 7:
                if board[self.y+1][self.x+1] != None and board[self.y+1][self.x+1].color == 'white':
                    moves.append((self.x+1, self.y+1))
                
            if self.x > 0:
                if board[self.y+1][self.x-1] != None and board[self.y+1][self.x-1].color == 'white':
                    moves.append((self.x-1, self.y+1))


        return moves

