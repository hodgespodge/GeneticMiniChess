from GameBroker import GameBroker
import BoardPresets

import multiprocessing as mp
import random
# from os import getpid
import os

def sim_game(gameBroker):

    print("starting process",os.getpid())

    return gameBroker.simulate_game(verbose=False)

def main():

    initial_board = BoardPresets.silverman4x5()
    max_search_time = 1

    brokers = []

    for i in range(4):

        # heuristic values are 0-5:  ["king","queen","rook","bishop","knight","pawn"]

        white_heuristic_coefficients = random.sample(range(0,100),6)
        black_heuristic_coefficients = random.sample(range(0,100),6)

        brokers.append(GameBroker(white_heuristic_coefficients,black_heuristic_coefficients,max_search_time,initial_board))

    for broker in brokers:
        print(broker.white_heuristic_coefficients,"vs",broker.black_heuristic_coefficients)

    print("cpus available:",mp.cpu_count())

    with mp.Pool(mp.cpu_count()-1) as pool:
        
        results = pool.map(sim_game, brokers) #pool.map ensures order is maintained

        pool.close()
        pool.join()

        print("multiprocessing done")
    
    print(results)

    for value in results:

        if value == 1:
            print("White Won!")
        elif value == -1:
            print("Black Won!")

if __name__ == "__main__":
    main()


