from GameTree import Player

from Board import Board, get_new_board_after_move, game_over, print_board, get_english_notation

class GameBroker():

    def __init__(self, white_heuristic_coefficients = None, black_heuristic_coefficients = None, max_search_time = 3, initial_board = None):
        
        self.white_heuristic_coefficients = white_heuristic_coefficients
        self.black_heuristic_coefficients = black_heuristic_coefficients
        self.initial_board = initial_board

        self.white_player = Player(self.black_heuristic_coefficients, max_search_time)
        self.black_player = Player(self.white_heuristic_coefficients, max_search_time)
        
    def simulate_game(self,verbose = False):

        board = self.initial_board

        if verbose:
            # print(board)
            print_board(board)

        while(True):

            white_move = self.white_player.get_move(board,first_player = True,verbose=verbose)
            # print("white move:",white_move)
            print("White: ",get_english_notation(white_move))

            board = get_new_board_after_move(board, white_move, first_player= True)

            if verbose:
                print_board(board)

            check_mate, winner = game_over(board=board)
            if check_mate:
                return winner

            black_move = self.black_player.get_move(board, first_player= False, verbose=verbose)

            print("Black: ",get_english_notation(black_move))
            board = get_new_board_after_move(board, black_move, first_player= False)

            if verbose:
                print_board(board)

            check_mate, winner = game_over(board=board)
            if check_mate:
                return winner

   