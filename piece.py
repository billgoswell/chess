import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, color,  x, y, size):
        super().__init__()
        self.sprite_sheet_image = pygame.transform.scale(pygame.image.load("./assets/pieces.png"), (size*6, size*2))
        self.x = x
        self.y = y
        self.xpos = size*x+20
        self.ypos = size*y+20
        self.color = color
        self.rect = pygame.Rect(self.xpos, self.ypos, size, size)

    def get_img(self, size, img_loc):
        if self.color == "white":
            img_rect = pygame.Rect(size*img_loc, 0, size, size)
        else:
            img_rect = pygame.Rect(size*img_loc, size, size, size)
        image = self.sprite_sheet_image.subsurface(img_rect)
        return image

    
    def update(self, move, size):
        self.x = move[0]
        self.y = move[1]
        self.xpos = size*self.x+20
        self.ypos = size*self.y+20
        self.rect = pygame.Rect(self.xpos, self.ypos, size, size)
    
    def possible_moves(self, board):
        return []

    def diag_moves(self, board):
        moves = []
        if self.x >= self.y:
            l = self.x
            s = self.y
        else:
            l = self.y
            s = self.x
        for i in range(1,8-l):
            if board[self.y+i][self.x+i] == None:
                moves.append((self.x+i, self.y+i))
            elif board[self.y+i][self.x+i].color != self.color:
                moves.append((self.x+i, self.y+i))
                break
            else:
                break
        for i in range(1, s+1):
            if board[self.y-i][self.x-i] == None:
                moves.append((self.x-i, self.y-i))
            elif board[self.y-i][self.x-i].color != self.color:
                moves.append((self.x-i, self.y-i))
                break
            else:
                break
        for i in range(1, 8):
            if self.y-i < 0:
                break
            if self.x+i > 7:
                break
            if board[self.y-i][self.x+i] == None:
                moves.append((self.x+i, self.y-i))
            elif board[self.y-i][self.x+i].color != self.color:
                moves.append((self.x+i, self.y-i))
                break
            else:
                break
        for i in range(1, 8):
            if self.x-i < 0:
                break
            if self.y+i > 7:
                break
            if board[self.y+i][self.x-i] == None:
                moves.append((self.x-i, self.y+i))
            elif board[self.y+i][self.x-i].color != self.color:
                moves.append((self.x-i, self.y+i))
                break
            else:
                break
        return moves

    def horz_moves(self, board): 
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
