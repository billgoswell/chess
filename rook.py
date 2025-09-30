from piece import Piece
import pygame

class Rook(Piece):
    def __init__(self, color, x, y, size):
        super().__init__(color, x, y, size)
        self.image = self.get_img(size, 4)


    def possible_moves(self, board):
        moves = []
        for i in range(self.x+1, 8):
            if board[self.y][i] == None:
                moves.append((i, self.y))
            elif board[self.y][i].color != self.color:
                moves.append((i, self.y))
                break
            else:
                break
        
        for i in range(self.x-1, -1, -1):
            if board[self.y][i] == None:
                moves.append((i, self.y))
            elif board[self.y][i].color != self.color:
                moves.append((i, self.y))
                break
            else:
                break

        for i in range(self.y+1, 8):
            if board[i][self.x] == None:
                moves.append((self.x, i))
            elif board[i][self.x].color != self.color:
                moves.append((self.x, i))
                break
            else:
                break
       
        for i in range(self.y-1, -1, -1):
            if board[i][self.x] == None:
                moves.append((self.x, i))
            elif board[i][self.x].color  != self.color:
                moves.append((self.x, i))
                break
            else:
                break
                    
        return moves
