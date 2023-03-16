import pygame
from piece import Piece
from settings import *
from state import State
import time
import ai
from copy import deepcopy


class Game:
    def __init__(self,state, player1, player2):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Black Hole Escape")
        self.clock = pygame.time.Clock()
        self.winner = None
        self.turn = 1
        self.state = state
        self.player1 = player1
        self.player2 = player2
    
    def new(self):
        self.run()
    
    def run(self):
        while self.winner is None:
            self.draw()
            if self.turn == 1:
                self.player1(self)
            else:
                self.player2(self)
            if self.state.check_win():
                self.winner = 3 - self.turn
        self.display_winner()
            
    def update(self):
        pass
    
    def draw_grid(self):
        for row in range(0,GAME_SIZE*TILE_SIZE + TILE_SIZE, TILE_SIZE):
            pygame.draw.line(self.screen, BLUE_PIECE_COLOR, (row,0), (row,GAME_SIZE*TILE_SIZE),7)

        for col in range(0,GAME_SIZE*TILE_SIZE + TILE_SIZE, TILE_SIZE+1):
            pygame.draw.line(self.screen, BLUE_PIECE_COLOR, (0,col), (GAME_SIZE*TILE_SIZE,col),7)
    
    def draw_board(self):
        self.state.draw(self.screen)
        
    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_grid()
        self.draw_board()
        pygame.display.flip()

    def display_winner(self):
        while True:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)
            font = pygame.font.SysFont('Arial', 30)
            text = font.render("Player " + str(self.winner) + " won!", True, BLACK)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.screen.blit(text, textRect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
                quit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    pygame.quit()
                    quit(0)
            
            # if a piece is selected, listen to mouse movements and clicks to move the piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    # if the mouse is clicked on a friendly piece, select it
                    for piece in self.state.pieces:
                        if piece.color == RED_PIECE_COLOR and self.turn == 1 or piece.color == BLUE_PIECE_COLOR and self.turn == 2:
                            if pygame.Rect(piece.x*TILE_SIZE, piece.y*TILE_SIZE, TILE_SIZE, TILE_SIZE).collidepoint(mouse_pos) and not piece.removed:
                                # listen to mouse click to select piece
                                if pygame.mouse.get_pressed()[0]:
                                    #select piece and desselect others
                                    for p in self.state.pieces:
                                        p.selected = False
                                    piece.selected = True
                                    self.state.selected_piece = piece
                                    return 
                    if self.state.selected_piece and self.state.is_valid_move(self.state.selected_piece,mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE):
                        self.state = self.state.move_piece(self.state.selected_piece,mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE)
                        self.selected_piece = None
                        self.turn = 3 - self.turn
                        return
                    
            

def execute_human_move(game):
    game.clock.tick(FPS)
    game.events()
    game.update()

game_pieces = [
    Piece(2,2,BLACK_HOLE_COLOR, 0),
    Piece(0,0,RED_PIECE_COLOR, 1),
    Piece(1,1,RED_PIECE_COLOR,  1), 
    Piece(4,0,RED_PIECE_COLOR, 1),
    Piece(3,1,RED_PIECE_COLOR, 1), 
    Piece(0,4,BLUE_PIECE_COLOR, 2),
    Piece(1,3,BLUE_PIECE_COLOR, 2),
    Piece(4,4,BLUE_PIECE_COLOR, 2),
    Piece(3,3,BLUE_PIECE_COLOR, 2),
]

state = State(game_pieces)

#game = Game(state, execute_human_move, execute_human_move) #human vs human
game = Game(state, execute_human_move, ai.execute_ai_move(5, ai.evaluate_f2)) #human vs ai
#game = Game(state, execute_ai_move(5, evaluate_f1), execute_human_move) #ai vs human
#game = Game(state, execute_ai_move(7, evaluate_f3), execute_ai_move(7, evaluate_f2)) #ai vs ai

while True:
    game.new()
    
