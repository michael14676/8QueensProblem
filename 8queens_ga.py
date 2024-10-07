import random as rand
import numpy as np
from chessboard import ChessBoard
import heapq

POPULATION_SIZE = 15
GENERATION_LIMIT = 10000
MUTATION_RATE = 0.05

def queen_list(queens):
    # takes str of queen positions and converts to list
    return [int(x) for x in queens]


def queen_str(queens):
    # takes list of queen positions and converts to str
    return ''.join(str(i) for i in queens)


def natural_selection(population):
    # returns 2 random individuals as parents, based on fitness. input is dict of individual:fitness
    weighted_population = {}
    if len(population) == 1: # if only one individual due to repeats
        return [max(population), max(population)]
    for individual in population:
        weighted_population[individual] = rand.random() * (population[individual]) ** 2 * np.sign(population[individual])    # randomly selected, weighted
    return heapq.nlargest(2, weighted_population, key=weighted_population.__getitem__)  # return the top 2 individuals as parents in list form


def mutation(individual):
    # get lists of len 8 representing queens, and randomly mutates 1 value
    individual[rand.randint(0, 7)] = rand.randint(0, 7)
    return individual


def reproduction(x, y):
    # get 2 parents with queens in list form to produce one child, then performs crossover
    c = rand.randint(1, len(x) - 1)
    return x[:c] + y[c:]

def genetic_algorithm(population, GENERATION_LIMIT, MUTATION_RATE):
    # population is a dict of individual:fitness. individual is in string
    POPULATION_SIZE = len(population)
    generations = 0
    best_fitness = -float('inf')  # Track best fitness found
    no_improvement_counter = 0
    while no_improvement_counter < GENERATION_LIMIT:
        new_population = {}
        for i in range(POPULATION_SIZE):
            parents = natural_selection(population)
            x = parents[0]
            y = parents[1]
            child = reproduction(queen_list(x), queen_list(y))
            if rand.random() <= MUTATION_RATE:  # chance of mutation
                child = mutation(child)
            board = ChessBoard(child)
            new_population[queen_str(child)] = board.fitness_fn()
        population = new_population

        # do it until we find a solution: fitness function = 32
        best = queen_list(max(population))
        board = ChessBoard(best)
        new_best_fitness = board.fitness_fn()
        if new_best_fitness > best_fitness:
            best_fitness = new_best_fitness
            no_improvement_counter = 0
        else:
            no_improvement_counter += 1
        # print(new_best_fitness, best)
        if best_fitness == 32:
            # print(f'{generations} generations')
            return best  # return best result
        generations += 1

    # if no solutions found
    # print(f'{generations} generations')
    return 'No result found.'

# generate random initial population of 8
population1 = {}
for i in range(0, POPULATION_SIZE):
    queens = [0, 1, 2, 3, 4, 5, 6, 7]
    rand.shuffle(queens)
    board = ChessBoard(queens)
    population1[queen_str(queens)] = board.fitness_fn()

print(genetic_algorithm(population1, GENERATION_LIMIT, MUTATION_RATE))


# example solution
# board = ChessBoard([0,6,4,7,1,3,5,2])
# print(board.board)
# print(board.fitness_fn())
