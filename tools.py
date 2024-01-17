import random
from typing import List, Tuple, Any, Set
import time
import os

TIMEOUT = 30

# FUNCTIONS THAT DO NOT REQUIRE OTHERS

def generateMinefield(numMines : int, sizeX : int, sizeY : int):
    board = [[0 for _ in range(sizeX)] for _ in range(sizeY)]
    for _ in range(numMines):
        x = random.randint(0, sizeX-1)
        y = random.randint(0, sizeY-1)
        while board[y][x] == 1:
            x = random.randint(0, sizeX-1)
            y = random.randint(0, sizeY-1)
        board[y][x] = 1
    return board


def neighborsOfCoord(coord : Tuple[int, int], innerboardlength : int, boardlength : int) -> Set[Tuple[int, int]]:
    neighbors = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            if coord[0] + i < 0 or coord[0] + i >= boardlength or coord[1] + j < 0 or coord[1] + j >=innerboardlength or (i == 0 and j == 0):
                continue
            neighbors.add((coord[0]+i, coord[1]+j))
    return neighbors


# true iff all neighbors of a coordinate have already been revealed
def allNeighborsClear(coord : Tuple[int, int], maskedBoard : List[List[Any]]) -> bool:
    neighbors = neighborsOfCoord(coord, len(maskedBoard[0]), len(maskedBoard))
    for neighbor in neighbors:
        if maskedBoard[neighbor[0]][neighbor[1]] == 'U':
            return False
    return True


# multithread here for different starting locations
def solvable(mineField : List[List[int]], numMines : int) -> bool :
    # call this with multiple threads
    def attemptSolve(start : Tuple[int, int], maskedBoard : List[List[Any]]): # -> Tuple[int, int] | False
        # to be iterated through to find new squares to reveal
        # when a square has then revealed ALL neighbors, removed from set to aid computation time
        revealed = set()
        foundMines = 0
        # fail if it doesn't open anything else on first click
        if mineField[start[0]][start[1]] != 0:
            return False
        for i, j in neighborsOfCoord((start[0], start[1]), len(mineField[0]), len(mineField)):
            revealed.add((i,j))
            maskedBoard[i][j] = mineField[i][j]
        

    # create masked board - U = unrevealed, B = bomb, otherwise number
    masked = list(map(lambda x: list(map(lambda y: 'U', x)), mineField))
    
    pass


def generateNoGuess(numMines : int, sizeX : int, sizeY : int):
    start = time.time()
    while time.time() - start < TIMEOUT:
        tmpBoard = generateNumbers(generateMinefield(numMines, sizeX, sizeY))
        if solvable(tmpBoard, numMines):
            return tmpBoard
    return []


def generateNumbers(board : list):
    numBoard = [[0 for _ in range(len(board[0]))] for _ in range(len(board))]
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == 1:
                numBoard[y][x] = -1
                continue
            for i, j in neighborsOfCoord((y, x), len(board[0]), len(board)):
                if board[i][j] == 1:
                    numBoard[y][x] += 1
    return numBoard