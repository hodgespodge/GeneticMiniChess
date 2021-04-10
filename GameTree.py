from Board import Board, get_new_board_after_move
from heapq import heappush, heappop
     
class StateNode():

    def __init__(self,board_hash, transposition_table,current_depth, max_depth,first_player,alpha,beta):
        
        self.transposition_table = transposition_table
        self.board_hash = board_hash
        # self.children = [] #list of children states
        self.children_hashes = []
        # self.first_player = first_player
        # self.current_depth = current_depth
        # self.max_depth = max_depth

        terminal = False

        if depth == 0 or terminal:
            self.value =  self.transposition_table[]

        self.children_hashes = self.generate_immediate_children_hashes()

        self.value = self.get_value(alpha,beta)

        # if max_depth - current_depth <= 0: 
        #     self.value = self.transposition_table[self.board_hash][0].get_board_heuristic()
        # else:
        #     self.value = self.generate_children(alpha,beta)
        

        # # transposition_table[board_hash] is (board, min_max_value, depth_searched)
        # self.transposition_table[self.board_hash][1] = self.value
        # self.transposition_table[self.board_hash][2] = max_depth - current_depth

    def get_value(self,alpha, beta):

        

        return 0



    # return unexpanded children sorted by previous knowledge of value
    # Important because then children are evaluated in order of previouse knowledge of importance
    def generate_immediate_children_hashes(self):

        children_hashes = []

        board = self.transposition_table[self.board_hash][0]
        possible_moves = board.get_all_moves(self.first_player)

        ''' 
        transposition_table[board_hash] is (board, min_max_value, depth_searched)
        '''

        for move in possible_moves:

            child_board = get_new_board_after_move(board,move,first_player = not self.first_player)
            # child_board_heuristic = child_board.get_board_heuristic()

            child_board_hash = child_board.get_hash_of_board()

            if self.transposition_table[child_board_hash] != None: # if board already been evaluated to some depth

                child_board_heuristic = self.transposition_table[child_board_hash][2]

            else: # Board not already in transposition table : add board with value = heuristic
                child_board_heuristic = child_board.get_board_heuristic()

                self.transposition_table[child_board_hash] = (child_board, child_board_heuristic,0)

            heappush(children_hashes,(child_board_heuristic,child_board_hash))

        return [heappop(children_hashes)[1] for i in range(len(children_hashes))] # Should return list of hashes sorted by heuristic



            # child_board_hash = self.transposition_table.add_board(child_board,child_board_heuristic,0)



            # child_board = get_new_board_after_move(board,move,first_player = not self.first_player)
            
            # child_board_hash = self.transposition_table.add_board(child_board,0,0)

            # state_after_move = StateNode(child_board_hash,self.transposition_table,self.current_depth + 1,self.max_depth, not self.first_player,alpha,beta)

            # children.append(state_after_move)

        # self.children.sort(key= lambda x: x.get_board_heuristic(),reverse=self.first_player)


        # # TODO make function to check if game over
        # game_over = False

        # if (self.max_depth <= self.current_depth) or game_over:
        #     return 

        # board = self.transposition_table[self.board_hash][0]
        

        # possible_moves = board.get_all_moves(self.first_player)

        # for move in possible_moves:

        #     child_board = get_new_board_after_move(board,move,first_player = not self.first_player)
            
        #     child_board_hash = self.transposition_table.add_board(child_board,0,0)

        #     state_after_move = StateNode(child_board_hash,self.transposition_table,self.current_depth + 1,self.max_depth, not self.first_player,alpha,beta)

        #     self.children.append(state_after_move)

        # # self.children.sort(key= lambda x: x.get_board_heuristic(),reverse=self.first_player)

        # # if self.first_player:

        # #     return max(child.value for child in self.children)
        # # else:
        # #     return min(child.value for child in self.children)




        # for child_state in self.children:
        #     pass

        # return value


        # self.min_max_value = None #float
        # self.current_depth = None #int

