import pygame 
from settings import *
class Piece:
    
    def __init__(self,x,y,color,player):
        self.color = color
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.selected = False
        self.removed = False
        self.player = player
        
    def draw(self,screen):
        if not self.removed:
            pygame.draw.circle(screen,self.color,(self.x * TILE_SIZE + TILE_SIZE/2,self.y * TILE_SIZE + TILE_SIZE/2),TILE_SIZE/2-10)
            if self.selected:
                pygame.draw.circle(screen,WHITE,(self.x * TILE_SIZE + TILE_SIZE/2,self.y * TILE_SIZE + TILE_SIZE/2),TILE_SIZE/2-10,3)
    
    # check if piece is out of bounds
    def check_out_of_bounds(self):
        if not self.removed:
            if self.x < 0:
                self.x = 0
                self.dx = 0
            elif self.x > 4:
                self.x = 4
                self.dx = 0
            if self.y < 0:
                self.y = 0
                self.dy = 0
            elif self.y > 4:
                self.y = 4
                self.dy = 0    
        return True
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        self.check_out_of_bounds()
        
        if self.landed_on_black_hole():
            self.x = -1
            self.y = -1
            self.removed = True

    def landed_on_black_hole(self):
        return self.x == 2 and self.y == 2 and self.dx == 0 and self.dy == 0
    