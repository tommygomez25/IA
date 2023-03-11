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
            # if the piece is moving left
            if x<piece.x:
                if x == 0 and not self.is_piece_at(x,piece.y) and self.get_first_blocking_piece(piece,-1,0) == None:
                    return True
                if not self.is_piece_at(x-1,piece.y):
                    return False
            # if the piece is moving right
            else:
                if x == 4 and not self.is_piece_at(x,piece.y):
                    return True
                if not self.is_piece_at(x+1,piece.y):
                    return False
                    
        # if the piece is moving vertically
        if piece.y != y:
            # if the piece is moving up
            if y<piece.y:
                if y == 0 and not self.is_piece_at(piece.x,y):
                    return True
                if not self.is_piece_at(piece.x,y-1):
                    return False
            # if the piece is moving down
            else:
                if y == 4 and self.is_piece_at(piece.x,y):
                    return True
                if not self.is_piece_at(piece.x,y+1):
                    return False
        return True
    
    def is_piece_at(self,x,y):
        for piece in self.pieces:
            if piece.x == x and piece.y == y and piece != self.selected_piece:
                return True
        return False
    
    def move_piece(self,piece,x,y):
        piece.x = x
        piece.y = y
        piece.dx = 0
        piece.dy = 0
        piece.selected = False
        self.selected_piece = None
    
    def get_first_blocking_piece(self,piece,dx,dy):
        x = piece.x
        y = piece.y
        while self.is_valid_move(piece,x+dx,y+dy):
            x += dx
            y += dy
        return self.get_piece_at(x,y)
    
    def get_piece_at(self,x,y):
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
        return None
        
            
    