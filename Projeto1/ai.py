import math
from settings import *
from copy import deepcopy
import random
from montecarlo import *

def execute_ai_move(evaluate_func, depth):
    def ai_move(game):
        value = minimax(game.state, depth, float('-inf'), float('inf'), True, game.state.turn, evaluate_func)
        plays = []
        if len(game.state.available_moves()) == 0:
            return
        for (x,y, newX, newY) in game.state.available_moves():
            if minimax(game.state.move_piece(game.state.get_piece_at(x,y), newX, newY), depth-1, float('-inf'), float('inf'), False, game.state.turn, evaluate_func) == value:
                plays.append(game.state.move_piece(game.state.get_piece_at(x,y), newX, newY))
        game.state = random.choice(plays)
    return ai_move         
        
        
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

def execute_monte_carlo_move():
    def ai_move(game):
        game.clock.tick(FPS)
        root = UctMctsAgent(game.state)
        root.search(10)
        move = root.best_move()
        num_rollouts, node_count, run_time = root.statistics()
        game.state = game.state.move_piece(game.state.get_piece_at(move[0], move[1]), move[2], move[3])
        print("Number of rollouts: ", num_rollouts)
        print("Number of nodes: ", node_count)
    return ai_move


def execute_human_move(game):
    game.clock.tick(FPS)
    game.events()
    #print("Game_size:", Game_size//2)
    game.update()

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
        if piece.color == RED_PIECE_COLOR:
            if piece.removed:
                pieces1 += 1              
        elif piece.color == BLUE_PIECE_COLOR:
            if piece.removed:
                pieces2 += 1
    return pieces1 - pieces2


# manhattan distance from center   
def eval_manh_dist(state):
    bh = Game_size//2
    pieces1 = 0
    pieces2 = 0
    for piece in state.pieces:
        if piece.color == RED_PIECE_COLOR:
            if not piece.removed:
                pieces1 += abs(piece.x - bh) + abs(piece.y - bh)
            else:
                pieces1 -= 10
        elif piece.color == BLUE_PIECE_COLOR:
            if not piece.removed:
                pieces2 += abs(piece.x - bh) + abs(piece.y - bh)
            else:
                pieces2 -= 10
    return -(pieces1 - pieces2)

def eval_central_pieces(state):
    bh = Game_size//2
    central_pos = [(bh, bh-1), (bh, bh+1), (bh-1, bh), (bh+1, bh)]
    def calc_score(state, piece, color):
        score = 0
        if piece.color == color:
            if (piece.x, piece.y) in central_pos:
                score += 1
                opp_color = BLUE_PIECE_COLOR if color == RED_PIECE_COLOR else RED_PIECE_COLOR
                if piece.x == 1:
                    opposite_x, opposite_y = central_pos[3]
                elif piece.x == 3:
                    opposite_x, opposite_y = central_pos[2]
                elif piece.y == 1:
                    opposite_x, opposite_y = central_pos[1]
                elif piece.y == 3:
                    opposite_x, opposite_y = central_pos[0]
                for p in state.pieces:
                    if (p.x, p.y) == (opposite_x, opposite_y):
                        if p.color == color:
                            score += 1000
                        elif p.color == opp_color:
                            score -= 1000
        return score

    pieces1 = sum(calc_score(state, piece, RED_PIECE_COLOR) for piece in state.pieces)
    pieces2 = sum(calc_score(state, piece, BLUE_PIECE_COLOR) for piece in state.pieces)

    return pieces1 - pieces2

def eval_mixed(state):
    return eval_manh_dist(state) + eval_avail_moves(state)

def eval_mixed2(state):
    return eval_manh_dist(state) + eval_central_pieces(state) + eval_avail_moves(state)