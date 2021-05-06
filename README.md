# GeneticMiniChess
Final project for CSC 520

By Samuel Hodges and Isabella Samuelsson



> python3 TestAgents.py

    This will start up a match between an AI agent and another AI agent. This file is just an example of how one may use the functions and of how the Genetic Algorithm simulates a single match. You may edit any of the variables passed to GameBroker.py for a different gameplay experience. Both players have their own list of heuristic weight values. Max_search_time is a rough bound on the allowed itereative deepening search time. Initial board takes any of the starting boards defined in BoardPreset.py. The verbose keyword argument in simulate game determines how much information is printed to the terminal.

> python3 PlayGame.py

    This will start up a match between an AI agent and the player. This file is just an example of how one may use the functions and does not support command like args yet. You may edit any of the variables passed to InteractiveBroker.py for a different gameplay experience. AI_heuristic_coefficients is a list of the ordered piece weights, first_player is a bool which if set true the human is white, max_search_time is a rough bound on the allowed itereative deepening search time. Initial board takes any of the starting boards defined in BoardPreset.py. The verbose keyword argument in play game determines how much information is printed to the terminal.



> python3 GeneticAlgorithm.py

    This will call the main method which will call the geneticAlgorithm() method. GeneticAlgorithm can take a very long time and uses multiprocessing. This method takes an initial input file, mutation type, selection type, crossover type mutation rate and a boolean value if testing. The initial input file is if you would like to seed the GA with a specified initial population. The selection, crossover and mutation types are to specify which type of operator to use as we have implemented multiple types. We have it set to default parameters of initial_input_file = None, mutation_type = 'swap', selection_type = 'roulette', reproduction_type = 'single_point', mutation_rate = 0.3, is_testing= ’F’. This does not use an initial input file. The main method will initialize the population and start the GA. When a generation is being evaluated for fitness the matches pairs will print out (solution vs solution) and wether a game has been a draw = D, white won = W or black won = B. Also after the fitness’s have been evaluated the fitness dictionary will be printed out so the number of simulated games won per solution can be viewed. This will continue until one of the solutions has met the stopping criteria fitness.


> GA_Test.py

    This will call main() then the init_test() method. This will go through the initializing population function in GeneticAlgorithm.py. This will demonstrate one generation being randomly created and the simulation of the games to demonstrate the fitness’s of the solutions being evaluated. The solutions vs solution matches will be printed out solution vs solution) and wether a game has been a draw = D, white won = W or black won = B. Also after the fitness’s have been evaluated the fitness dictionary will be printed out so the number of simulated games won per solution can be viewed.
