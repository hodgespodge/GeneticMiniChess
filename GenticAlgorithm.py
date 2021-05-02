#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 10:22:51 2021

@author: Isabella Samuelsson
"""
import random
import copy
import datetime
from SimulateGame.py import GA_simulate

fitness = {}
m_type = ""
s_type = ""
r_type = ""
m_rate = 0

stopping_fitness = 5 #beats all selected to play against
generation_count = 0
population_size  = 20
value_scale      = 100
num_values       = 6
output_file      = 0

testing = ""
#Notes: save to text file population
#Set initial from text file


#Should we have a time limit? if at time return best have
def geneticAlgorithm(mutation_type, selection_type, reproduction_type, mutation_rate, is_testing, initial_input_file):
    if is_testing == "T":
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        output_file = open("output_" + dt_string, "w")
    
    m_type.append(mutation_type)
    s_type.append(selection_type)
    r_type.append(reproduction_type)
    m_rate.append(mutation_rate)
    
    testing.append(is_testing)
    
    initialPopulation = []
    
    if initial_input_file != "F":
        file = open(initial_input_file,"r")
        line = file.readLine(12)
        arr = line.split()
        initialPopulation.append(arr)      
        file.close()
    else:
        pop = initPopulation()
        initialPopulation.append(pop)
    
    best_found = geneticAlg(initialPopulation)
    
    output_file.close()
    
    return best_found
    


def initPopulation():
    #population size: 20
    #scale of values: 0-100
    values = []
    i = 0
    while i != population_size:
        values[i] = []
        j = 0
        while j != num_values:
            val = random.randint(0,value_scale)
            values[i].append(str(val))
            j += 1
        i += 1 
        
    k = 0
    while k < num_values:
        eval_fitness(values[k], values[k+1])
        k += 2
        
    return values           
 
    
        
    
def eval_fitness(children):
     #what to value: #wins
     #plays against evryone / 1/5 pop
    for child in enumerate(children):
        fitness[child].append(0)
         
    groups = []
    i = 0
    while i != 5:
        groups[i] = [children[i], children[i + 5], children[i + 10], children[i + 15]]
        i += 1
        
    matches = []
    
         
    for group in enumerate(groups):
    
        group_copy = copy.deepcopy(group)
        for child_i_1 in enumerate(group):
            group_copy.remove(child_i_1)
            for child_i_2 in enumerate(group_copy):
                matches.append([children[child_i_1], children[child_i_2]])
                
        GA_simulate(matches)
                 


def geneticAlg(population):
    
    if testing == "T":
        print("Initial Generation: 0 Population \n")
        print(population + "\n")
        
        output_file.write("Initial Generation: 0 Population \n");
        output_file.write(population + "\n");
        
    next_gen = []
    
    #Selection
    selected = selection(population)

    #Reproduce
    i = 0
    while i < len(selected):
        child_1, child_2 = reproduction(selected[i], selected[i+1])
        #Mutate
        chance_1 = random.random()
        chance_2 = random.random()
        #What percent chance?
        if chance_1 < m_rate:
            mutation(child_1)
        if chance_2 < m_rate:
            mutation(child_2)
            
        next_gen.append(child_1)
        next_gen.append(child_2)
        i += 2
        
    #Assign fitness to new gen
    generation_count += 1
    fitness.clear()
    eval_fitness(next_gen)
    
    
    best_found_index = 0 
    best_fit = 0
   
    
    #if can play    
    #Check stopping criteria
    #should say continue even if lower if have more time?
    if testing == "T":
        print("Generation : %s Fittest : %s Population: " % (generation_count, best_fit))
        print(next_gen)
        print("\n")
        
        output_file.write("Generation : %s Fittest : %s Population: " % (generation_count, best_fit));
        output_file.write(next_gen + "\n");
    
    if stopping_fitness > best_fit:
        geneticAlg(next_gen)
    else:
        print()
        return next_gen[best_found_index]



def mutation(child):
    if m_type == 'single_point':
        single_point_M(child)
    elif m_type == 'swap':
        swap_M(child)
    elif m_type == 'reverse':
        reverse_M(child)    
    else:
        scramble_M(child)
    
    
def reproduction(parent_1, parent_2):
    if r_type == 'single_point':
        single_point_C(parent_1, parent_2)   
    else:
        uniform_C(parent_1, parent_2)
    
    
def selection(population):
    if s_type == 'roulette':
        roulette_S(population)   
    else:
        tournament_S(population)    
    
 
#General Mutation Methods    
    
def single_point_M(child):
    mutation = random.randint(0,value_scale)
    print("Mutation:" + mutation)
    m_location = random.randint(0, num_values - 1)
    print("Location: " + m_location) 
    child[m_location] = mutation
    print("Mutated: " + child)
    
    
def swap_M(child):
    loc_1 = random.randint(0, num_values - 1)
    loc_2 = random.randint(0, num_values - 1)
    print("Location1: " + loc_1 + "Location2: " + loc_2)
    
    save = child[loc_1]
    
    child[loc_1] = child[loc_2]
    child[loc_2] = save
    
    print("Mutated: " + child)
    
       
def reverse_M(child):
    reverse = child[::-1]
    for i in child:
        child[i] = reverse[i]
    print("Mutated: " + child)
    
def scramble_M(child):
    copy_child = copy.deepcopy(child)
    i = 0
    
    while len(copy_child) != 0:
        value = random.choice(copy_child)
        copy_child.remove(value)
        child[i] = value
        i += 1
        
    
#General Crossover Methods    
    
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
    

    
   
    
#General Selection Methods 
    
def roulette_S(population):
    sum_fitness = 0
    for individual in enumerate(population):
        sum_fitness += fitness[individual]
     
    probability = []
    sum_of_prob = 0
    for individual in enumerate(population):
        p = sum_of_prob + ((fitness[individual]*1.0)/sum_fitness)
        probability.append(p)
        sum_of_prob += p
        
    size_pop = len(population)
    selected = []
    while len(selected) != size_pop:
        num = random.random()
        for (i, individual) in enumerate(population):
            if num <= probability[i]:
                selected.append(individual)
                break
            
    return selected
        
    
def tournament_S(population):
    #tournament size? paper says less then 10 
    t_size = 3
    size_pop = len(population)
    selected = []
    
    i = 0
    while i != size_pop:
        tournament = []
        k = 0
        index = 0
        best_fit = 0
        best_index = 0
        while k != t_size:
            index = random.randint(0,size_pop - 1)
            tournament.append(population[index])
            if fitness[population[index]] > best_fit:
                best_fit = fitness[population[index]]
                best_index = index
            
        selected.append(population[best_index])
        i += 1
    
    return selected
    
