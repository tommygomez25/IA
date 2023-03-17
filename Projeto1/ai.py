import math
from settings import *
from copy import deepcopy

def execute_ai_move(difficulty, evaluate_func):
    def ai_move(game):
        game.clock.tick(FPS)
        game.state.selected_piece = None
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
