from settings import *
import pygame

class State:
    
    def __init__(self,pieces):
        self.pieces = pieces
        self.selected_piece = None
    
    def draw(self,screen):
        for piece in self.pieces:
            piece.draw(screen)
    
    def is_valid_move(self,piece,x,y):
        if x < 0 or x > 4 or y < 0 or y > 4:
            return False
        # the piece moves only vertically or horizontally and is moved until blocked by another piece
        if piece.x != x and piece.y != y:
            return False
    
        # if the piece is moving horizontally
        if piece.x != x:
            if x < piece.x:
                piece.dx = -1
            elif x > piece.x:
                piece.dx = 1
            piece.dy = 0
            # check if piece is out of bounds
            if not piece.removed:
                if piece.x < 0:
                    piece.x = 0
                    piece.dx = 0
                elif piece.x > 4:
                    piece.x = 4
                    piece.dx = 0
                if piece.y < 0:
                    piece.y = 0
                    piece.dy = 0
                elif piece.y > 4:
                    piece.y = 4
                    piece.dy = 0
            # check if pieces are on top of each other
            for p in self.pieces:
                if p != self and p.x == piece.x and p.y == piece.y:
                    piece.x -= piece.dx
                    piece.y -= piece.dy
                    piece.dx = 0
                    piece.dy = 0
        
        # if the piece is moving vertically
        if piece.y != y:
            if y < piece.y:
                piece.dy = -1
            elif y > piece.y:
                piece.dy = 1
            piece.dx = 0
            
            # check if piece is out of bounds
            if not piece.removed:
                if piece.x < 0:
                    piece.x = 0
                    piece.dx = 0
                elif piece.x > 4:
                    piece.x = 4
                    piece.dx = 0
                if piece.y < 0:
                    piece.y = 0
                    piece.dy = 0
                elif piece.y > 4:
                    piece.y = 4
                    piece.dy = 0
            # check if pieces are on top of each other
            for p in self.pieces:
                if p != self and p.x == piece.x and p.y == piece.y:
                    piece.x -= piece.dx
                    piece.y -= piece.dy
                    piece.dx = 0
                    piece.dy = 0
        return True
    
    def move(self):
        for piece in self.pieces:
            piece.move()
    

        
            
    