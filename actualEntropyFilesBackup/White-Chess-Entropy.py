#!/usr/bin/env python3
import asyncio
import sys, os
import numpy as np
import chess.pgn
import chess.engine
import math
import itertools
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
#Up There are the dependencies exluding re, sys, and os the rest are standard
#Here is where the pgn files are from https://theweekinchess.com/a-year-of-pgn-game-files

numFiles = len(sys.argv)
iterableFiles = range(1, numFiles)
baseName = [sys.argv[i][0:-4] for i in iterableFiles]
log2 = lambda a: math.log(a, 2)

def main():
    #This is the time which is the name of each file so they are unqiue each time
    runtime = datetime.now()
    dt_string = runtime.strftime("%d-%H-%M-%S")
    #the data we graph is in a dictionary
    data = {}
    #These go in the dictionary as a list of lists
    totalMoves = []
    totalShannonEntropies = []
    totalConditionalEntropies = []
    totalJointEntropy = []
    #open our data file which we write our statistics to
    dataFile = open(f"run-data-{dt_string}.out", 'w')
    #This iterates over all of the pgn files
    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
    for i in iterableFiles:
        with open(sys.argv[i]) as pgn:
            #reads in the pgn and makes a chess board
            game = chess.pgn.read_game(pgn)
            board = game.board()
            dataFile.write(f"Game {i} and File Name {baseName[i-1]}\n")
            for moveNum, move in enumerate(game.mainline_moves()):
                #This only does the calculations if it is the white players move
                if moveNum % 2 == 0:
                    moveTo = (str(move)[2::])
                    if len(moveTo) == 3:
                        moveTo = moveTo[:-1]
                    piece = board.piece_at(chess.parse_square(moveTo))
                    info = engine.analyse(board, chess.engine.Limit(time=0.1))
                    betterMoves = info["pv"]
                    numBetterMoves = len(betterMoves)
                    board.push(move)
                    info = engine.analyse(board, chess.engine.Limit(time=0.01))
                    newBetterMoves = len(info["pv"])
                    if moveNum % 2 == 0:
                        dataFile.write(f"Player: White Move Number: {moveNum} Move: {move} Piece: {piece} Number of Better Moves: {numBetterMoves} Entropy: {shannonEntropy(numBetterMoves)} Conditional Entropy: {conditionalEntropy(numBetterMoves, newBetterMoves)} Joint Entropy: {jointEntropy(numBetterMoves, newBetterMoves)}\n")
                    else:
                        dataFile.write(f"Player: Black Move Number: {moveNum} Move: {move} Piece: {piece} Number of Better Moves: {numBetterMoves} Entropy: {shannonEntropy(numBetterMoves)} Conditional Entropy: {conditionalEntropy(numBetterMoves, newBetterMoves)} Joint Entropy: {jointEntropy(numBetterMoves, newBetterMoves)}\n")
                    totalMoves.append(moveNum)
                    totalShannonEntropies.append(shannonEntropy(numBetterMoves))
                    totalConditionalEntropies.append(conditionalEntropy(numBetterMoves, newBetterMoves))
        #updates the data with the data filename:[stats, stats, stats]
        data.update({baseName[i-1]: [totalMoves, totalShannonEntropies, totalConditionalEntropies, totalJointEntropy]})
        #empties the lists so we can fill and repeat with the next pgn file
        totalMoves = []
        totalShannonEntropies = []
        totalConditionalEntropies = []
        totalJointEntropy = []
        print(f"File {i} has completed")
    plotShannonEntropy(data, dt_string)
    plotBestFitShannonEntropy(data, dt_string)
    plotConditionalEntropy(data, dt_string)
    plotBestFitConditionalEntropy(data, dt_string)

def jointEntropy(numLegalMoves, newNumMovesCon):
    jointEntropies = []
    try:
        pX = 1/numLegalMoves
        pY = 1/newNumMovesCon
        pXY = pX * pY
        for i in range(numLegalMoves):
            jointEntropies.append(pXY * (log2(pXY)))
        for i in range(newNumMovesCon):
            jointEntropies.append(pXY * (log2(pXY)))
        jointEntropy = -1 * sum(jointEntropies)
    except ZeroDivisionError:
        jointEntropy = 0
    return jointEntropy

def plotBestJointEntropy(data, dt_string):
    bestFitXs = []
    bestFitYs = []
    plt.figure()
    for i in list(data.keys()):
        plt.scatter(data[i][0], data[i][3])
        bestFitXs.append(data[i][0])
        bestFitYs.append(data[i][3])
    bestFitXs = np.array(list(itertools.chain(*bestFitXs)))
    bestFitYs = np.array(list(itertools.chain(*bestFitYs)))
    m, b = np.polyfit(bestFitXs, bestFitYs, 1)
    plt.plot(bestFitXs, m * bestFitXs + b, label="Linear Regression")
    plt.xlabel('Moves')
    plt.ylabel('Joint Entropy')
    plt.title('Entropy over Time in Chess')
    plt.savefig(f"figure-joint-best-{dt_string}.png")
    plt.show()

def plotJointEntropy(data, dt_string):
    plt.figure()
    for i in list(data.keys()):
        plt.plot(data[i][0], data[i][3])
    plt.xlabel('Moves')
    plt.ylabel('Joint Entropy')
    plt.title('Entropy over Time in Chess')
    plt.savefig(f"figure-joint-{dt_string}.png")
    plt.show()


def conditionalEntropy(numLegalMoves, newNumMovesCon):
    conEntropies = []
    try:
        pX = 1/numLegalMoves
        pY = 1/newNumMovesCon
        pXY = pX * pY
        for i in range(numLegalMoves):
            conEntropies.append(pXY * (log2(pX)/pXY))
        for i in range(newNumMovesCon):
            conEntropies.append(pXY * (log2(pX)/pXY))
        conditionalEntropy = -1 * sum(conEntropies)
    except ZeroDivisionError:
        conditionalEntropy = 0
    return conditionalEntropy
    
