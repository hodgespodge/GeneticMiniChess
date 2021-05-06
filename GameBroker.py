from GameTree import Player

from Board import Board, get_new_board_after_move, game_over
from MiscFunctions import get_english_notation, print_board
import time

# Print out for makeshift progress bar
def _progress_bar_print(winner):
    if winner == 1:
        print("W",end="",flush=True)
    elif winner == -1:
        print("B",end="",flush=True)
    elif winner == 0:
        print("D",end="",flush=True)

class GameBroker():

    def __init__(self, white_heuristic_coefficients = None, black_heuristic_coefficients = None, max_search_time = 3, initial_board = None):
        
        self.white_heuristic_coefficients = white_heuristic_coefficients
        self.black_heuristic_coefficients = black_heuristic_coefficients
        self.initial_board = initial_board

        self.white_player = Player(self.white_heuristic_coefficients, max_search_time)
        self.black_player = Player(self.black_heuristic_coefficients, max_search_time)
    
    # Print out for makeshift progress bar

    def simulate_game(self,verbose = 0, max_game_time = 60):

        if verbose == False:
            verbose = 0

        start_time = time.time()

        board = self.initial_board

        if verbose > 0:
            print_board(board)

        while(True):

            white_move= self.white_player.get_move(board,first_player = True,verbose=verbose)
            if verbose > 0:
                print("White: ",get_english_notation(white_move))

            board = get_new_board_after_move(board, white_move, first_player= True)

            if verbose > 1:
                print_board(board)

            end, winner = game_over(board=board, first_player=False)
            if end:

                if verbose == -1:
                    _progress_bar_print(winner)

                return winner

            if time.time() - start_time > max_game_time:
                return None

            black_move = self.black_player.get_move(board, first_player= False, verbose=verbose)

            if verbose > 0:
                print("Black: ",get_english_notation(black_move))
            
            board = get_new_board_after_move(board, black_move, first_player= False)

            if verbose > 1:
                print_board(board)

            end, winner = game_over(board=board, first_player= True)
            if end:

                if verbose == -1:
                    _progress_bar_print(winner)

                return None

            if time.time() - start_time > max_game_time:
                break
