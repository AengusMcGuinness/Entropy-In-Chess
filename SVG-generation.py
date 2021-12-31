#!/usr/bin/env python3
import sys, os
import numpy as np
import chess.pgn
import math
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

numFiles = len(sys.argv)
iterableFiles = range(1, numFiles)
baseName = [sys.argv[i][0:-4] for i in iterableFiles]

def main():
    for i in iterableFiles:
        with open(sys.argv[i]) as pgn:
            game = chess.pgn.read_game(pgn)
            board = game.board()
            for moveNum, move in enumerate(game.mainline_moves()):
                legalMoves = list(board.legal_moves)
                numLegalMoves = len(list(board.legal_moves))
                stateSVG = open(f"{baseName[i-1]}-move{moveNum}gameState.svg", 'w')
                stateSVG.write(chess.svg.board(board, size = 350))
                stateSVG.close()
                board.push(move)

main()
