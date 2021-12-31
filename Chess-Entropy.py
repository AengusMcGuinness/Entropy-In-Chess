#!/usr/bin/env python3
import sys, os
import numpy as np
import chess.pgn
import math
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
"""Up There are the dependencies exluding re, sys, and os the rest are standard"""
"""Here is where the pgn files are from https://theweekinchess.com/a-year-of-pgn-game-files"""

numFiles = len(sys.argv)
iterableFiles = range(1, numFiles)
baseName = [sys.argv[i][0:-4] for i in iterableFiles]

def main():
    runtime = datetime.now()
    dt_string = runtime.strftime("%d-%H-%M-%S")
    data = {}
    totalMoves = []
    totalEntropies = []
    dataFile = open(f"run-data-{dt_string}.out", 'w')
    for i in iterableFiles:
        with open(sys.argv[i]) as pgn:
            game = chess.pgn.read_game(pgn)
            board = game.board()
            for moveNum, move in enumerate(game.mainline_moves()):
                legalMoves = list(board.legal_moves)
                numLegalMoves = len(list(board.legal_moves))
                if moveNum % 2 == 0:
                    dataFile.write(f"Player: White Move Number: {moveNum} Move: {move} Entropy: {shannonEntropy(numLegalMoves)} Number of Legal Moves: {numLegalMoves}\n")
                else:
                    dataFile.write(f"Player: Black Move Number: {moveNum} Move: {move} Entropy: {shannonEntropy(numLegalMoves)} Number of Legal Moves: {numLegalMoves}\n")
                board.push(move)
                totalMoves.append(moveNum)
                totalEntropies.append(shannonEntropy(numLegalMoves))
        data.update({baseName[i-1]: [totalMoves, totalEntropies]})
        totalMoves = []
        totalEntropies = []
    dataFile.close()
    plot(data, dt_string)
                
def shannonEntropy(numMoves):
    log2 = lambda a: math.log(a, 2)
    entropies = []
    for i in range(numMoves):
        moveEntropy = (1/numMoves)*log2(1/numMoves)
        entropies.append(moveEntropy)
    entropy = -1*sum(entropies)
    return entropy

def plot(data, dt_string):
    plt.figure()
    for i in list(data.keys()):
        plt.plot(data[i][0], data[i][1], label=f"{i}")
    plt.xlabel('Moves')
    plt.ylabel('Entropy')
    plt.title('Entropy over Time in Chess')
    plt.savefig(f"figure-{dt_string}.png")
    plt.show()

#I AM GOING TO MAKE A WHOLE SEPERATE FILE FOR SVG GENERATION
    
# def printAll(data):
#     for i in list(data.keys()):
#         print(i)
#         moves = len(data[i][0])
#         print(moves)
#         entropies = len(data[i][1])
#         print(entropies)

# def chessSVGS(moveNum, board, baseName, i):
#     f = open(f"{baseName[i-1]}-move{moveNum}gameState.svg", "x")
#     f.write(chess.svg.board(board, size = 350))
#     f.close()

# def svgDictionary(moveNum, numLegalMoves, i):
#     svgData = {}
#     if moveNum % 2:
#         svgData.update({f"{baseName[i-1]}{moveNum}gameState.svg": [numLegalMoves, "Black",  shannonEntropy(numLegalMoves)]})
#     else:
#         svgData.update({f"{baseName[i-1]}{moveNum}gameState.svg": [numLegalMoves, "White", shannonEntropy(numLegalMoves)]})

    
if __name__ == "__main__":
    main()
