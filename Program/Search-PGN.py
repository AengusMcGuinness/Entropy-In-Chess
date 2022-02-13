#!/usr/bin/env python3
import sys, os
import re
from datetime import datetime

iterableFiles = (1, len(sys.argv))

def main():
    whiteFile = open("White-Winning-Games.txt", 'w')
    blackFile = open("Black-Winning-Games.txt", 'w')
    drawFile = open("Draw-Games.txt", 'w')
    blackSearch = re.compile(r"0-1")
    whiteSearch = re.compile(r"1-1")
    drawSearch = re.compile(r"1/2-1/2")
    for i in iterableFiles:
        with open(sys.argv[i], 'r') as pgn:
            content = pgn.read()
            whiteMatches = len(blackSearch.findall(content))
            blackMatches = len(whiteSearch.findall(content))
            drawMatches = len(drawSearch.findall(content))
            if whiteMatches == 1:
                whiteFile.write(f"{sys.argv[i]}\n")
            if blackMatches == 1:
                blackFile.write(f"{sys.argv[i]}\n")
            if drawMatches == 1:
                drawFile.write(f"{sys.argv[i]}\n")
    whiteFile.close()
    blackFile.close()
    drawFile.close()
                
            
main()
