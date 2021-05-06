from GameBroker import GameBroker
import BoardPresets

def main():

    # heuristic values are 0-5:  ["king","queen","rook","bishop","knight","pawn"]

    white_heuristic_coefficients = [10, 10, 3, 4, 3, 1]
    black_heuristic_coefficients = [10, 10, 3, 4, 3, 1]
    max_search_time = 0.5 # Rough upperbound on iterative search (will not interupt search)
    
    # game = GameBroker( white_heuristic_coefficients, black_heuristic_coefficients, max_search_time , initial_board = BoardPresets.silverman4x5())
    
    game = GameBroker( white_heuristic_coefficients, black_heuristic_coefficients, max_search_time , initial_board = BoardPresets.unfair())

    winner = game.simulate_game(verbose=2,max_game_time=60)

    # if winner is None:
    #     print("Game ran out of time")

    if winner == 1:
        print("White Won!")
    elif winner == -1:
        print("Black Won!")
    elif winner == 0:
        print("Draw!")

if __name__ == "__main__":
    main()