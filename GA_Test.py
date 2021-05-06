#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 14:03:04 2021

@author: Isabella Samuelsson
"""

from GeneticAlgorithm import single_point_M, swap_M, reverse_M, scramble_M, initPopulation, tournament_S, roulette_S
'''
Calls the init_test() method which tests the initialize 
population function in GeneticAlgorithm.py. This function 
will randomly generate solutions and will show the evaluation 
of there fitness.
'''
def main():
    init_test()

'''
Used to demonstrate the Initialize population functions in 
GeneticAlgorithm.py and the evaluation of one generations 
fitness using the eval_fitness() function.
'''
def init_test():
    values = initPopulation()
    print(values, sep=" ")

'''
Utilized for earlier testing of selection functions.
'''
def selection_test():
    values = initPopulation()
    selected = tournament_S(values)
    print("Len: " + str(len(selected)))
    print(selected, sep=" ")

    selected2 = roulette_S(values)
    print("Len: " + str(len(selected2)))
    print(selected2, sep=" ")

'''
Utilized for earlier testing of mutation functions.
'''
def mutation_test():
    test_arr = [1,2,3,4,5,6]
    # Mutation Tests
    print("Single Point M")
    print("Before ")
    print(test_arr, sep=" ")
    print("here")
    single_point_M(test_arr)
    print("/n")

    print("Swap M")
    print(test_arr, sep=" ")
    swap_M(test_arr)
    print("/n")

    print("Reverse M")
    print(test_arr, sep=" ")
    reverse_M(test_arr)
    print("/n")

    print("Scramble M")
    print(test_arr, sep=" ")
    scramble_M(test_arr)
    print("/n")

def reproduction_test():
    print("")


if __name__ == "__main__":
    main()
