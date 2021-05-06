from GameTree import Player

from Board import Board, get_new_board_after_move, game_over
from MiscFunctions import get_english_notation, print_board, reverse_alphabet
import time

# Print out for makeshift progress bar
def _progress_bar_print(winner):
    if winner == 1:
        print("W",end="",flush=True)
    elif winner == -1:
        print("B",end="",flush=True)
    elif winner == 0:
        print("D",end="",flush=True)

# Brokers a game between 2 AIs with heuristic coefficients
class GameBroker():

    def __init__(self, white_heuristic_coefficients = None, black_heuristic_coefficients = None, max_search_time = 3, initial_board = None):
        
        self.white_heuristic_coefficients = white_heuristic_coefficients
        self.black_heuristic_coefficients = black_heuristic_coefficients
        self.initial_board = initial_board

        self.white_player = Player(self.white_heuristic_coefficients, max_search_time)
        self.black_player = Player(self.black_heuristic_coefficients, max_search_time)
    
    
    # Simulate a full game and return an int for the winner (-1, 0, or 1)
    def simulate_game(self,verbose = 0, max_game_time = 60):

        if verbose == False:
            verbose = 0

        start_time = time.time()

        board = self.initial_board

        if verbose > 0:
            print_board(board)

        while(True):

            white_move, draw = self.white_player.get_move(board,first_player = True,verbose=verbose)
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


            if (time.time() - start_time > max_game_time) or draw:
                return 0

            black_move, draw = self.black_player.get_move(board, first_player= False, verbose=verbose)

            if verbose > 0:
                print("Black: ",get_english_notation(black_move))
            
            board = get_new_board_after_move(board, black_move, first_player= False)

            if verbose > 1:
                print_board(board)

            end, winner = game_over(board=board, first_player= True)
            if end:

                if verbose == -1:
                    _progress_bar_print(winner)

                return winner

            if (time.time() - start_time > max_game_time) or draw:
                return 0

# Brokers a game between an agent and a human 
class InteractiveBroker():
    
    def __init__(self, AI_heuristic_coefficients = None, first_player= True, max_search_time = 3, initial_board = None):

        self.AI_heuristic_coefficients = AI_heuristic_coefficients
        self.initial_board = initial_board
        self.first_player = first_player
        
        self.AI_player = Player(self.AI_heuristic_coefficients ,max_search_time)

    def check_if_end(self, board,verbose, player):
        end, winner = game_over(board, player)
            
        if end:
            if winner == 0:
                print("Draw")
            elif (winner == -1 and not self.first_player) or (winner == 1 and self.first_player) :
                print("Human Won!")
            else: 
                print("AI Won!")

            return True

    def ai_turn(self,board,verbose):
        move, draw = self.AI_player.get_move(board,first_player = not self.first_player,verbose=verbose)

        if verbose > 0:
            if self.first_player:

                print("White: ",get_english_notation(move))

        board = get_new_board_after_move(board, move, first_player= not self.first_player)

        if verbose > 1:
            print_board(board)

        return board

    def human_turn(self, board, verbose):
        print("Available moves:")
        possible_moves = board.get_all_moves(self.first_player)

        for move in possible_moves:
            print(get_english_notation(move))

        while(True):

            player_input = input().split()

            try:

                before = player_input[0]
                after = player_input[1]

                before = (reverse_alphabet()[before[0]] ,int(before[1])-1)
                after = (reverse_alphabet()[after[0]],int(after[1])-1)

                if board[before] == 5 and ( after[1] == board.board_dimensions[1]):
                    player_move = (before,after,1)
                elif board[before] == 11 and ( after[1] == 0):
                    player_move = (before,after,6)
                else:
                    player_move = (before,after,board[before])

                if player_move not in possible_moves:
                    print("Move not possible.")
                else:
                    break

            except:
                print("Invalid input. Try again")

        board = get_new_board_after_move(board, player_move, first_player= self.first_player)

        if verbose > 1:
            print_board(board)

        return board
        
    def play_game(self,verbose = 2):

        if verbose == False:
            verbose = 0

        board = self.initial_board

        if verbose > 0:
            print_board(board)

        if self.first_player:
            board = self.human_turn(board, verbose)
            if self.check_if_end(board,verbose,player= not self.first_player):
                print("game ended in first turn")

        while(True):

            board = self.ai_turn(board, verbose)
            if self.check_if_end(board,verbose,player= self.first_player):
                break
            
            board = self.human_turn(board, verbose)
            if self.check_if_end(board,verbose,player= not self.first_player):
                break
