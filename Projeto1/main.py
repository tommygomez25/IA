import pygame
from piece import Piece
from settings import *
from state import State

class Game:
    def __init__(self,state):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Black Hole Escape")
        self.clock = pygame.time.Clock()
        self.winner = None
        self.turn = 1
        self.state = state
    
    def new(self):
        self.run()
    
    def run(self):
        while self.winner is None:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
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
            if self.state.selected_piece:
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
                                        state.selected_piece = piece
                                        return 
                                    
                        if self.state.is_valid_move(self.state.selected_piece,mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE):
                            self.state.move()
                            self.state.selected_piece = None
                            # SWITCH TURNS
                            self.turn = 2 if self.turn == 1 else 1
                    
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        for piece in self.state.pieces:
                            if piece.color == RED_PIECE_COLOR and self.turn == 1 or piece.color == BLUE_PIECE_COLOR and self.turn == 2:
                                if pygame.Rect(piece.x*TILE_SIZE, piece.y*TILE_SIZE, TILE_SIZE, TILE_SIZE).collidepoint(mouse_pos) and not piece.removed:
                                    # listen to mouse click to select piece
                                    if pygame.mouse.get_pressed()[0]:
                                        #select piece and desselect others
                                        for p in self.state.pieces:
                                            p.selected = False
                                        piece.selected = True
                                        state.selected_piece = piece
                                        
            

game_pieces = [
    Piece(0,0,RED_PIECE_COLOR, 1),
    Piece(1,1,RED_PIECE_COLOR,  1), 
    Piece(4,0,RED_PIECE_COLOR, 1),
    Piece(3,1,RED_PIECE_COLOR, 1), 
    Piece(0,4,BLUE_PIECE_COLOR, 2),
    Piece(1,3,BLUE_PIECE_COLOR, 2),
    Piece(4,4,BLUE_PIECE_COLOR, 2),
    Piece(3,3,BLUE_PIECE_COLOR, 2),
    Piece(2,2,BLACK_HOLE_COLOR, 0),
]

state = State(game_pieces)

game = Game(state)

while True:
    game.new()
    game.run()
    
