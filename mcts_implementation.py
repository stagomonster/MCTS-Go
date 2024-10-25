from go_project import *
import numpy as np
from collections import defaultdict

'''
TODO: 

backpropogation -> validate results of node
apply/modify current tree policy
decision making dependent on both quality + confidence (n)
efficiency in data management
efficiency in tracking progress

hash instantiation for KO (low priority)
'''

class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return
    
    def untried_actions(self): #Potential moves
        if self.untried_actions == None:
            return self.state.get_legal_actions()
        for row in self.untried_actions:
            for col in self.untried_actions[0]:
                pass
        legal_actions = self.state.get_legal_actions()
        
        return legal_actions
    
    def q(self): 
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses
    
    def expand(self): 
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node 
    
    def is_terminal_node(self): 
        return self.state.is_game_over()

    def rollout(self):
        current_rollout_state = self.state
        
        while not current_rollout_state.is_game_over():
            
            possible_moves = current_rollout_state.get_legal_actions()
            
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

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

    def rollout_policy(self, possible_moves): #May Change
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self): #May Change
        current_node = self
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100
        for i in range(simulation_no):
            
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        
        return self.best_child(c_param=0.)
    
    def get_legal_actions(self): 
        #TODO: Make more efficient by recording move hash
        arr = [[0 for row in range(len(self.state))] for col in range(0,len(self.state[0]))]

        for row in range(len(self.state)):
            for col in range(len(self.state[0])):
                if self.state[row][col] == E:
                    arr[row][col] = 1
                else:
                    arr[row][col] = 0
        return arr

    def is_game_over(self):
        for row in range (len(self.state)):
            for col in range(len(self.state[0])):
                if self.board_state[row][col] == E:
                    return False
        return True

    def game_result(self):
        return self.is_game_over()

    def move(self):
        point = random_point()
        while self.board_state[point[0], point[1]] != E or self.violatesKo(self.state, point, zobrist):
            point = random_point()
                
        return point
        

def violatesKO(state, move, hashlist): 
    return False #Accuracy negligible, checking may impact performance
    #  r_squares = check_captures(state)
    # return True if len(r_squares) > 0 else False

def main():
    root = MonteCarloTreeSearchNode(state = board)
    selected_node = root.best_action()
    return


# #tree policy: 50% children, node, may modify


