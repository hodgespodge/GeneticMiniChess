from Board import Board, get_new_board_after_move, get_board_heuristic
from heapq import heappush, heappop
  
def tt_flag_dict():
    return {"EXACT": 0, "LOWERBOUND": 1, "UPPERBOUND": 2}
    
class GameTree():

    def __init__(self,heuristic_coefficients):

        self.transposition_table = {}
        self.heuristic_coefficients = heuristic_coefficients
   
    def get_best_move(self,current_board,max_search_time,first_player):

        current_board_hash = current_board.get_hash_of_board()

        self.transposition_table[current_board_hash] = (current_board,0,0,None)

        # put selection in while loop with increasing depth with timer for iterative deepening
        ###############

        children = []

        import time

        start_time = time.time()

        iterative_depth  = 1
        while (True):
            current_time = time.time()
            if current_time-start_time > max_search_time:
                break
            else:
                children = self.root_negamax(current_board_hash,depth=iterative_depth,alpha=float("-inf"),beta=float("inf"),first_player=first_player)
                iterative_depth += 1
        ################

        best_value = self.transposition_table[children[0][0]][1] # use hash of first child to get its minmax score
        best_move = children[0][1]  # default best move is move of first child

        for child in children:
            if child[0] > best_value:
                best_value = self.transposition_table[children[0]][1]
                best_move = child[1]

        

        return best_move

    def root_negamax(self,board_hash,depth,alpha,beta,first_player):

        alphaOrig = alpha

        ttEntry = self.transposition_table[board_hash]

        if ttEntry[2] >= depth and ttEntry[3] != None: # TT depth
            if ttEntry[3] == tt_flag_dict()["EXACT"]: # TT Flag
                return ttEntry[1] # TT Value

            elif ttEntry[3] == tt_flag_dict()["LOWERBOUND"]: # TT Flag
                alpha = max(alpha, ttEntry[1]) # TT value

            elif ttEntry[3] == tt_flag_dict()["UPPERBOUND"]:
                beta = min(beta, ttEntry[1]) # TT value

            if alpha >= beta:
                return ttEntry[1] # TT value
 
        # TODO need check for terminal board
        terminal_board = False

        if depth == 0 or terminal_board:

            # must check if 1 is correct for first_player
            if first_player:
                return 1 * get_board_heuristic(ttEntry,self.heuristic_coefficients)
            else:

                return -1 * get_board_heuristic(ttEntry)
        
        childNodes = self.generate_ordered_children(board=ttEntry[0],first_player=first_player)
        
        value = float("-inf")

        for child in childNodes:
            child_hash = child[1]
            value = max(value,self.negamax(child_hash,depth-1,alpha=-beta,beta=-alpha,first_player= not first_player))
            alpha = max(alpha,value)

            if alpha >= beta:
                break
        
        if value <= alphaOrig:
            self.transposition_table[board_hash]=(ttEntry[0],value,depth,tt_flag_dict()["UPPPERBOUND"])

        elif value >= beta:
            self.transposition_table[board_hash]=(ttEntry[0],value,depth,tt_flag_dict()["LOWERBOUND"])

        else:
            self.transposition_table[board_hash]=(ttEntry[0],value,depth,tt_flag_dict()["EXACT"])

        return [(child[1],child[2]) for child in childNodes] # return list of (hash, move)

    # https://en.wikipedia.org/wiki/Negamax#Negamax_with_alpha_beta_pruning_and_transposition_tables
    def negamax(self,board_hash,depth,alpha,beta,first_player):
        alphaOrig = alpha

        ttEntry = self.transposition_table[board_hash]
        if ttEntry[2] >= depth and ttEntry[3] != None: # TT depth
            if ttEntry[3] == tt_flag_dict()["EXACT"]: # TT Flag
                return ttEntry[1] # TT Value

            elif ttEntry[3] == tt_flag_dict()["LOWERBOUND"]: # TT Flag
                alpha = max(alpha, ttEntry[1]) # TT value

            elif ttEntry[3] == tt_flag_dict()["UPPERBOUND"]:
                beta = min(beta, ttEntry[1]) # TT value

            if alpha >= beta:
                return ttEntry[1] # TT value

        # TODO chekc for terminal board
        terminal_board = False

        if depth == 0 or terminal_board:

            # must check if 1 is correct for first_player
            if first_player:
                return 1 * get_board_heuristic(ttEntry)
            else:

                return -1 * get_board_heuristic(ttEntry)

        
        childNodes = self.generate_ordered_children(board=ttEntry[0],first_player=first_player)

        
        value = float("-inf")

        for child in childNodes():

            child_hash = child[1]
            value = max(value,self.negamax(child_hash,depth-1,alpha=-beta,beta=-alpha,first_player= not first_player))
            alpha = max(alpha,value)

            if alpha >= beta:
                break
        
        if value <= alphaOrig:
            self.transposition_table[board_hash]=(ttEntry[0],value,depth,tt_flag_dict()["UPPPERBOUND"])

        elif value >= beta:
            self.transposition_table[board_hash]=(ttEntry[0],value,depth,tt_flag_dict()["LOWERBOUND"])

        else:
            self.transposition_table[board_hash]=(ttEntry[0],value,depth,tt_flag_dict()["EXACT"])

        return value

    def generate_ordered_children(self, board,first_player):

        childNodes = []

        possible_moves = board.get_all_moves(first_player)

        for move in possible_moves:

            child_board = get_new_board_after_move(board,move,first_player = not first_player)

            child_board_hash = child_board.get_hash_of_board()

            if self.transposition_table[child_board_hash] != None: # if board already been evaluated to some depth
                child_board_heuristic = self.transposition_table[child_board_hash][1]

            else: # Board not already in transposition table : add board with value = heuristic
                child_board_heuristic = get_board_heuristic(child_board)

                self.transposition_table[child_board_hash] = (child_board, 0,0,None) # Add child board state but no other details

            heappush(childNodes,(child_board_heuristic,child_board_hash,move))

        return [heappop(childNodes) for i in range(len(childNodes))] 


class Player():

    def __init__(self, heuristic_coefficients, max_search_time = 3):
        
        self.heuristic_coefficients = heuristic_coefficients
        self.max_search_time = max_search_time
        self.gameTree = None

    def get_move(self,current_board,first_player):

        if self.gameTree is None: # initialize gameTree if not already initialized
            self.gameTree = GameTree(self.heuristic_coefficients)

        return self.gameTree.get_best_move(current_board,self.max_search_time, first_player)

        