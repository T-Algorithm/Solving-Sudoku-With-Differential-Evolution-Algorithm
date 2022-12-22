import numpy as np


# function to return the index(row, column) of value 0
def check(sudoko, arr):
    flag = 0
    for x in range(9):
        for y in range(9):
            if sudoko[x][y] == 0:
                arr[0] = x
                arr[1] = y
                flag = 1
                break
        if flag:
            break
    return flag


# function to check if the number we have chosen is valid for our table or not
def valid(sudoko, row, col, number):
    for x in range(9):
        if sudoko[row][x] == number:
            return False
    for x in range(9):
        if sudoko[x][col] == number:
            return False
    for x in range(3):
        for y in range(3):
            if sudoko[x + (int(row / 3)) * 3][y + (int(col / 3)) * 3] == number:
                return False

    return True


# function to generate random sudoko board with valid values randomly
def randomSudoko(sudoko):
    arr = [0, 0]
    if check(sudoko, arr) == 0:
        return True
    rows = arr[0]
    cols = arr[1]
    for i in range(9):
        numbers = np.random.randint(1, 10)
        if valid(sudoko, rows, cols, numbers):
            sudoko[rows][cols] = numbers
            if randomSudoko(sudoko):
                return True
            sudoko[rows][cols] = 0
    return False


# function to make empty cells randomly
def emptyCells(sudoko, n):
    for i in range(n):
        rows = np.random.randint(9)
        cols = np.random.randint(9)
        while sudoko[rows][cols] == 0:
            rows = np.random.randint(9)
            cols = np.random.randint(9)
        sudoko[rows][cols] = 0
