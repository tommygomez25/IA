import math
import time
from settings import *
from copy import deepcopy


def execute_ai_move(difficulty, evaluate_func):
    def ai_move(game):
        game.state.selected_piece = None
        move = minimax(game.state, difficulty,0,0,True, game.turn,evaluate_func)[1]
        game.state = game.state.move_piece(game.state.get_piece_at(move[0], move[1]),move[2], move[3])
        print("AI moved from " + str(move[0]) + "," + str(move[1]) + " to " + str(move[2]) + "," + str(move[3]))
        game.turn = 3 - game.turn
    return ai_move

def minimax(game_state, depth, alpha, beta, maximizing, player, evaluate_func):
    if depth == 0:
        return (evaluate_func(game_state),None)
    
    available_moves = game_state.available_moves(player)

    if maximizing:
        max_value = -math.inf
        for move in available_moves:
            state_after_move = game_state.move_piece(game_state.get_piece_at(move[0], move[1]),move[2], move[3])
            evaluation = minimax(state_after_move, depth-1, alpha, beta, False,player, evaluate_func)[0]
            max_value = max(max_value, evaluation)
            moveF=move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return (max_value, moveF)
    else:
        min_value = math.inf
        for move in available_moves:
            state_after_move = game_state.move_piece(game_state.get_piece_at(move[0], move[1]),move[2], move[3])
            evaluation = minimax(state_after_move, depth-1, alpha, beta, True,player, evaluate_func)[0]
            min_value = min(min_value, evaluation)
            moveF=move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return (min_value, moveF)

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