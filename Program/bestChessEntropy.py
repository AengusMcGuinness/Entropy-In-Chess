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
                if moveNum % 2 != 0:
                    #This only does the calculations if it is the white players move
                    moveTo = (str(move)[2::])
                    if len(moveTo) == 3:
                        moveTo = moveTo[:-1]
                    piece = board.piece_at(chess.parse_square(moveTo))

                    # this calculate the probabilities of the new moves
                    weights = []
                    if ((numBetterMoves := len(list(board.legal_moves))) > 0):
                        info = engine.analyse(board, chess.engine.Limit(time=0.1, depth=10), multipv=numBetterMoves)
                        for j in info:
                            score = (j['score'])
                            if ((num := int(str(score.black()))) > 0):
                                weights.append(num)
                        denom = sum(weights)
                        probabilities = [(val/denom) for val in weights]
                    else:
                        probabilities=[0]
                    # print("Weights ", weights)
                    # print("Probabilities", probabilities)
                    # print("Board Push")
                    board.push(move)
                    #round two

                    weights = []
                    if ((newNumBetterMoves := len(list(board.legal_moves))) > 0):
                        info = engine.analyse(board, chess.engine.Limit(time=0.1, depth=10), multipv=newNumBetterMoves)
                        for k in info:
                            score = (k['score'])
                            if ((num := int(str(score.white()))) > 0):
                                weights.append(num)
                        denom = sum(weights)
                        newProbabilities = list([val/denom for val in weights])
                    else:
                        newProbabilities=[0]
                    # print("Weights ", weights)
                    # print("Probabilities", newProbabilities)
                    # print("Board Push")
                    entropy = shannonEntropy(probabilities)
                    conEntropy = conditionalEntropy(probabilities, newProbabilities)
                    jEntropy = jointEntropy(probabilities, newProbabilities)
                    dataFile.write(f"Player: Black Move Number: {moveNum} Move: {move} Piece: {piece} Number of Better Moves: {numBetterMoves} Entropy: {entropy} Conditional Entropy: {conEntropy} Joint Entropy: {jEntropy}\n")
                    totalMoves.append(moveNum)
                    totalShannonEntropies.append(shannonEntropy(probabilities))
                    totalConditionalEntropies.append(conEntropy)
                    totalJointEntropy.append(jEntropy)
                else:
                    #This only does the calculations if it is the white players move
                    moveTo = (str(move)[2::])
                    if len(moveTo) == 3:
                        moveTo = moveTo[:-1]
                    piece = board.piece_at(chess.parse_square(moveTo))

                    # this calculate the probabilities of the new moves
                    weights = []
                    if ((numBetterMoves := len(list(board.legal_moves))) > 0):
                        info = engine.analyse(board, chess.engine.Limit(time=0.1, depth=10), multipv=numBetterMoves)
                        for j in info:
                            score = (j['score'])
                            if ((num := int(str(score.white()))) > 0):
                                weights.append(num)
                        denom = sum(weights)
                        probabilities = [(val/denom) for val in weights]
                    else:
                        probabilities=[0]
                    # print("Weights ", weights)
                    # print("Probabilities", probabilities)
                    # print("Board Push")
                    board.push(move)
                    #round two

                    weights = []
                    if ((newNumBetterMoves := len(list(board.legal_moves))) > 0):
                        info = engine.analyse(board, chess.engine.Limit(time=0.1, depth=10), multipv=newNumBetterMoves)
                        for k in info:
                            score = (k['score'])
                            if ((num := int(str(score.black()))) > 0):
                                weights.append(num)
                        denom = sum(weights)
                        newProbabilities = list([val/denom for val in weights])
                    else:
                        newProbabilities=[0]
                    # print("Weights ", weights)
                    # print("Probabilities", newProbabilities)
                    # print("Board Push")
                    entropy = shannonEntropy(probabilities)
                    conEntropy = conditionalEntropy(probabilities, newProbabilities)
                    jEntropy = jointEntropy(probabilities, newProbabilities)
                    dataFile.write(f"Player: White Move Number: {moveNum} Move: {move} Piece: {piece} Number of Better Moves: {numBetterMoves} Entropy: {entropy} Conditional Entropy: {conEntropy} Joint Entropy: {jEntropy}\n")
                    totalMoves.append(whiteMove)
                    totalShannonEntropies.append(shannonEntropy(probabilities))
                    totalConditionalEntropies.append(conEntropy)
                    totalJointEntropy.append(jEntropy)
            #updates the data with the data filename:[stats, stats, stats]
            data.update({baseName[i-1]: [totalMoves, totalShannonEntropies, totalConditionalEntropies, totalJointEntropy]})
            #data.update({baseName[0] : [totalMoves, totalShannonEntropies]})
            #data.update({baseName[0] : [totalMoves, totalShannonEntropies, totalConditionalEntropies]})
            #empties the lists so we can fill and repeat with the next pgn file
            totalMoves = []
            totalShannonEntropies = []
            totalConditionalEntropies = []
            totalJointEntropy = []
    engine.quit()
    dataFile.close()
    plotShannonEntropy(data, dt_string)
    plotBestFitShannonEntropy(data, dt_string)
    plotConditionalEntropy(data, dt_string)
    plotBestFitConditionalEntropy(data, dt_string)
    plotJointEntropy(data, dt_string)
    plotBestJointEntropy(data, dt_string)
    exit()
    

def conditionalEntropy(probabilities, newProbabilities):
    conditionalEntropy = -1 * sum(conditionalEntropy := [pX*pY * (log2(pX)/(pX*pY)) for pX in probabilities for pY in probabilities if pY != 0 and pX != 0])
    return conditionalEntropy
    
def shannonEntropy(probabilities):
    entropy = -1 * sum(entropies := [((prob)*log2(prob)) for prob in probabilities if prob != 0])
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

    
def jointEntropy(probabilities, newProbabilities):
    jointEntropy = -1 * sum((pX * pY * log2(pX*pY)) for pX in probabilities for pY in newProbabilities if pX !=0 and pY != 0)
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
    print("Slope: ", m)
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

    
if __name__ == "__main__":
    main()

