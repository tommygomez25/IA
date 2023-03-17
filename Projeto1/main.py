import pygame
from mcts import MonteCarloTreeSearchNode
from settings import *
from state import State
from copy import deepcopy
import time


class Game:
    def __init__(self,state, player1, player2):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Black Hole Escape")
        self.clock = pygame.time.Clock()
        self.winner = None
        #self.turn = 1
        self.state = state
        self.player1 = player1
        self.player2 = player2
    
    def new(self):
        self.run()
    
    def run(self,test=False):
        while self.winner is None:
            self.draw()
            if self.state.turn == 1:
                self.player1(self)
            else:
                self.player2(self)
            if self.state.check_win():
                self.winner = 3 - self.state.turn
        if not test:
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
            if self.state.selected_piece != None:
                print("selected piece x: " + str(self.state.selected_piece.x) + " y: " + str(self.state.selected_piece.y))
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
                                    print("I am going to select the piece with coordinates x: " + str(piece.x) + " y: " + str(piece.y)+ "and color: " + str(piece.color))
                                    piece.selected = True
                                    self.state.selected_piece = piece
                                    
                                        
                        print("veio ao if")
                        if self.state.is_valid_move(self.state.selected_piece,mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE):
                            print("valid move")
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
                                    
    def run_n_matches(self, n, max_time = 3600):
        state_copy = deepcopy(self.state)
        start_time = time.time()
        
        results = [0, 0, 0] # [draws, player 1 victories, player 2 victories]
        print(n)
        for i in range(n):
            print(i)
            self.state = deepcopy(state_copy)
            self.run(True)
            print("END GAME")
            results[self.winner] += 1
            self.winner = None
            self.turn = 1
            
            if int(time.time() - start_time) > max_time:
                print("Max time reached!")
                break
            
     
        print("\n=== Elapsed time: %s seconds ===" % (int(time.time() - start_time)))
        print(f"  Player 1: {results[1]} victories")
        print(f"  Player 2: {results[2]} victories")
        print(f"  Draws: {results[0]} ")
        print("===============================")
        # close pygame
        pygame.quit()
            

def execute_human_move(game):
    game.clock.tick(FPS)
    game.events()


def execute_ai_move(evaluate_func, depth):
    def ai_move(game):
        value = minimax(game.state, depth, float('-inf'), float('inf'), True, game.state.turn, evaluate_func)
        print("-------------------")
        print("value: " + str(value))
        for (x,y, newX, newY) in game.state.available_moves():
            print("x: " + str(x) + " y: " + str(y) + " newX: " + str(newX) + " newY: " + str(newY))
            v_kiko = minimax(game.state.move_piece(game.state.get_piece_at(x,y), newX, newY), depth-1, float('-inf'), float('inf'), False, game.state.turn, evaluate_func)
            print("v_kiko: " + str(v_kiko))
            if v_kiko == value:
                game.state = game.state.move_piece(game.state.get_piece_at(x,y), newX, newY)
                break
        
    return ai_move

def execute_ai_move_mcts(game):
    game.clock.tick(FPS)
    root = MonteCarloTreeSearchNode(game.state)
    selected_node = root.best_action()
    #print("selected node: " + str(selected_node.state.pieces))
    game.state = selected_node.state
         
        
        
def minimax(state, depth, alpha, beta, maximizing, player, evaluate_func):
    if depth == 0 or state.check_win():
        if player == 1:
            return evaluate_func(state)
        else:
            return -evaluate_func(state)
    
    if maximizing:
        value = float('-inf')
        for (x, y, newX, newY) in state.available_moves():
            value = max(value, minimax(state.move_piece(state.get_piece_at(x,y),newX, newY), depth - 1, alpha, beta, False, player, evaluate_func))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        value = float('inf')
        for (x, y, newX, newY) in state.available_moves():
            value = min(value, minimax(state.move_piece(state.get_piece_at(x,y),newX, newY), depth - 1, alpha, beta, True, player, evaluate_func))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

    
# prioritizes the number of available moves
def eval_avail_moves(state):
    moves1 = len(state.available_moves())
    new_state = deepcopy(state)
    new_state.turn = 3 - new_state.turn
    moves2 = len(new_state.available_moves())
    return moves1 - moves2
        

# prioritizes the piece going to the black hole
def eval_black_hole(state):
    pieces1 = 0
    pieces2 = 0
    for piece in state.pieces:
        if piece.color == RED_PIECE_COLOR :
            if piece.removed:
                pieces1 += 1              
        elif piece.color == BLUE_PIECE_COLOR:
            if piece.removed:
                pieces2 += 1
    return pieces1 - pieces2


# manhattan distance from center   
def eval_manh_dist(state):
    pieces1 = 0
    pieces2 = 0
    for piece in state.pieces:
        if piece.color == RED_PIECE_COLOR:
            pieces1 += abs(piece.x - 2) + abs(piece.y - 2)
        elif piece.color == BLUE_PIECE_COLOR:
            pieces2 += abs(piece.x - 2) + abs(piece.y - 2)
    return -(pieces1 - pieces2)

