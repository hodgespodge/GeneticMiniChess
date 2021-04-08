from Board import MapOfBoards, Board

class StateNode():

    def __init__(self,board_hash, mapOfBoards,current_depth, max_depth):
        
        self.mapOfBoards = mapOfBoards
        self.board_hash = board_hash
        self.children = None #list of children states
        self.min_max_value = None #float
        self.current_depth = None #int
        
class GameTree():

    def __init__(self,initial_board, max_depth):

        self.mapOfBoards = MapOfBoards()
        board_hash = self.mapOfBoards.add_board(initial_board)

        self.root_node = StateNode(board_hash,self.mapOfBoards,current_depth=0,max_depth=max_depth)
        # self.target_depth = None #int
        
class Player():

    def __init__(self, heuristic_coefficients = [], max_search_depth = 3, initial_board = [],first_player = True):
        
        self.heuristic_coefficients = heuristic_coefficients
        self.max_search_depth = max_search_depth
        self.initial_board = initial_board
        self.first_player = first_player

    def get_move(self,current_board,first_player):

        move = ((1,1),0)

        return move