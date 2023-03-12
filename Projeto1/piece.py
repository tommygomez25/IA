import pygame 
from settings import *
class Piece:
    
    def __init__(self,x,y,color,player):
        self.color = color
        self.x = x
        self.y = y
        self.selected = False
        self.removed = False
        self.player = player
        
    def draw(self,screen, state):
        if not self.removed:
            pygame.draw.circle(screen,self.color,(self.x * TILE_SIZE + TILE_SIZE/2,self.y * TILE_SIZE + TILE_SIZE/2),TILE_SIZE/2-10)
            if self.selected:
                pygame.draw.circle(screen,WHITE,(self.x * TILE_SIZE + TILE_SIZE/2,self.y * TILE_SIZE + TILE_SIZE/2),TILE_SIZE/2-10,3)
                for move in self.available_moves(state):
                    pygame.draw.circle(screen,GREY,(move[0] * TILE_SIZE + TILE_SIZE/2,move[1] * TILE_SIZE + TILE_SIZE/2),TILE_SIZE/2-10)
                

    def landed_on_black_hole(self):
        return self.x == 2 and self.y == 2
    
    def available_moves(self, state):
        moves1 = []
        moves2 = []
        moves3 = []
        moves4 = []
        for i in range(1,5):
            if self.x + i < 5 and not state.is_piece_at(self.x + i,self.y):
                moves1.append((self.x + i,self.y))
            else:
                break
        for i in range(1,5):
            if self.x - i >= 0 and not state.is_piece_at(self.x - i,self.y):
                moves2.append((self.x - i,self.y))
            else:
                break
        for i in range(1,5):
            if self.y + i < 5 and not state.is_piece_at(self.x,self.y + i):
                moves3.append((self.x,self.y + i))
            else:
                break
        for i in range(1,5):
            if self.y - i >= 0 and not state.is_piece_at(self.x,self.y - i):
                moves4.append((self.x,self.y - i))
            else:
                break
        moves = []
        if len(moves1) > 0:
            moves.append(moves1[-1])
        if len(moves2) > 0:
            moves.append(moves2[-1])
        if len(moves3) > 0:
            moves.append(moves3[-1])
        if len(moves4) > 0:
            moves.append(moves4[-1])
        return moves


    