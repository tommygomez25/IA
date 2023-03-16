from settings import *
import pygame
from piece import Piece
from copy import deepcopy

class State:
    
    def __init__(self,pieces):
        self.pieces = pieces
        self.selected_piece = None
    
    def draw(self,screen):
        for piece in self.pieces:
            piece.draw(screen, self)
    
    def is_valid_move(self,piece,x,y):
        return piece.available_moves(self).count((piece.x,piece.y,x,y)) > 0
    
    def is_piece_at(self,x,y):
        if x == 2 and y == 2:
            return False
        for piece in self.pieces:
            if piece.x == x and piece.y == y and piece != self.selected_piece:
                return True
        return False
    
    def available_moves(self, turn):
        moves = []
        for piece in self.pieces:
            if piece.player == turn and not piece.removed:
                moves.extend(piece.available_moves(self))
        return moves
    
    def move_piece(self,piece,x,y):
        state_copy = deepcopy(self)
        p = state_copy.get_piece_at(piece.x, piece.y)
        p.x = x
        p.y = y
        p.selected = False
        self.selected_piece = None
        
        if(p.landed_on_black_hole()):
            p.removed = True
        return state_copy
    
    def get_piece_at(self,x,y):
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
        return None
    
    def check_win(self):
        player1_pieces = 0
        player2_pieces = 0
        for piece in self.pieces:
            if piece.player == 1 and piece.removed:
                player1_pieces += 1
            elif piece.player == 2 and piece.removed:
                player2_pieces += 1
        return player1_pieces == 2 or player2_pieces == 2
            