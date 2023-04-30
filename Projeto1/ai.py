from settings import *
from copy import deepcopy
import random
from montecarlo import *


def handle_cycles(state, move):
    last_moves = state.p1_last_moves if state.turn == 1 else state.p2_last_moves

    if len(last_moves) == 4 and move in last_moves[::2]:
        move = random.choice(state.available_moves())
    if len(last_moves) == 4:
        last_moves.pop(0)

    last_moves.append(move)
    if state.turn == 1: 
        state.p1_last_moves = last_moves
    else:
        state.p2_last_moves = last_moves

    state = state.move_piece(state.get_piece_at(move[0], move[1]), move[2], move[3])
    return state
        
    

def execute_ai_move(evaluate_func, depth):
    def ai_move(game):
        _, move = minimax(game.state, depth, float('-inf'), float('inf'), True, game.state.turn, evaluate_func)
        state = handle_cycles(game.state, move)
        game.state = state
    return ai_move 
      
def minimax(state, depth, alpha, beta, maximizing, player, evaluate_func):
    if depth == 0 or state.check_win():
        if player == 1:
            return evaluate_func(state), None
        else:
            return -evaluate_func(state), None
    
    if maximizing:
        best_value = float('-inf')
        best_move = None
        for (x, y, newX, newY) in state.available_moves():
            value, _ = minimax(state.move_piece(state.get_piece_at(x,y),newX, newY), depth - 1, alpha, beta, False, player, evaluate_func)
            if value > best_value:
                best_value = value
                best_move = (x, y, newX, newY)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value, best_move
    else:
        best_value = float('inf')
        best_move = None
        for (x, y, newX, newY) in state.available_moves():
            value, _ = minimax(state.move_piece(state.get_piece_at(x,y),newX, newY), depth - 1, alpha, beta, True, player, evaluate_func)
            if value < best_value:
                best_value = value
                best_move = (x, y, newX, newY)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value, best_move

def execute_monte_carlo_move(t=10):
    def ai_move(game):
        game.clock.tick(FPS)
        root = UctMctsAgent(game.state)
        root.search(t)
        move = root.best_move()
        num_rollouts, node_count, run_time = root.statistics()
        game.state = game.state.move_piece(game.state.get_piece_at(move[0], move[1]), move[2], move[3])
        print("Number of rollouts: ", num_rollouts)
    return ai_move


def execute_human_move(game):
    game.clock.tick(FPS)
    game.events()

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

# number of moves
def eval_num_moves(state):
    if state.turn == 1:
        return state.p2_moves -state.p1_moves
    return state.p1_moves -state.p2_moves

# manhattan distance from center   
def eval_manh_dist(state):
    bh = GAME_SIZE//2
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
    bh = GAME_SIZE//2
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
    return eval_manh_dist(state) + eval_avail_moves(state) + eval_num_moves(state)

def eval_mixed2(state):
    return eval_manh_dist(state) + eval_central_pieces(state) + eval_avail_moves(state) + eval_num_moves(state)

def eval_mixed3(state):
    return 4*eval_central_pieces(state) + 100*eval_black_hole(state) - 10*state.p1plays

def eval_mixed4(state):
    return 100*eval_black_hole(state) - 10*state.p1plays + 4*eval_avail_moves(state)
