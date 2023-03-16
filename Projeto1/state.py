from settings import *
import pygame
from copy import deepcopy
from piece import Piece

class State:
    
    def __init__(self):
        self.pieces = []
        self.pieces.append(Piece((GAME_SIZE-1)/2,(GAME_SIZE-1)/2,BLACK_HOLE_COLOR,3))
        # create pieces for player 1 and 2 according to GAME_SIZE and position them only in matrix diagonal AND ANTI-DIAGONAL
        for i in range(GAME_SIZE):
            for j in range(GAME_SIZE):
                if i == j and i != (GAME_SIZE-1)/2 and j < (GAME_SIZE-1)/2:
                    self.pieces.append(Piece(i,j,RED_PIECE_COLOR,1))
                if i == j and i != (GAME_SIZE-1)/2 and j > (GAME_SIZE-1)/2:
                    self.pieces.append(Piece(i,j,BLUE_PIECE_COLOR,2))
                if i + j == GAME_SIZE - 1 and i != (GAME_SIZE-1)/2 and j < (GAME_SIZE-1)/2:
                    self.pieces.append(Piece(i,j,RED_PIECE_COLOR,1))
                if i + j == GAME_SIZE - 1 and i != (GAME_SIZE-1)/2 and j > (GAME_SIZE-1)/2:
                    self.pieces.append(Piece(i,j,BLUE_PIECE_COLOR,2))
                    
        self.selected_piece = None
    
    def draw(self,screen):
        for piece in self.pieces:
            piece.draw(screen, self)
    
    def is_valid_move(self,piece,x,y):
        return piece.available_moves(self).count((piece.x,piece.y,x,y)) > 0
    
    def is_piece_at(self,x,y):
        if x == (GAME_SIZE-1)/2 and y == (GAME_SIZE-1)/2:
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
        for p in state_copy.pieces:
            if p.x == piece.x and p.y == piece.y:
                p.x = x
                p.y = y
                p.selected = False
                if(p.landed_on_black_hole()):
                    p.removed = True
                    state_copy.pieces.remove(p)
                return state_copy
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
        return player1_pieces == (GAME_SIZE -1)/2 or player2_pieces == (GAME_SIZE-1)/2
            
        
            
    