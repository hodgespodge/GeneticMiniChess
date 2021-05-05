from GameBroker import GameBroker
import BoardPresets

from GenticAlgorithm import geneticAlgorithm

# def main(mutation_type, selection_type, reproduction_type, mutation_rate, is_testing):
def main():

    # heuristic values are 0-5:  ["king","queen","rook","bishop","knight","pawn"]

    white_heuristic_coefficients = geneticAlgorithm(initial_input_file=None)
    ##This is our base comparision player?
    
    max_search_time = 1 # Rough upperbound on iterative search (will not interupt search)
    
    game = GameBroker( white_heuristic_coefficients, white_heuristic_coefficients, max_search_time , initial_board = BoardPresets.silverman4x5())

    winner = game.simulate_game(verbose=True)

    if winner == 1:
        print("White Won!")
    elif winner == -1:
        print("Black Won!")

        
if __name__ == "__main__":
    main()
