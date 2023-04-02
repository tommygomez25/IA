import settings
import pygame
from piece import Piece
from copy import deepcopy
from piece import Piece

class State:
    
    def __init__(self, game_pieces = None):
        self.pieces = []
        self.pieces.append(Piece((settings.Game_size-1)/2,(settings.Game_size-1)/2,settings.BLACK_HOLE_COLOR,3))
        if game_pieces is None:
            # create pieces for player 1 and 2 according to settings.Game_size and position them only in matrix diagonal AND ANTI-DIAGONAL
            for i in range(settings.Game_size):
                for j in range(settings.Game_size):
                    if i == j and i != (settings.Game_size-1)/2 and j < (settings.Game_size-1)/2:
                        self.pieces.append(Piece(i,j,settings.RED_PIECE_COLOR,1))
                    if i == j and i != (settings.Game_size-1)/2 and j > (settings.Game_size-1)/2:
                        self.pieces.append(Piece(i,j,settings.BLUE_PIECE_COLOR,2))
                    if i + j == settings.Game_size - 1 and i != (settings.Game_size-1)/2 and j < (settings.Game_size-1)/2:
                        self.pieces.append(Piece(i,j,settings.RED_PIECE_COLOR,1))
                    if i + j == settings.Game_size - 1 and i != (settings.Game_size-1)/2 and j > (settings.Game_size-1)/2:
                        self.pieces.append(Piece(i,j,settings.BLUE_PIECE_COLOR,2))
        else:
            self.pieces = game_pieces
                    
        self.selected_piece = None
        self.turn = 1
        self.p1plays = 0
        self.p2plays = 0
    
    def draw(self,screen):
        for piece in self.pieces:
            piece.draw(screen, self)
    
    def is_valid_move(self,piece,x,y):
        return piece.available_moves(self).count((piece.x,piece.y,x,y)) > 0
    
    def is_piece_at(self,x,y):
        if x == (settings.Game_size-1)/2 and y == (settings.Game_size-1)/2:
            return False
        for piece in self.pieces:
            if piece.x == x and piece.y == y and piece != self.selected_piece:
                return True
        return False
    
    def available_moves(self):
        moves = []
        for piece in self.pieces:
            if piece.player == self.turn and not piece.removed:
                moves.extend(piece.available_moves(self))
        
        #print("Available moves: " + str(moves))
        return moves
    
    def move_piece(self,piece,x,y):
        state_copy = deepcopy(self)
        for p in state_copy.pieces:
            if p.x == piece.x and p.y == piece.y:
                p.x = x
                p.y = y
                p.selected = False
                if(p.landed_on_black_hole()):
                    p.x = -1
                    p.y = -1
                    p.removed = True
                state_copy.turn = 3 - state_copy.turn
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
        return player1_pieces == (settings.Game_size -1)/2 or player2_pieces == (settings.Game_size-1)/2

    def get_outcome(self):
        # Returns 1 or 0 or -1 depending on your state corresponding to win, tie or a loss.
        player1_pieces = 0
        player2_pieces = 0
        for piece in self.pieces:
            if piece.player == 1 and piece.removed:
                player1_pieces += 1
            elif piece.player == 2 and piece.removed:
                player2_pieces += 1
        if player1_pieces == (settings.Game_size -1)/2 or player1_pieces == 1 and self.turn == 1:
            return 1
        elif player2_pieces == (settings.Game_size-1)/2 or player2_pieces == 1 and self.turn == 2:
            return 2
        elif player1_pieces == (settings.Game_size -1)/2 or player1_pieces == 1 and self.turn == 2:
            return 1
        elif player2_pieces == (settings.Game_size-1)/2 or player2_pieces == 1 and self.turn == 1:
            return 2
        else :
            return 0
    
    def get_turn(self):
        return self.turn
            
        
            
    
