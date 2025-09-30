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
        pass
