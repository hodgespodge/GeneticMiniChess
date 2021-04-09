from Board import Board, get_new_board_after_move

class StateNode():

    def __init__(self,board_hash, transposition_table,current_depth, max_depth,first_player,alpha,beta):
        
        self.transposition_table = transposition_table
        self.board_hash = board_hash
        self.children = [] #list of children states
        self.first_player = first_player

        if max_depth - current_depth <= 0: 
            self.value = self.transposition_table[self.board_hash][0].get_board_heuristic()
        else:
            self.value = self.generate_children()
        
        self.transposition_table[self.board_hash][1] = self.value
        self.transposition_table[self.board_hash][2] = max_depth - current_depth

    # WORK IN PROGRESS
    def generate_children(self):

        board = self.transposition_table[self.board_hash][0]

        possible_moves = board.get_all_moves(self.first_player)

        for move in possible_moves:

            child_board = get_new_board_after_move(board,move,first_player = not self.first_player)
            
            child_board_hash = self.transposition_table.add_board(child_board,0,0)

            state_after_move = StateNode(child_board_hash,self.transposition_table,self.current_depth + 1,self.max_depth, not self.first_player,alpha,beta)

            self.children.append(state_after_move)

        # self.children.sort(key= lambda x: x.get_board_heuristic(),reverse=self.first_player)

        if self.first_player:
            return max(child.value for child in self.children)
        else:
            return min(child.value for child in self.children)

        # for child_state in self.children:

        #     child_state.generate_children()


        # self.min_max_value = None #float
        # self.current_depth = None #int


    
class TranspositionTable():
    def __init__(self) -> None:
        self.boards = {}

    def add_board(self,board,min_max_value,depth_searched):
        
        board_hash = board.get_hash_of_board()

        self.boards[board_hash] = (board, min_max_value, depth_searched)

        return board_hash



class GameTree():

    def __init__(self,initial_board, max_depth):

        self.transposition_table = TranspositionTable()
        board_hash = self.transposition_table.add_board(initial_board, initial_board.get_board_heuristic(), 0)
        self.root_node = StateNode(board_hash,self.transposition_table,current_depth=0,max_depth=max_depth)

        self.current_state = self.root_node

    def update_current_state(self,current_board):

        current_board_hash = current_board.get_hash_of_board()

        for state in self.current_state.children: # Find the state that matches the other player's move
            if state.board_hash == current_board_hash:
                self.current_state = state
                
                break

    

        
class Player():

    def __init__(self, heuristic_coefficients = None, max_search_depth = 3,first_player = True):
        
        self.heuristic_coefficients = heuristic_coefficients
        self.max_search_depth = max_search_depth
        self.first_player = first_player

        self.gameTree = None

    def get_move(self,current_board,first_player):

        if self.gameTree is None: # initialize gameTree if not already initialized
            self.gameTree = GameTree(current_board, self.max_search_depth)

        else: # Else gameTree needs to be updated because of oponent's move
            self.gameTree.update_current_state(current_board)



        # PLACE HOLDERS
        best_child_state = None
        move = ((1,1),(2,2),0)

        self.gameTree.current_state = best_child_state

        return move