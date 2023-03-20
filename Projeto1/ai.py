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
    return ai_move


def execute_human_move(game):
    game.clock.tick(FPS)
    game.events()
    game.update()

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
