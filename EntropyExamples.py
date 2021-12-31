import sys, os
import numpy as np
import math
import random

coinProb = 1/2 #probability for heads
coinDist = 1/4 #second probability set
log2 = lambda x: math.log(x, 2)

def main():
    #Standard Shannon Entropy
    print(f"So shannon entropy is the negative of the probability of a thing times the log base two of that probability for each outcome so for a coin it would be:\n-({coinProb} * {log2(coinProb)} + {1-coinProb} * {log2(1-coinProb)}) which is {shannonEntropy()} bit of information. This makes sense because a bit has either heads or tails")
    kld(coinDist) #This stands for Kullback-Liebler Divergance
    print(f"\nSo kullback liebler divergance tells us the difference between to sets or distributions of probabilities. It is the sum of all the probabilites times the log base 2 of a probability divided by the other one in a set. So lets say we have a real shitty coin that is heads halfa fourth of the time so we have \n{coinProb} * {log2(coinProb / coinDist)} + {1-coinProb} * {log2((1-coinProb) / (1 - coinDist))} which is {kld(coinDist)} bit of information. This makes sense because both probability distributions are very close")
    
def randDist():
    randDistribution = random.random() #random probability for heads
    return randDistribution
        
def kld(cD):
    kldBits = coinProb*(log2(coinProb/cD)) + coinProb*(log2(coinProb/(1-cD))) 
    return(kldBits)
    
def shannonEntropy():
    shannonEntropy = -(coinProb * log2(coinProb) + ((1- coinProb) * log2(1 - coinProb)))
    return shannonEntropy

main()
