from GameBroker import GameBroker
import BoardPresets

def main(mutation_type, selection_type, reproduction_type, mutation_rate, is_testing):

    # heuristic values are 0-5:  ["king","queen","rook","bishop","knight","pawn"]

    white_heuristic_coefficients = GeneticAlgorithm.geneticAlgorithm(mutation_type, selection_type, reproduction_type, mutation_rate, is_testing)
    ##This is our base comparision player?
    black_heuristic_coefficients = GeneticAlgorithm.geneticAlgorithm(mutation_type, selection_type, reproduction_type, mutation_rate, is_testing)
    max_search_time = 1 # Rough upperbound on iterative search (will not interupt search)
    
    game = GameBroker( white_heuristic_coefficients, black_heuristic_coefficients, max_search_time , initial_board = BoardPresets.silverman4x5())

    winner = game.simulate_game(verbose=True)

    if winner == 1:
        print("White Won!")
    elif winner == -1:
        print("Black Won!")
        
def GA_simulate(matches):
    max_search_time = 1 # Rough upperbound on iterative search (will not interupt search)
    
    brokers = []
    for match in enumerate(matches):
        game = GameBroker( match[0], match[1], max_search_time , initial_board = BoardPresets.silverman4x5())
        brokers.append(game)
        
    

if __name__ == "__main__":
    main()
