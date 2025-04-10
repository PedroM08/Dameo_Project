import pygame
from  . import constants

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        self.captures_to_make = 0

    # def calc_pos(self):
    #     pass

    def make_king(self):
        self.king = True

    def draw(self, window): # draws the piece on the (row, cols) of the  board 
        # Draw the piece either blue or red deppending on the self.color
        # if self.color == 'b': 
        #     if self.king == False: self.piece = pygame.image.load('images/Azul.png')
        #     else: self.piece = pygame.image.load('images/Rei_azul.png')
        # else : 
        #     if self.king == False: self.piece = pygame.image.load('images/Vermelho.png')
        #     else: self.piece = pygame.image.load('images/Rei_vermelho.png')

        if self.color == 'b': 
            if not self.king:
                image = pygame.image.load('images/Azul.png')
            else:
                image = pygame.image.load('images/Rei_azul.png')
        else: 
            if not self.king:
                image = pygame.image.load('images/Vermelho.png')
            else:
                image = pygame.image.load('images/Rei_vermelho.png')

        # Scale the piece to match the board size
        scaled_piece = pygame.transform.scale(image, (constants.screen_w // 11, constants.screen_h // (180 / 29)))
        # Make a rectangle the size of the piece that is centered in the piece square
        piece_rect = scaled_piece.get_rect(center=(((constants.screen_w * 28) / 128) + ((constants.screen_w * 8) / 128)* self.col, 5 + (constants.screen_h / 9)*(9 - self.row)))
        window.blit(scaled_piece, piece_rect.topleft) # Display the piece



    def move_piece(self, row=None, col=None):
        # Change the old cords of the piece for the new ones
        self.row, self.col = row, col

    def __repr__(self):
        return str(f'({self.row}, {self.col}); {self.color}, {self.king} im a object')