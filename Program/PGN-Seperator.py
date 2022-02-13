import os, sys

def main():
    baseName = sys.argv[1][0:-4]
    count = 0
    numFiles = 0
    gameWriter = []
    with open(sys.argv[1], 'r') as masterFile:
        lines = masterFile.readlines()
        for index, line in enumerate(lines):
            gameWriter.append(line)
            if line == "\n":
                count += 1
            if count == 2:
                numFiles += 1
                newGameFile = open(f"{baseName}-game{numFiles}.pgn", 'w')
                print(f"{baseName}-game{numFiles}.pgn")
                for line in gameWriter:
                    newGameFile.writelines(line)
                newGameFile.close()
                gameWriter.clear()
                count = 0
main()
        