def shannonEntropy(numMoves):
    entropies = []
    for i in range(numMoves):
        moveEntropy = (1/numMoves)*log2(1/numMoves)
        entropies.append(moveEntropy)
    entropy = -1*sum(entropies)
    return entropy

def plotConditionalEntropy(data, dt_string):
    plt.figure()
    for i in list(data.keys()):
        plt.plot(data[i][0], data[i][2])
    plt.xlabel('Moves')
    plt.ylabel('Conditional Entropy')
    plt.title('Entropy over Time in Chess')
    plt.savefig(f"figure-conditional-{dt_string}.png")
    plt.show()


def plotBestFitConditionalEntropy(data, dt_string):
    bestFitXs = []
    bestFitYs = []
    plt.figure()
    for i in list(data.keys()):
        plt.scatter(data[i][0], data[i][2])
        bestFitXs.append(data[i][0])
        bestFitYs.append(data[i][2])
    bestFitXs = np.array(list(itertools.chain(*bestFitXs)))
    bestFitYs = np.array(list(itertools.chain(*bestFitYs)))
    m, b = np.polyfit(bestFitXs, bestFitYs, 1)
    print(f"Slope: {m}")
    plt.plot(bestFitXs, m * bestFitXs + b, label="Linear Regression")
    plt.xlabel('Moves')
    plt.ylabel('Condtional Entropy')
    plt.title('Entropy over Time in Chess')
    plt.savefig(f"figure-conditional-best-{dt_string}.png")
    plt.show()

    
def plotBestFitShannonEntropy(data, dt_string):
    bestFitXs = []
    bestFitYs = []
    plt.figure()
    for i in list(data.keys()):
        plt.scatter(data[i][0], data[i][1])
        bestFitXs.append(data[i][0])
        bestFitYs.append(data[i][1])
    bestFitXs = np.array(list(itertools.chain(*bestFitXs)))
    bestFitYs = np.array(list(itertools.chain(*bestFitYs)))
    m, b = np.polyfit(bestFitXs, bestFitYs, 1)
    print(f"Slope: {m}")
    plt.plot(bestFitXs, m * bestFitXs + b, label="Linear Regression")
    plt.xlabel('Moves')
    plt.ylabel('Shannonian Entropy')
    plt.title('Entropy over Time in Chess')
    plt.savefig(f"figure-shannon-best-{dt_string}.png")
    plt.show()


def plotShannonEntropy(data, dt_string):
    plt.figure()
    for i in list(data.keys()):
        plt.plot(data[i][0], data[i][1])
    plt.xlabel('Moves')
    plt.ylabel('Shannonian Entropy')
    plt.title('Entropy over Time in Chess')
    plt.savefig(f"figure-shannon-{dt_string}.png")
    plt.show()

    
if __name__ == "__main__":
    main()

    #             #This identifies the piece on the square we move t
    #             moveTo = (str(move)[2::])
    #             if len(moveTo) == 3:
    #                 moveTo = moveTo[:-1]
    #             piece = board.piece_at(chess.parse_square(moveTo))
    #             #calculates the number of moves and the list of moves
    #             legalMoves = list(board.legal_moves)
    #             numLegalMoves = len(list(board.legal_moves))
    #             #writes the data alternating white and then black
    #             #pushes the board state to the next one
    #             board.push(move)
    #             #calculates the new set of moves for conditional entropy
    #             newNumMovesCon = len(list(board.legal_moves))
    #             if moveNum % 2 == 0:
    #                 dataFile.write(f"Player: White Move Number: {moveNum} Move: {move} Piece: {piece} Number of Legal Moves: {numLegalMoves} Entropy: {shannonEntropy(numLegalMoves)} Conditional Entropy: {conditionalEntropy(numLegalMoves, newNumMovesCon)} Joint Entropy: {jointEntropy(numLegalMoves, newNumMovesCon)}\n")
    #             else:
    #                 dataFile.write(f"Player: Black Move Number: {moveNum} Move: {move} Piece: {piece} Number of Legal Moves: {numLegalMoves} Entropy: {shannonEntropy(numLegalMoves)} Conditional Entropy: {conditionalEntropy(numLegalMoves, newNumMovesCon)} Joint Entropy: {jointEntropy(numLegalMoves, newNumMovesCon)}\n")
    #             #append the moves and entropies to our data
    #             totalMoves.append(moveNum)
    #             totalShannonEntropies.append(shannonEntropy(numLegalMoves))
    #             totalConditionalEntropies.append(conditionalEntropy(numLegalMoves, newNumMovesCon))
    #             totalJointEntropy.append(jointEntropy(numLegalMoves, newNumMovesCon))
    #     #updates the data with the data filename:[stats, stats, stats]
    #     data.update({baseName[i-1]: [totalMoves, totalShannonEntropies, totalConditionalEntropies, totalJointEntropy]})
    #     #empties the lists so we can fill and repeat with the next pgn file
    #     totalMoves = []
    #     totalShannonEntropies = []
    #     totalConditionalEntropies = []
    #     totalJointEntropy = []
    # #close the file
    # dataFile.close()
    # #plots different junk
    # plotShannonEntropy(data, dt_string)
    # plotBestFitShannonEntropy(data, dt_string)
    # plotConditionalEntropy(data, dt_string)
    # plotBestFitConditionalEntropy(data, dt_string)
    # plotJointEntropy(data, dt_string)
    # plotBestJointEntropy(data, dt_string)
