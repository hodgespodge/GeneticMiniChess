from GameBroker import GameBroker
import BoardPresets
import multiprocessing as mp
import os

def GA_simulate(matches):
    max_search_time = 1 # Rough upperbound on iterative search (will not interupt search)
    
    brokers = []
    for match in enumerate(matches):
        game = GameBroker(match[0], match[1], max_search_time , initial_board = BoardPresets.silverman4x5())
        brokers.append(game)

    initial_board = BoardPresets.silverman4x5()
    max_search_time = 1

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

    return results

def sim_game(gameBroker):

    print("starting process",os.getpid())

    return gameBroker.simulate_game(verbose=False)

    
