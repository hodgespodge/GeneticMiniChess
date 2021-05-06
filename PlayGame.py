from GameBroker import InteractiveBroker
import BoardPresets

def main():

    # heuristic values are 0-5:  ["king","queen","rook","bishop","knight","pawn"]

    AI_heuristic_coefficients = [10, 10, 3, 4, 3, 1]
    
    max_search_time = 0.5 # Rough upperbound on iterative search (will not interupt search)
    
    game = InteractiveBroker( AI_heuristic_coefficients , first_player= True,  max_search_time = max_search_time,initial_board = BoardPresets.silverman4x4())

    game.play_game(verbose=2)

if __name__ == "__main__":
    main()