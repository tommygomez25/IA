
import math
from queue import Queue
import time
PLAYERS = {'none': 0, 'red': 1, 'blue': 2}
EXPLORATION = math.sqrt(2)
from copy import deepcopy
from random import choice
from state import State

class Node:
    def __init__(self, move: tuple=None, parent: object = None):
        self.move = move
        self.parent = parent
        self.N = 0  # times this position was visited
        self.Q = 0  # average reward (wins-losses) from this position
        self.N_RAVE = 0
        self.Q_RAVE = 0
        self.children = {}
        self.outcome = PLAYERS['none']
        
    def add_children(self, children: dict) -> None:
        for child in children:
            self.children[child.move] = child
    
    def value(self, explore:float =EXPLORATION):
        if self.N == 0:
            return 0 if explore == 0 else float('inf')
        else :
            return self.Q / self.N + explore * math.sqrt(2* math.log(self.parent.N)/ self.N)
        
class UctMctsAgent:
    def __init__(self, state: State):
        self.root_state = deepcopy(state)
        self.root = Node()
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0
    
    def best_move(self) -> tuple:
        if self.root_state.get_outcome() != PLAYERS['none']:
            return -1

        # choose the move of the most simulated node breaking ties randomly
        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        bestchild = choice(max_nodes)
        return bestchild.move
    
    #def move(self, move: tuple) -> None:
    #    
    #    if move in self.root.children:
    #        child = self.root.children[move]
    #        child.parent = None
    #        self.root = child
    #        self.root_state.move_piece(self.root_state.get_piece_at(move[0], move[1]), move[2], move[3])
    #        return

        # if for whatever reason the move is not in the children of
        # the root just throw out the tree and start over
        #self.root_state.move_piece(move[0], move[1], move[2], move[3])
       # self.root = Node()
        
    def select_node(self) -> tuple:
        node = self.root
        state = deepcopy(self.root_state)
        
        while len(node.children) != 0:
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value()).value
            max_nodes = [n for n in node.children.values() if n.value == max_value]
            node = choice(max_nodes)
            state = state.move_piece(state.get_piece_at(node.move[0], node.move[1]), node.move[2], node.move[3])
            
            if node.N == 0:
                return node, state
        
        if self.expand(node, state):
            node = choice(list(node.children.values()))
            state = state.move_piece(state.get_piece_at(node.move[0], node.move[1]), node.move[2], node.move[3])
        
        return node,state
    
    @staticmethod
    def expand(parent: Node, state: State) -> bool:
        children = []
        if state.get_outcome() != PLAYERS['none']:
            return False
        
        for move in state.available_moves():
            children.append(Node(move, parent))
        
        parent.add_children(children)
        return True

    @staticmethod
    def roll_out(state: State) -> int:
        
        while state.get_outcome() == PLAYERS['none']:
            possible_moves = state.available_moves()
            if len(possible_moves) == 0:
                break
            move = choice(possible_moves)
            state = state.move_piece(state.get_piece_at(move[0], move[1]), move[2], move[3])
        
        return state.get_outcome()
    
    @staticmethod
    def backup(node: Node, turn: int, outcome: int) -> None:
        
        # the reward is calculated for player who just played at the node and not the next player to play
        
        if outcome == turn :   
            reward = 0
        else: 
            reward = 1
            
         # We alternate between nodes which loser player has chosen and winner player has chosen,
        # so we have to give +1 reward to winner nodes and 0 to loser nodes.
        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
            reward = 0 if reward == 1 else 1
    
    def search(self,time_budget: int) -> None:
      
        num_rollouts = 0
        
        start_time = time.time()

        while  time.time() - start_time < time_budget:
            node, state = self.select_node()
            outcome = self.roll_out(state)
            self.backup(node, state.get_turn(), outcome)
            num_rollouts += 1

        run_time = time.time() - start_time
        node_count = self.tree_size()
        self.node_count = node_count
        self.num_rollouts = num_rollouts
    
    
    def tree_size(self) -> int:

        Q = Queue()
        count = 0
        Q.put(self.root)
        while not Q.empty():
            node = Q.get()
            count += 1
            for child in node.children.values():
                Q.put(child)
        return count
    
    def statistics(self) -> tuple:
        return self.num_rollouts, self.node_count, self.run_time