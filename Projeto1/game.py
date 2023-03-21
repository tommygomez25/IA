import pygame
import pygame_menu
from settings import *
from piece import Piece
from state import State



class Game:
    def __init__(self,state, player1, player2):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
    

    # def pause(self):
    #     pause_theme = pygame_menu.Theme(background_color=(255, 255, 255, 200))
    #     menu = pygame_menu.Menu('Black-hole Escape!', SCREEN_WIDTH, SCREEN_HEIGHT, theme=pause_theme)
    #     menu.add.button('Return to game', action=lambda self: self.playing:=False)
    #     menu.add.button('Back to menu')
    #     menu.add.button('Quit', pygame_menu.events.EXIT)
    #     menu.mainloop(self.screen)

    def run(self):
        while self.winner is None:
            self.draw()
            if self.state.turn == 1:
                self.player1(self)
            else:
                self.player2(self)
            if self.playing == False:
                self.pause()
            if self.state.check_win():
                self.winner = 3 - self.state.turn
            
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
                    return 0
            
             # if a piece is selected, listen to mouse movements and clicks to move the piece
            if self.state.selected_piece != None:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        # if the mouse is clicked on a friendly piece, select it
                        for piece in self.state.pieces:
                            if (piece.color == RED_PIECE_COLOR and self.state.turn == 1 and piece != self.state.selected_piece )or (piece.color == BLUE_PIECE_COLOR and self.state.turn == 2 and piece != self.state.selected_piece):
                                if pygame.Rect(piece.x*TILE_SIZE, piece.y*TILE_SIZE, TILE_SIZE, TILE_SIZE).collidepoint(mouse_pos):
                                    #select piece and desselect others
                                    for p in self.state.pieces:
                                        p.selected = False
                                    
                                    self.state.selected_piece = piece
                                    
                                        
 
                        if self.state.is_valid_move(self.state.selected_piece,mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE):
                            
                            self.state = self.state.move_piece(self.state.selected_piece,mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE)
                            self.state.selected_piece = None
                    
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        for piece in self.state.pieces:
                            if (piece.color == RED_PIECE_COLOR and self.state.turn == 1) or (piece.color == BLUE_PIECE_COLOR and self.state.turn == 2):
                                if pygame.Rect(piece.x*TILE_SIZE, piece.y*TILE_SIZE, TILE_SIZE, TILE_SIZE).collidepoint(mouse_pos) and not piece.removed:
                                    #select piece and desselect others
                                    for p in self.state.pieces:
                                        p.selected = False
                                    piece.selected = True
                                    self.state.selected_piece = piece

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

    
