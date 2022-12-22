import numpy as np
from Random import randomSudoko, emptyCells
import random
import math

# let's start with random board
answer = np.zeros([9, 9])
flag = False
board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]
randomSudoko(board)
emptyCells(board, 20)

print('   _____           __      __        ')
print('  / ___/__  ______/ /___  / /____  __')
print('  \__ \/ / / / __  / __ \/ //_/ / / /')
print(' ___/ / /_/ / /_/ / /_/ / ,< / /_/ / ')
print('/____/\__,_/\__,_/\____/_/|_|\__,_/  ')

print(' __     ___  ___  ___  __   ___      ___                 ___       __            ___    __ ')
print('|  \ | |__  |__  |__  |__) |__  |\ |  |  |  /\  |       |__  \  / /  \ |    |  |  |  | /  \ |\ | ')
print('|__/ | |    |    |___ |  \ |___ | \|  |  | /~~\ |___    |___  \/  \__/ |___ \__/  |  | \__/ | \|')
print('\n')
print('IMPLEMENTED By Ahmed')
print('IMPLEMENTED By Alzahraa')
print('IMPLEMENTED By Sara')
print('IMPLEMENTED By Nada')
print('IMPLEMENTED By Mariam')
print('--------------------')
print('We are team from Faculty Of Computer and Artificial Intelligence Helwan University')
print('Country : Egypt')
print('--------------------')


# function to make copy from any board
def copyBoard(copyFrom):
    copyTo = []
    for row in range(len(copyFrom)):
        copyTo.append(copyFrom[row].copy())
    return copyTo


# this function take the started board and make random population
def make_population(startedBoard, length):
    pop = []
    for i in range(length):
        person = copyBoard(startedBoard)
        for row in range(9):
            for column in range(9):
                if person[row][column] == 0:
                    person[row][column] = int(random.uniform(1, 9))
        pop.append(person)
    return pop


# we should have functions to get the fitness of the parent
# sudoku will be solved if we haven't any repeated value in each row and column and subgrid(3*3)
# we use the data structure ( set() ) to insert values in it
# the set inserts unique values and ignore the insertion of repeated values
# so if each search in row or column or subgrid(3*3) have unique value so the length of the set should be ( 9 )
# if we have n repeated values the length of the set will be ( 9 - n )
# so if we subtract 9 from the length of the set we will get the length of repeated values
# we will get zero fitness if the all inserted values is unique
# so if we get fitness zero it must be the best solution for our board

# lets start doing our fitness functions


# calculate fitness for row
def row_fitness(chromosome):
    fit = 0
    for row in range(9):
        sett = set()
        for col in range(9):
            sett.add(chromosome[row][col])
        fit += 9 - len(sett)
    return fit


# calculate fitness for column
def col_fitness(chromosome):
    fit = 0
    for col in range(9):
        sett = set()
        for row in range(9):
            sett.add(chromosome[row][col])
        fit += 9 - len(sett)
    return fit


# calculate the fitness for 3*3 subgrid
def fitness9x9(board):
    fit = 0
    for row in range(0, 9, 3):
        for column in range(0, 9, 3):
            fit += fitness3X3Cells(board, row, column)
    return fit


# counting fitness for 3*3 subgrid
def fitness3X3Cells(board, rowIndex, columnIndex):
    startRow = 3 * math.floor(rowIndex / 3)
    startColumn = 3 * math.floor(columnIndex / 3)
    setNumbers = set()
    for i in range(startRow, startRow + 3):
        for j in range(startColumn, startColumn + 3):
            setNumbers.add(board[i][j])

    return 9 - len(setNumbers)


# calculate the fitness of whole board
def fitness_sum(chromosome):
    return row_fitness(chromosome) + col_fitness(chromosome) + fitness9x9(chromosome)


# function to handle the values which greater than 9 and smaller than 1
def overflow(value):
    value = int(value)
    return 1 if value < 1 else 9 if value > 9 else value


# we make mutation in values of zeros to get updated board
def mutation(parent, mutation_factor=0.3):
    parent_size = len(parent)
    vector1 = vector2 = vector3 = None  # we use 3 vectors to make mutant vector
    while vector1 == vector2 or vector1 == vector3 or vector2 == vector3:  # loop to get 3 different index
        vector1 = parent[random.randint(0, parent_size - 1)]
        vector2 = parent[random.randint(0, parent_size - 1)]
        vector3 = parent[random.randint(0, parent_size - 1)]
    mutation_vector = copyBoard(board)
    for row in range(9):
        for col in range(9):
            if mutation_vector[row][col] == 0:  # we make mutation in the empty cells
                mutation_vector[row][col] = overflow(
                    vector3[row][col] + (mutation_factor * (vector1[row][col] - vector2[row][col])))  # Equation
    return mutation_vector  # return the mutant vector


# function to make crossover we create trial vector from  the mutant vector and target vector according cross_prob.
def crossover(donor_vector, parent, chromosome_index, cross_probability=0.4):
    trial_vector = copyBoard(board)
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                if cross_probability >= random.random():  # we use random
                    trial_vector[row][col] = donor_vector[row][
                        col]  # if random value is less CR we use index from mutant
                else:
                    trial_vector[row][col] = parent[chromosome_index][row][col]  # else we use index from target
    return trial_vector  # return mixed vector (trial vector)


# now we have to decide which is better to go to the next population
# the better vector is the vector whose fitness is 0
# so if fitness of the trial vector is less than the fitness of target vector we select trial to next population
def selection(trail_vector, parent, chromosome_index):
    global flag
    global answer
    trial_vector_fitness = fitness_sum(trail_vector)
    target_vector_fitness = fitness_sum(parent[chromosome_index])
    if target_vector_fitness > trial_vector_fitness:  # the less value in the sum of fitness is the best vector
        parent[chromosome_index] = trail_vector
    if fitness_sum(parent[chromosome_index]) == 0:  # if fitness = 0 it means we get the best answer
        answer = parent[chromosome_index]  # so we have to save answer
        flag = True
    return parent


# print the best solution
def print_solution():
    global answer
    print(np.matrix(answer))


# that's our start number of population and iterations
population_size = 200
population = make_population(board.copy(), population_size)
iterations = 100000
answer_index = 0
for i in range(iterations):
    for pop in range(len(population)):
        mutant = mutation(population)  # first step in our algorithm to make mutation
        trial = crossover(mutant, population, pop)  # second step to get the trial vector by making crossover
        population = selection(trial, population, pop)  # third step to select the best parent for the next population
        if flag:  # if flag true it means we get the answer
            answer_index = pop  # save index
            break
    if i % 100 == 0 or flag:  # we print the search for every 100 iteration or if we have found the answer
        print("generation number: ", i, " ", "Best Solution? : ", flag)
    if flag:  # if teh answer found break
        break
print('--------------------')
print_solution()  # print answer