def tt_flag_dict():
    return {"EXACT": 0, "LOWERBOUND": 1, "UPPERBOUND": 2}
    
class TranspositionTable():
    def __init__(self) -> None:
        self.boards = {}

    def add_board(self,board,min_max_value,depth_searched,flag_name):
        
        board_hash = board.get_hash_of_board()

        self.boards[board_hash] = (board, min_max_value, depth_searched, tt_flag_dict()[flag_name])

        return board_hash



class GameTree():

    def __init__(self,initial_board, max_depth, first_player):

        self.transposition_table = TranspositionTable()
        board_hash = self.transposition_table.add_board(initial_board, initial_board.get_board_heuristic(), 0)
        self.root_node = StateNode(board_hash,self.transposition_table,current_depth=0,max_depth=max_depth,first_player=first_player, alpha=float('-inf'),beta=float('inf'))

        self.current_state = self.root_node

    def update_current_state(self,current_board):

        current_board_hash = current_board.get_hash_of_board()

        for state in self.current_state.children: # Find the state that matches the other player's move
            if state.board_hash == current_board_hash:
                self.current_state = state
                
                break

    ''' 
    transposition_table[board_hash] is (board, value, depth, flag)
    '''


    # https://en.wikipedia.org/wiki/Negamax#Negamax_with_alpha_beta_pruning_and_transposition_tables
    def negamax(self,board_hash,depth,alpha,beta,color):
        alphaOrig = alpha

        ttEntry = self.transposition_table()[board_hash]
        if ttEntry[2] >= depth: # TT depth
            if ttEntry[3] == tt_flag_dict()["EXACT"]: # TT Flag
                return ttEntry[1] # TT Value

            elif ttEntry[3] == tt_flag_dict()["LOWERBOUND"]: # TT Flag
                alpha = max(alpha, ttEntry[1]) # TT value

            elif ttEntry[3] == tt_flag_dict()["UPPERBOUND"]:
                beta = min(beta, ttEntry[1]) # TT value

            if alpha >= beta:
                return ttEntry[1] # TT value

        terminal_board = False

        if depth == 0 or terminal_board:
            return color * ttEntry.get_board_heuristic()

        childNodes = self.generate_orderd_children()
    
    def generate_orderd_children(self, board,first_player):

        childNodes = []

        possible_moves = board.get_all_moves(first_player)

        ''' 
        transposition_table[board_hash] is (board, min_max_value, depth_searched,flag)
        '''

        for move in possible_moves:

            child_board = get_new_board_after_move(board,move,first_player = not first_player)
            # child_board_heuristic = child_board.get_board_heuristic()

            child_board_hash = child_board.get_hash_of_board()

            if self.transposition_table[child_board_hash] != None: # if board already been evaluated to some depth
                child_board_heuristic = self.transposition_table[child_board_hash][1]

            else: # Board not already in transposition table : add board with value = heuristic
                child_board_heuristic = child_board.get_board_heuristic()

                # self.transposition_table[child_board_hash] = (child_board, child_board_heuristic,0)

            heappush(childNodes,(child_board_heuristic,child_board_hash))

        return [heappop(childNodes) for i in range(len(childNodes))] 



    
        
class Player():

    def __init__(self, heuristic_coefficients = None, max_search_depth = 3,first_player = True):
        
        self.heuristic_coefficients = heuristic_coefficients
        self.max_search_depth = max_search_depth
        self.first_player = first_player

        self.gameTree = None

    def get_move(self,current_board,first_player):

        if self.gameTree is None: # initialize gameTree if not already initialized
            self.gameTree = GameTree(current_board, self.max_search_depth, self.first_player)

        else: # Else gameTree needs to be updated because of oponent's move
            self.gameTree.update_current_state(current_board)



        # PLACE HOLDERS
        best_child_state = None
        move = ((1,1),(2,2),0)

        self.gameTree.current_state = best_child_state

        return move