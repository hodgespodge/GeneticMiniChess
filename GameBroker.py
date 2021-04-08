from GameTree import Player, Board

class GameBroker():

    def __init__(self, white_heuristic_coefficients = [], black_heuristic_coefficients = [], max_search_depth = 3, initial_board = []):
        
        self.white_heuristic_coefficients = white_heuristic_coefficients
        self.black_heuristic_coefficients = black_heuristic_coefficients
        self.max_search_depth = max_search_depth
        self.initial_board = initial_board

        self.white_player = Player(heuristic_coefficients=self.white_heuristic_coefficients,max_search_depth=self.max_search_depth,initial_board=self.initial_board)
        self.black_player = Player(heuristic_coefficients=self.black_heuristic_coefficients,max_search_depth=self.max_search_depth,initial_board=self.initial_board)

        
    def simulate_game(self):

        board = self.initial_board

        while(True):

            board = board.get_new_board_after_move()

            board = self.white_player.get_move(board,first_player = True)

            board = self.black_player.get_move(board,first_player = False)
    
    