#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 10:22:51 2021

@author: Isabella Samuelsson
"""
import random
import copy
import datetime
from GA_simulate import GA_simulate

# seed the random number generator for testing
random.seed(10)

# Fitness Map which holds solution as a Key and int fitness as Value
fitness = {}
# Mutation Operator Type
m_type = None
# Selection Operator type
s_type = None
# Reproduction Operator Type
r_type = None
# Mutation Rate
m_rate = None

# Stopping Criteria for GA means a solution beat each of the players it played against
stopping_fitness = 3
# Number of generations
generation_count = 0
# Population Size
population_size  = 20
# Max value of a variable
value_scale      = 100
# Number of heuristic values
num_values       = 6
# Output File
output_file      = 0
# If Testing
testing = ""

# Main for if just running GA
def main():
    geneticAlgorithm()
'''
This is the method that is called from TODO. It starts 
the Genetic Algorithm and returns the best found heuristic 
piece values array. This method can take a specified mutation,
 reproduction and selection operator along with a mutation 
 rate, an is testing boolean variable ('T' for true anything else for false)
 and an input file which specifies a set of an initial population 
 size list of solutions to seed the GA with.
'''
def geneticAlgorithm(initial_input_file = None, mutation_type = 'swap', selection_type = 'roulette', reproduction_type = 'single_point', mutation_rate = 0.3, is_testing= 'F'):
    global output_file, m_rate, m_type, r_type, testing, s_type

    if is_testing == "T":
        now = "output_" + str(datetime.datetime.now())
        output_file = open(now, "w")
    
    m_type = mutation_type
    s_type = selection_type
    r_type = reproduction_type
    m_rate = mutation_rate
    
    testing = is_testing
    
    initialPopulation = []
    
    if initial_input_file:
        file = open(initial_input_file, "r")
        i = 0
        while i != population_size:
            line = file.readLine(12)
            arr = line.split()
            initialPopulation.append(arr)
            i += 1
        file.close()
    else:
        pop = initPopulation()
        initialPopulation.append(pop)
    
    best_found = geneticAlg(initialPopulation)
    
    output_file.close()
    
    return best_found
    

'''
Randomly initializes the population and calls eval_fitness 
to evaluate the fitness of the generated solutions.
'''
def initPopulation():
    # population size: 20
    # scale of values: 0-100
    values = []
    i = 0
    while i != population_size:
        values.append([])
        j = 0
        while j != num_values:
            val = random.randint(0, value_scale)
            values[i].append(val)
            j += 1
        i += 1
    eval_fitness(values)
    print("len values :", len(values))
    print("fitness: ", fitness.values())
        
    return values           
 
    
        
'''
Evaluates the fitness of the population. Groups the 
parameter population into 5 groups of 4 solutions. Each 
solution competes against other member solutions of a group 
for a total of 3 games per solution. The fitness of a solution 
is the number of games won. This function creates an array 
of matches pairs which is used as a parameter in the call to 
GA_Simulate(). GA_Simulate will use MultiProcessing to run 
all the matches in the matches array. The fitness dictionary 
takes the solution array as a key and the fitness (# of wins) 
as the value.
'''
def eval_fitness(children):
    for _, child in enumerate(children):
        fitness[tuple(child)] = 0
         
    groups = []
    i = 0
    while i != 5:
        groups.append([i, i + 5, i + 10, i + 15])
        # groups.append([i, i + 4, i + 8, i + 12, i + 16])
        i += 1
        
    matches = []

    for _, group in enumerate(groups):
    
        group_copy = copy.deepcopy(group)
        for ix, child_i_1 in enumerate(group):
            group_copy[ix] = None
            for _, child_i_2 in enumerate(group_copy):
                if child_i_2 is not None:
                    arr = [children[child_i_1], children[child_i_2]]
                    matches.append(arr)
                
    scores = GA_simulate(matches)
    i = 0
    stop = len(matches)
    while i != stop:
        if scores[i] == 1:
            fitness[tuple(matches[i][0])] += 1
        elif scores[i] == -1:
            fitness[tuple(matches[i][1])] += 1
        i += 1
                 

'''
Called by GeneticAlgorithm() to continue creating and 
evaluating new generations of solutions until the stopping 
criteria is met.
'''
def geneticAlg(population):

    global generation_count
    
    if testing == "T":
        print("Initial Generation: 0 Population \n")
        print(population)
        print('\n')
        
        output_file.write("Initial Generation: 0 Population \n")
        i = 0
        while i != population_size:
            output_file.write(str(population[i]))
            print(len(population))
            print(i)
            i += 1
        print('\n')
        
    next_gen = []
    
    # Selection
    selected = selection(population)

    # Reproduce
    i = 0
    while i < len(selected):
        child_1, child_2 = reproduction(selected[i], selected[i+1])
        # Mutate
        chance_1 = random.random()
        chance_2 = random.random()
        # What percent chance?
        if chance_1 < m_rate:
            mutation(child_1)
        if chance_2 < m_rate:
            mutation(child_2)
            
        next_gen.append(child_1)
        next_gen.append(child_2)
        i += 2
        
    # Assign fitness to new gen
    generation_count += 1
    fitness.clear()
    eval_fitness(next_gen)
    print("len values :", len(next_gen))
    print("fitness: ", fitness.values())

    best_found_index = 0 
    best_fit = 0

    for ix, individual in enumerate(next_gen):
    #    str_individual = ''.join([str(elem) for elem in individual])
        if fitness[tuple(individual)] > best_fit:
            best_found_index = ix
            best_fit = fitness[tuple(individual)]

    if testing == "T":
        print("Generation : %s Fittest : %s Population: " % (generation_count, best_fit))
        print(next_gen)
        print("\n")
        
        output_file.write("Generation : %s Fittest : %s Population: " % (generation_count, best_fit));
        output_file.write(next_gen + "\n");
    
    if stopping_fitness > best_fit:
        geneticAlg(next_gen)
    else:
        return next_gen[best_found_index]


'''
Calls the specified mutation operator on the 
parameter child solution.
'''
def mutation(child):
    if m_type == 'single_point':
        single_point_M(child)
    elif m_type == 'swap':
        swap_M(child)
    elif m_type == 'reverse':
        reverse_M(child)    
    else:
        scramble_M(child)

'''
Calls the specified reproduction operator on the 
two parameter parent solution, returns two offspring solutions.
'''
def reproduction(parent_1, parent_2):
    if r_type == 'single_point':
        return single_point_C(parent_1, parent_2)

    return uniform_C(parent_1, parent_2)
    
'''
Calls the specified selection operator on the 
population, returns selected individuals for 
crossover array.
'''
def selection(population):
    if s_type == 'roulette':
        return roulette_S(population)
    return tournament_S(population)

# General Mutation Methods
'''
Mutation Operator. Single Point Mutation randomly 
chooses a single index and sets it to a random value.
'''
def single_point_M(child):
    mutation = random.randint(0,value_scale)

    m_location = random.randint(0, num_values - 1)

    child[m_location] = mutation
    
'''
Mutation operator. Swap Mutation selects two random 
locations and switches the values at the locations.
'''
def swap_M(child):
    loc_1 = random.randint(0, num_values - 1)
    loc_2 = random.randint(0, num_values - 1)
    
    save = child[loc_1]
    
    child[loc_1] = child[loc_2]
    child[loc_2] = save
    
'''
Mutation Operator. Reverse Mutation reverses 
the order of the values in the array.
'''
def reverse_M(child):
    reverse = child[::-1]
    i = 0
    while i != num_values:
        child[i] = reverse[i]
        i += 1
'''
Mutation Operator. Scramble Mutation randomly 
arranges the values in the array.
'''
def scramble_M(child):
    copy_child = copy.deepcopy(child)
    i = 0

    while len(copy_child) != 0:
        value = random.choice(copy_child)
        copy_child.remove(value)
        child[i] = value
        i += 1

# General Crossover Methods
'''
First Crosssover function option. Single Point Crossover 
randomly selects a crossover index and has the first part 
of the child donate by 1 parent and the second part after 
the index from the other parent.
'''
def single_point_C(parent_1, parent_2):
    child_1 = []
    child_2 = []
    loc_1 = random.randint(0, num_values - 1)
    i = 0
    while i != loc_1:
        child_1.append(parent_1[i])
        child_2.append(parent_2[i])
        i += 1
    i = loc_1
    while i != num_values:
       child_1.append(parent_2[i])
       child_2.append(parent_1[i])
       i += 1
       
    return child_1, child_2    
    
'''
Second Crosssover function option. Uniform Crossover 
has a 50% probability that each value in the child 
solution comes for either parent. 
'''
def uniform_C(parent_1, parent_2):
    child_1 = []
    child_2 = []
    i = 0
    
    while i != num_values:
        coin = random.randint(0,1)
        if coin == 1:
            child_1.append(parent_1[i])
            child_2.append(parent_2[i])
        else:
            child_1.append(parent_2[i])
            child_2.append(parent_1[i])
        i += 1
        
    return child_1, child_2

# General Selection Methods
'''
First Selection function option. Roulette Selection assigns a probability 
to each solutions which is based on the fitness and the 
overall fitness's of the solutions. Because of this there is 
a higher probability that fit solutions will be selected. 
'''
def roulette_S(population):
    sum_fitness = 0
    for _, individual in enumerate(population):
        sum_fitness += fitness[tuple(individual)]
     
    probability = []
    sum_of_prob = 0
    for _, individual in enumerate(population):
        p = sum_of_prob + ((fitness[tuple(individual)]*1.0)/sum_fitness)
        probability.append(p)
        sum_of_prob += p
        
    size_pop = len(population)
    selected = []
    while len(selected) != size_pop:
        num = random.random()
        for i, individual in enumerate(population):
            if num <= probability[i]:
                selected.append(individual)
                break
            
    return selected

'''
Second Selection function option. Tournament Selection continuously 
selects a group of k individuals and selects the highest 
fitness individual for crossover. This is done until 
the specified number of solutions (population size) 
are selected. 
'''
def tournament_S(population):
    # tournament size? paper says less then 10
    t_size = 3
    size_pop = len(population)
    selected = []
    
    i = 0
    while i != size_pop:
        k = 0
        best_fit = 0
        best_index = 0
        while k != t_size:
            index = random.randint(0, size_pop - 1)
            arr = population[index]
            if fitness[tuple(arr)] > best_fit:
                best_fit = fitness[tuple(arr)]
                best_index = index
            k += 1
        selected.append(population[best_index])
        i += 1
    
    return selected

if __name__ == "__main__":
    main()

