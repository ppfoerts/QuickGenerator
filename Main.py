#!/usr/bin/python
#Python project to quickly generate a D&D character

import random
import sys

#quick generator requirements,
#name, class, stats, race, alignment
#Dice Roller
#N for # of Dice and S for # of sides
def rollDice(N, S):
    result = 0
    for i in range(0,N):
        result += 1 + random.randrange(S)
     
    return result
 

def statGen(method):  
    stats = [0,0,0,0,0,0]
    #different methods to generate
    #3d6
    if(method == "3d6"):
        for i in range(0,6):
            stats[i] = rollDice(3,6)
    #4d6
    elif(method == "4d6"):
        stats[1] = 1
    #pregen
    elif(method == "pregen"):
        stats[2] = 1
      
    return stats
    

def nameGen():
    name = ""
    return name
    
def classGen():
    clas = "" #refer to class as class for code sake
    return clas
    
def raceGen():
    race = ""
    return race
    
def alignmentGen():
    alignment = ""
    return alignment;
    
if __name__ == "__main__":
    #check for arguments
    if(len(sys.argv) != 2):
        print("Format of argument is python "+sys.argv[0]+" statGenMethod")
    else:
        #1st generates stats
        print(statGen(sys.argv[1]))
        #2nd then choose class
    