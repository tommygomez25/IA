import pygame
from piece import Piece
from settings import *
from state import State
import math
from copy import deepcopy
import time


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
                            self.state = self.state.move_piece(self.state.selected_piece,mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE)
                            self.selected_piece = None
                            self.turn = 3 - self.turn
                    
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
                                        self.state.selected_piece = piece
            

def execute_human_move(game):
    game.clock.tick(FPS)
    game.events()
    game.update()

def execute_ai_move(difficulty, evaluate_func):
    def ai_move(game):
        game.clock.tick(FPS)
        value = minimax(game.state, difficulty, -math.inf, math.inf, True, game.turn, evaluate_func)
        for (x,y, newX, newY) in game.state.available_moves(game.turn):
            new_state = game.state.move_piece(game.state.get_piece_at(x, y),newX, newY)
            if value == minimax(new_state, difficulty - 1, -math.inf, math.inf, False, game.turn, evaluate_func):
                game.state = game.state.move_piece(game.state.get_piece_at(x, y),newX, newY)
                print("AI moved from " + str(x) + "," + str(y) + " to " + str(newX) + "," + str(newY))
                break
        game.update()
        game.turn = 3 - game.turn
    return ai_move

def minimax(state, depth, alpha, beta, maximizing, player, evaluate_func):
    if depth == 0 :
        if player == 1:
            return evaluate_func(state)
        else:
            return -evaluate_func(state)
    
    if maximizing:
        value = -math.inf
        for (x, y, newX, newY) in state.available_moves(player):
            state_copy = deepcopy(state)
            state_copy = state_copy.move_piece(state_copy.get_piece_at(x,y),newX, newY)
            value = max(value, minimax(state_copy, depth - 1, alpha, beta, False, player, evaluate_func))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        value = math.inf
        for (x, y, newX, newY) in state.available_moves(player):
            state_copy = deepcopy(state)
            state_copy = state_copy.move_piece(state_copy.get_piece_at(x,y),newX, newY)
            value = min(value, minimax(state_copy, depth - 1, alpha, beta, True, player, evaluate_func))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def evaluate_f1(state):
    pieces1 = 0
    pieces2 = 0
    for piece in state.pieces:
        if piece.color == RED_PIECE_COLOR:
            if piece.removed:
                pieces1 += 1000
            else:
                pieces1 += len(piece.available_moves(state))
        elif piece.color == BLUE_PIECE_COLOR:
            if piece.removed:
                pieces2 += 1000
            else:
                pieces2 += len(piece.available_moves(state))
    return pieces1 - pieces2

def evaluate_f2(state):
    #manhattan distance from center
    pieces1 = 0
    pieces2 = 0
    for piece in state.pieces:
        if piece.color == RED_PIECE_COLOR:
            if piece.removed:
                pieces1 += 1000
            else:
                pieces1 -= abs(piece.x - 2) + abs(piece.y - 2)
        elif piece.color == BLUE_PIECE_COLOR:
            if piece.removed:
                pieces2 += 1000
            else:
                pieces2 -= abs(piece.x - 2) + abs(piece.y - 2)
    return pieces1 - pieces2

def evaluate_f3(state):
    # join two other heuristics
    return evaluate_f1(state) + evaluate_f2(state)

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
game = Game(state, execute_human_move, execute_ai_move(5, evaluate_f3)) #human vs ai
#game = Game(state, execute_ai_move(5, evaluate_f1), execute_human_move) #ai vs human
#game = Game(state, execute_ai_move(7, evaluate_f3), execute_ai_move(7, evaluate_f2)) #ai vs ai

while True:
    game.new()
    
