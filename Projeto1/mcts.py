import numpy as np
from collections import defaultdict
from state import State

class MonteCarloTreeSearchNode():
    def __init__(self, state : State(), parent=None, parent_action=None):
        self.state = state # board state
        self.parent = parent
        self.parent_action = parent_action # action the parent took that led to this node
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):

        self._untried_actions = self.state.available_moves()
        return self._untried_actions
    
    
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses
    
    def n(self):
        return self._number_of_visits
    
    # expand
    def expand(self):
	
        action = self._untried_actions.pop()
        print("Action: ", action)
        next_state = self.state.move_piece(self.state.get_piece_at(action[0],action[1]),action[2],action[3])
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node 
    
    def is_terminal_node(self):
        return self.state.check_win()
    
    # simulation 
    def rollout(self):
        current_rollout_state = self.state
        
        while not current_rollout_state.check_win():
            
            possible_moves = current_rollout_state.available_moves()
            if (len(possible_moves) == 0):
                break
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move_piece(current_rollout_state.get_piece_at(action[0],action[1]),action[2],action[3])
        print("Rollout outcome : ", current_rollout_state.get_outcome())
        return current_rollout_state.get_outcome()
    
    # backpropagate
    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)
            
    def is_fully_expanded(self):
        return len(self._untried_actions) == 0
    
    def best_child(self, c_param=0.1):
    
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]
    
    # policy to choose the next move, it can be improved by implementing heuristics
    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]
    
    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                return current_node.expand() # expansion
            else:
                current_node = current_node.best_child() # selection 
        return current_node
    
    def best_action(self):
        simulation_no = 100
        
        
        for i in range(simulation_no):
            
            v = self._tree_policy() # selection and expansion -> reaches a terminal node and then simulates a game
            reward = v.rollout() # simulation -> simulates game until the end and returns if the player won or lost
            v.backpropagate(reward) # backpropagation -> updates the results of the nodes in the path from the terminal node to the root node
        
        return self.best_child(c_param=0.)