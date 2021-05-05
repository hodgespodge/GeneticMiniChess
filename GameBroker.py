from GameTree import Player

from Board import Board, get_new_board_after_move, game_over, print_board, get_english_notation

class GameBroker():

    def __init__(self, white_heuristic_coefficients = None, black_heuristic_coefficients = None, max_search_time = 3, initial_board = None):
        
        self.white_heuristic_coefficients = white_heuristic_coefficients
        self.black_heuristic_coefficients = black_heuristic_coefficients
        self.initial_board = initial_board

        self.white_player = Player(self.white_heuristic_coefficients, max_search_time)
        self.black_player = Player(self.black_heuristic_coefficients, max_search_time)
        
    def simulate_game(self,verbose = False):


        board = self.initial_board

        if verbose:
            print_board(board)

        while(True):

            # print("|",flush=True,end="")

            white_move = self.white_player.get_move(board,first_player = True,verbose=verbose)
            if verbose:

                print("White: ",get_english_notation(white_move))

            board = get_new_board_after_move(board, white_move, first_player= True)

            if verbose:
                print_board(board)

            check_mate, winner = game_over(board=board)
            if check_mate:

                # Print out for makeshift progress bar
                if winner == 1:
                    print("W",end="",flush=True)
                elif winner == -1:
                    print("B",end="",flush=True)

                return winner

            black_move = self.black_player.get_move(board, first_player= False, verbose=verbose)

            if verbose:
                print("Black: ",get_english_notation(black_move))
            
            board = get_new_board_after_move(board, black_move, first_player= False)

            if verbose:
                print_board(board)

            check_mate, winner = game_over(board=board)
            if check_mate:

                # Print out for makeshift progress bar
                if winner == 1:
                    print("W",end="",flush=True)
                elif winner == -1:
                    print("B",end="",flush=True)

                return winner

   