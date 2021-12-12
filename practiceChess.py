#!/usr/bin/env python3
import chess.pgn
import matplotlib.pyplot as plt

def main():
    chessDistribution = {"p" : 1, "n" : 3, "b" : 3, "r" : 5, "q" : 9}
    pgn = open("wcupSanaElmer.pgn")
    game = chess.pgn.read_game(pgn)
    board = game.board()
    gameMoves = []
    for moveNum, move in enumerate(game.mainline_moves()):
        legalMoves = list(board.legal_moves)
        numLegalMoves = len(list(board.legal_moves))
        gameMoves.append(numLegalMoves)
        #f = open(f"{moveNum}gameState.svg", "x")
        #f.write(chess.svg.board(board, size = 350))
        #f.close()
        board.push(move)
        if moveNum % 2:
            print(f"{moveNum}gameState.svg", numLegalMoves, " Black")
        else:
            print(f"{moveNum}gameState.svg", numLegalMoves, " White")
            
            
main()
