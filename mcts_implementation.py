import go_project_old
import numpy as np



#tree policy: 50% children, node, may modify

class MCTS:
    def __init__(self, state, parent=None): 
        #TODO complete implementation of init mcts
        self.board_state = state #current state
        self.parent = parent #last_move
        self.children = []
        self.unvisited_nodes = []
        self.settled = False
        self.hash = 0 
        self.number_visits = 0
        

        pass
    def expand(self):
        pass
    def backpropogate(self, result):
        pass

    def visits(self):
        return self.number_visits
    
    def gen_playout_moves(self): #get legal actions
        pass
    
    def game_completed(self):
        pass
        

def main():
    #TODO main function
    pass
    
    
