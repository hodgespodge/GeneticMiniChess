from GameBroker import GameBroker
import BoardPresets

def main():

    # heuristic values are 0-5:  ["king","queen","rook","bishop","knight","pawn"]

    white_heuristic_coefficients = [1000, 1, 3, 4, 3, 1]
    black_heuristic_coefficients = [1000, 8, 4, 2, 2, 1]
    max_search_time = 1 # Rough upperbound on iterative search (will not interupt search)
    
    game = GameBroker( white_heuristic_coefficients, black_heuristic_coefficients, max_search_time , initial_board = BoardPresets.silverman4x5())

    winner = game.simulate_game(verbose=True)

    if winner == 1:
        print("White Won!")
    elif winner == -1:
        print("Black Won!")

if __name__ == "__main__":
    main()