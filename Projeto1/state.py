from settings import *
import pygame

class State:
    
    def __init__(self,pieces):
        self.pieces = pieces
        self.selected_piece = None
    
    def draw(self,screen):
        for piece in self.pieces:
            piece.draw(screen, self)

    def available_moves(self):
        if self.selected_piece:
            return self.selected_piece.available_moves(self)
        return []
    
    def is_valid_move(self,piece,x,y):
        print(piece.available_moves(self))
        print(self.is_piece_at(2,2))
        #print pieces
        return piece.available_moves(self).count((x,y)) > 0
    
    def is_piece_at(self,x,y):
        if x == 2 and y == 2:
            return False
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
        if(piece.landed_on_black_hole()):
            piece.removed = True
            self.pieces.remove(piece)
    
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
    
    def check_win(self):
        # if any of the players has 2 pieces he is the winner
        player1_pieces = 0
        player2_pieces = 0
        for piece in self.pieces:
            if piece.player == 1:
                player1_pieces += 1
            else:
                player2_pieces += 1
        return player1_pieces == 2 or player2_pieces == 2
            
        
            
    