import pygame
import settings
from piece import Piece
import time
from copy import deepcopy



class Game:
    def __init__(self,state, player1, player2):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Black Hole Escape")
        self.clock = pygame.time.Clock()
        self.winner = None
        self.state = state
        self.playing = True
        self.player1 = player1
        self.player2 = player2

    def loop(self):
        while self.winner == None:
            self.run()
        return self.winner

    def run(self):
        p1time = 0
        p2time = 0
        n1plays = 0
        n2plays = 0
        while self.winner is None:
            self.draw()
            if self.state.turn == 1:
                self.state.p1plays += 1
                start = time.time()
                self.player1(self)
                p1time += time.time() - start
                n1plays += 1
            else:
                self.state.p2plays += 1
                start = time.time()
                self.player2(self)
                p2time += time.time() - start
                n2plays += 1
            if self.playing == False:
                self.pause()
            if self.state.check_win():
                self.winner = 3 - self.state.turn
        #print("Player 1 plays: ", self.state.p1plays)
        #print("Player 1 average time: ", p1time/n1plays)
        #print("Player 2 average time: ", p2time/n2plays)
    
    def draw_grid(self):
        for row in range(0,settings.GAME_SIZE*settings.TILE_SIZE + settings.TILE_SIZE, settings.TILE_SIZE):
            pygame.draw.line(self.screen, settings.BLUE_PIECE_COLOR, (row,0), (row,settings.GAME_SIZE*settings.TILE_SIZE),7)

        for col in range(0,settings.GAME_SIZE*settings.TILE_SIZE + settings.TILE_SIZE, settings.TILE_SIZE+1):
            pygame.draw.line(self.screen, settings.BLUE_PIECE_COLOR, (0,col), (settings.GAME_SIZE*settings.TILE_SIZE,col),7)
    
    def draw_board(self):
        self.state.draw(self.screen)
        
    def draw(self):
        self.screen.fill(settings.BACKGROUND_COLOR)
        self.draw_grid()
        self.draw_board()
        pygame.display.flip()

    def run_n_matches(self, n, max_time = 3600):
        state_copy = deepcopy(self.state)
        start_time = time.time()
        
        results = [0, 0, 0] # [draws, player 1 victories, player 2 victories]
        for i in range(n):
            self.state = deepcopy(state_copy)
            self.run()
            print("END GAME")
            results[self.winner] += 1
            self.winner = None
            self.turn = 1
            
     
        print("\n=== Elapsed time: %s seconds ===" % (time.time() - start_time))
        print(f"  Player 1: {results[1]} victories")
        print(f"  Player 2: {results[2]} victories")
        print(f"  Draws: {results[0]} ")
        print("===============================")
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
                quit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    return 0
            
             # if a piece is selected, listen to mouse movements and clicks to move the piece
            if self.state.selected_piece != None:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        # if the mouse is clicked on a friendly piece, select it
                        for piece in self.state.pieces:
                            if (piece.color == settings.RED_PIECE_COLOR and self.state.turn == 1 and piece != self.state.selected_piece )or (piece.color == settings.BLUE_PIECE_COLOR and self.state.turn == 2 and piece != self.state.selected_piece):
                                if pygame.Rect(piece.x*settings.TILE_SIZE, piece.y*settings.TILE_SIZE, settings.TILE_SIZE, settings.TILE_SIZE).collidepoint(mouse_pos):
                                    #select piece and desselect others
                                    for p in self.state.pieces:
                                        p.selected = False
                                    piece.selected = True
                                    self.state.selected_piece = piece
                                    
                                        
 
                        if self.state.is_valid_move(self.state.selected_piece,mouse_pos[0] // settings.TILE_SIZE, mouse_pos[1] // settings.TILE_SIZE):
                            
                            self.state = self.state.move_piece(self.state.selected_piece,mouse_pos[0] // settings.TILE_SIZE, mouse_pos[1] // settings.TILE_SIZE)
                            self.state.selected_piece = None
                    
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        for piece in self.state.pieces:
                            if (piece.color == settings.RED_PIECE_COLOR and self.state.turn == 1) or (piece.color == settings.BLUE_PIECE_COLOR and self.state.turn == 2):
                                if pygame.Rect(piece.x*settings.TILE_SIZE, piece.y*settings.TILE_SIZE, settings.TILE_SIZE, settings.TILE_SIZE).collidepoint(mouse_pos) and not piece.removed:
                                    #select piece and desselect others
                                    for p in self.state.pieces:
                                        p.selected = False
                                    piece.selected = True
                                    self.state.selected_piece = piece

game_pieces = [
    Piece(2,2,settings.BLACK_HOLE_COLOR, 0),
    Piece(0,0,settings.RED_PIECE_COLOR, 1),
    Piece(1,1,settings.RED_PIECE_COLOR,  1), 
    Piece(4,0,settings.RED_PIECE_COLOR, 1),
    Piece(3,1,settings.RED_PIECE_COLOR, 1), 
    Piece(0,4,settings.BLUE_PIECE_COLOR, 2),
    Piece(1,3,settings.BLUE_PIECE_COLOR, 2),
    Piece(4,4,settings.BLUE_PIECE_COLOR, 2),
    Piece(3,3,settings.BLUE_PIECE_COLOR, 2),
]