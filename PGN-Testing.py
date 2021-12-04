#!/usr/bin/env python3
import sys, os
import numpy

def main():
    with open(sys.argv[1], "r") as f:
        print(f.read())
    print("That's all folks")


if __name__ == "__main__":
    main()
