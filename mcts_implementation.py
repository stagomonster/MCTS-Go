from go_project import *
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
    
    def violatesKo(self, point):
        
        return False
    
    def gen_playout_move(self): #get a legal action
        point = random_point()
        while self.board_state[point[0], point[1]] != E or self.violatesKo(point):
            point = random_point()
        
        return point
    
    def game_completed(self): #Ignore cases in which playouts of every position would be invalid, edge cases are minimal in effect
        for row in range (len(self.board_state)):
            for col in range(len(self.board_state[0])):
                if self.board_state[row][col] == E:
                    return False
        return True
    
        

def main():
    #TODO main function
    pass
    
    