# prioritizes pieces that are central
def eval_central_pieces(state):
    pieces1 = 0
    pieces2 = 0
    for piece in state.pieces:
        if piece.color == RED_PIECE_COLOR:
            if (piece.x == 2 and piece.y == 1) or (piece.x == 2 and piece.y == 3) or (piece.x == 1 and piece.y == 2) or (piece.x == 3 and piece.y == 2):
                pieces1 += 1
                # if is in central position, check opposite side and if the player has a piece there that is friendly, add 1000, otherwise subtract 1000
                if piece.x == 2 and piece.y == 1:
                    for p in state.pieces:
                        if (p.x == 2 and p.y == 3 and p.color == RED_PIECE_COLOR ) or (p.x == 2 and p.y == 4 and p.color == RED_PIECE_COLOR):
                            pieces1 += 1
                        elif (p.x == 2 and p.y == 3 and p.color == BLUE_PIECE_COLOR) or (p.x == 2 and p.y == 4 and p.color == BLUE_PIECE_COLOR):
                            pieces1 -= 2
                elif piece.x == 2 and piece.y == 3:
                    for p in state.pieces:
                        if (p.x == 2 and p.y == 1 and p.color == RED_PIECE_COLOR) or (p.x == 2 and p.y == 0 and p.color == RED_PIECE_COLOR):
                            pieces1 += 1
                        elif (p.x == 2 and p.y == 1 and p.color == BLUE_PIECE_COLOR) or (p.x == 2 and p.y == 0 and p.color == BLUE_PIECE_COLOR):
                            pieces1 -= 2
                elif piece.x == 1 and piece.y == 2:
                    for p in state.pieces:
                        if (p.x == 3 and p.y == 2 and p.color == RED_PIECE_COLOR) or (p.x == 4 and p.y == 2 and p.color == RED_PIECE_COLOR):
                            pieces1 += 1
                        elif (p.x == 3 and p.y == 2 and p.color == BLUE_PIECE_COLOR) or (p.x == 4 and p.y == 2 and p.color == BLUE_PIECE_COLOR):
                            pieces1 -= 2
                elif piece.x == 3 and piece.y == 2:
                    for p in state.pieces:
                        if (p.x == 1 and p.y == 2 and p.color == RED_PIECE_COLOR) or (p.x == 0 and p.y == 2 and p.color == RED_PIECE_COLOR):
                            pieces1 += 1
                        elif (p.x == 1 and p.y == 2 and p.color == BLUE_PIECE_COLOR) or (p.x == 0 and p.y == 2 and p.color == BLUE_PIECE_COLOR):
                            pieces1 -= 2
        elif piece.color == BLUE_PIECE_COLOR:
            if (piece.x == 2 and piece.y == 1) or (piece.x == 2 and piece.y == 3) or (piece.x == 1 and piece.y == 2) or (piece.x == 3 and piece.y == 2):
                pieces2 += 1
                # if is in central position, check opposite side and if the player has a piece there that is friendly, add 1000, otherwise subtract 1000
                if piece.x == 2 and piece.y == 1:
                    for p in state.pieces:
                        if p.x == 2 and p.y == 3 and p.color == BLUE_PIECE_COLOR:
                            pieces2 += 1
                        elif p.x == 2 and p.y == 3 and p.color == RED_PIECE_COLOR:
                            pieces2 -= 2
                elif piece.x == 2 and piece.y == 3:
                    for p in state.pieces:
                        if p.x == 2 and p.y == 1 and p.color == BLUE_PIECE_COLOR:
                            pieces2 += 1
                        elif p.x == 2 and p.y == 1 and p.color == RED_PIECE_COLOR:
                            pieces2 -= 2
                elif piece.x == 1 and piece.y == 2:
                    for p in state.pieces:
                        if p.x == 3 and p.y == 2 and p.color == BLUE_PIECE_COLOR:
                            pieces2 += 1
                        elif p.x == 3 and p.y == 2 and p.color == RED_PIECE_COLOR:
                            pieces2 -= 2
                elif piece.x == 3 and piece.y == 2:
                    for p in state.pieces:
                        if p.x == 1 and p.y == 2 and p.color == BLUE_PIECE_COLOR:
                            pieces2 += 1
                        elif p.x == 1 and p.y == 2 and p.color == RED_PIECE_COLOR:
                            pieces2 -= 2
    return pieces1 - pieces2

def eval_mixed(state):
    return eval_avail_moves(state) + 10000 * eval_black_hole(state) + eval_manh_dist(state) + eval_central_pieces(state)

state = State()

#game = Game(state, execute_human_move, execute_human_move) #human vs human
#game = Game(state, execute_human_move, execute_ai_move(eval_mixed,3)) #human vs ai
#game = Game(state, execute_ai_move(eval_mixed,3), execute_human_move) #ai vs human
#game = Game(state, execute_ai_move(eval_mixed,4), execute_ai_move(eval_mixed,3)) #ai vs ai
game = Game(state,execute_human_move, execute_ai_move_mcts)

game.new()

#game.run_n_matches(5)   
