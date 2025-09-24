import pygame

class Board:
    def __init__(self, player_color):
        self.square_size = 85
        self.player_color = player_color
        self.white_sq_color = (40,34,15)
        self.black_sq_color = (120,100,50)
        self.border = 20
        self.pieces = pygame.image.load("./assets/pieces.png")

    def draw(self, window):
        if self.player_color == "white":
            color = self.white_sq_color
        else:
            color = self.black_sq_color
        for i in range(8):
            x_val = self.border + i*self.square_size
            for j in range(8):
                y_val = self.border + j*self.square_size
                pygame.draw.rect(window, color, (x_val, y_val, 85, 85))
                if j == 7:
                    break
                elif color == self.white_sq_color:
                    color = self.black_sq_color
                else:
                    color = self.white_sq_color

    def draw_pawn(self, window, x, y):
        x_loc = x*85 + 33
        y_loc = y*85 + 33
        location = (x_loc, y_loc)
        rectangle = pygame.Rect(0,64,64,64)
        window.blit(self.pieces, location, rectangle)
    
    def draw_bishop(self, window, x, y):
        x_loc = x*85 + 33
        y_loc = y*85 + 33
        location = (x_loc, y_loc)
        rectangle = pygame.Rect(128,0,64,64)
        window.blit(self.pieces, location, rectangle)
    
