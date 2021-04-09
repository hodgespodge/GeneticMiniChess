from GameTree import Player

from Board import Board, get_new_board_after_move

class GameBroker():

    def __init__(self, white_heuristic_coefficients = [], black_heuristic_coefficients = [], max_search_depth = 3, initial_board = []):
        
        self.white_heuristic_coefficients = white_heuristic_coefficients
        self.black_heuristic_coefficients = black_heuristic_coefficients
        self.max_search_depth = max_search_depth
        self.initial_board = initial_board

        self.white_player = Player(heuristic_coefficients=self.white_heuristic_coefficients,max_search_depth=self.max_search_depth)
        self.black_player = Player(heuristic_coefficients=self.black_heuristic_coefficients,max_search_depth=self.max_search_depth)

        
    def simulate_game(self):

        board = self.initial_board

        while(True):

            white_move = self.white_player.get_move(board,first_player = True)

            board = get_new_board_after_move(board, white_move, first_player= True)

            black_move = self.black_player.get_move(board, first_player= False)

            board = get_new_board_after_move(board, black_move, first_player= False)

    