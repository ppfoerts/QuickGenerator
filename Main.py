#!/usr/bin/python
#Python project to quickly generate a D&D character

import random
import sys
import heapq
import os

#quick generator requirements,
#name, class, stats, race, alignment
#Dice Roller
#N for # of Dice and S for # of sides
def rollDice(N, S):
    result = 0
    for i in range(0,N):
        result += 1 + random.randrange(S)
     
    return result
 
def calcBonus(stat):
    bonus = 0
    bonus = round((stat - 10)/2);
    return bonus
  
#random generator functions  
def statGen(method):  
    stats = [0,0,0,0,0,0]
    #different methods to generate
    #3d6
    if(method == "3d6"):
        for i in range(0,6):
            stats[i] = rollDice(3,6)
    #4d6
    elif(method == "4d6"):
        for i in range(0,6):
            values = [0,0,0,0]
            for y in range(0,4):
                values[y] = rollDice(1,6)
                
            values.remove(min(values))
            stats[i] = sum(values)
    #pregen
    elif(method == "pregen"):
        values = [15,14,13,12,10,8]
        for i in range(0,6):
            rand = random.randrange(len(values))
            stats[i] = values[rand]
            values.remove(values[rand])
      
    return stats
    
def nameGen(race,gender):
    script_dir = os.path.dirname(__file__)
    name = ""
    fileName = "names/"
    first = ""
    last = ""
    
    if("Dwarf" in race):
        fileName += "Dwarf"        
    elif("Half-Elf" in race):
        fileName += "Half-Elf"
    elif("Elf" in race):
        fileName += "Elf"
    elif("Halfling" in race):
        fileName += "Halfling"
    elif("Human" in race):
        fileName += "Human"
    elif("Dragonborn" in race):
        fileName += "Dragonborn"
    elif("Gnome" in race):
        fileName += "Gnome"
    elif("Half-orc" in race):
        fileName += "Half-orc"
    elif("Tiefling" in race):
        fileName += "Tiefling"
        
    fileNameLast = fileName+"last"+".txt"
    absPath = os.path.join(script_dir, fileNameLast)
    nameFile = open(absPath,'r')
    names =  nameFile.read().split(',')
    last = random.choice(names).strip()
        
    if(gender == "Male"):
        fileName += "M"
    elif(gender == "Female"):
        fileName += "F"
        
    fileNameFirst = fileName + ".txt"
    absPath = os.path.join(script_dir, fileNameFirst)
    nameFile = open(absPath,'r')
    names =  nameFile.read().split(',')
    first = random.choice(names).strip()
        
    
        
    name = first + " " + last
    
    return name
    
def classGen(stats):
    clas = "" #refer to class as class for code sake
    #str,dex,con,int,wis,cha
    #first find 3 highest values
    bestStats = heapq.nlargest(3,enumerate(stats), key=lambda x:x[1])
    
    firstStat = bestStats[0][0]
    secStat = bestStats[1][0]
    #check if any of the stats is con, the non determiner, and move if it is
    if(firstStat == 2):
        firstStat = bestStats[1][0]
        secStat = bestStats[2][0]     
    if(secStat == 2):
        secStat = bestStats[2][0]
        
    #first try if fit 2 stats classes: Monk, Paladin, Ranger    
    #first try out ranger and monk (Dex & Wis)
    if((firstStat == 1 and secStat == 4) or (firstStat == 4 and secStat == 4)):
        #then randomly assign one of them 
        clas = random.choice(["Ranger","Monk"])
    #then paladin
    elif ((firstStat == 0 and secStat == 5) or (firstStat == 5 and secStat == 0)):
        clas = "Paladin"
    #then Barbarian or fighter
    elif(firstStat == 0):
        clas = random.choice(["Barbarian","Fighter"])
    #then Rogue
    elif(firstStat == 1):
        clas = "Rogue"
    #then wizard
    elif(firstStat == 3):
        clas = "Wizard"
    #then cleric or druid
    elif(firstStat == 4):
        clas = random.choice(["Cleric","Druid"])
    #then bard,sorceror, or warlock
    elif(firstStat == 5):
        clas = random.choice(["Bard","Sorceror","Warlock"])
    else:
        clas = "Peasant"
    #then 1 stat classes
    return clas
    
def raceGen(clas):
    race = ""
    #create list of good choices for class then randomly choose from them
    choices = ["Human"] #human is a good choice for every class
    if(clas == "Barbarian" or clas == "Figher" or clas == "Paladin"):
        choices.append("Mountain Dwarf")
        choices.append("Half-orc")
        choices.append("Dragonborn")
    elif(clas == "Monk" or clas == "Ranger" or clas == "Rogue"):
        choices.append("High Elf")
        choices.append("Wood Elf")
        choices.append("Stout Halfling")
        choices.append("Lightfoot Halfling")
        choices.append("Forest Gnome")
    elif(clas == "Wizard"):
        choices.append("High Elf")
        choices.append("Tiefling")
        choices.append("Forest Gnome")
        choices.append("Rock Gnome")
    elif(clas == "Cleric" or clas == "Druid"):
        choices.append("Wood Elf")
        choices.append("Hill Dwarf")    
    elif(clas == "Bard" or clas == "Sorceror" or clas == "Warlock"):
        choices.append("Half-Elf")
        choices.append("Tiefling")
        choices.append("Drow")
        choices.append("Dragonborn")
        choices.append("Lightfoot Halfling")
        
    race = random.choice(choices)
    return race
    
def raceStatChanges(stats,race):
    nStats = stats
    if(race == "Dragonborn"):
        nStats[0] = nStats[0] + 2
        nStats[5] = nStats[5] + 1
    elif(race == "Hill Dwarf"):
        nStats[2] = nStats[2] + 2
        nStats[4] = nStats[4] + 1
    elif(race == "Mountain Dwarf"):
        nStats[0] = nStats[0] + 2
        nStats[2] = nStats[2] + 2
    elif(race == "Drow"):
        nStats[1] = nStats[1] + 2
        nStats[5] = nStats[5] + 1
    elif(race == "High Elf"):
        nStats[1] = nStats[1] + 2
        nStats[3] = nStats[3] + 1
    elif(race == "Wood Elf"):
        nStats[1] = nStats[1] + 2
        nStats[4] = nStats[4] + 1
    elif(race == "Forest Gnome"):
        nStats[3] = nStats[3] + 2
        nStats[1] = nStats[1] + 1
    elif(race == "Rock Gnome"):
        nStats[3] = nStats[3] + 2
        nStats[2] = nStats[2] + 1
    elif(race == "Lightfoot Halfling"):
        nStats[1] = nStats[1] + 2
        nStats[5] = nStats[5] + 1
    elif(race == "Stout Halfling"):
        nStats[1] = nStats[1] + 2
        nStats[2] = nStats[2] + 1
    elif(race == "Half Elf"):
        nStats[5] = nStats[5] + 2
        randomStats = random.sample(range(0,5),2)
        nStats[randomStats[0]] = nStats[randomStats[0]] + 1
        nStats[randomStats[1]] = nStats[randomStats[1]] + 1
    elif(race == "Half Orc"):
        nStats[0] = nStats[0] + 2
        nStats[2] = nStats[2] + 1
    elif(race == "Human"):
        [x+1 for x in nStats]
    elif(race == "Tiefling"):
        nStats[5] = nStats[5] + 2
        nStats[3] = nStats[3] + 1
        
    return nStats
    
def alignmentGen():
    alignment = random.choice(["LG","LN","LE","NG","N","NE","CG","CN","CE"])
    return alignment;
  
def backgroundGen():
    return random.choice(["Acolyte","Charlatan","Criminal","Entertainer","Folk Hero","Guild Artisan","Hermit","Noble","Outlander","Sage","Sailor","Soldier","Urchin"])

#calculators
def hpCalc(clas,con):
    d12 = {'Barbarian'}
    d10 = {"Fighter","Paladin","Ranger"}
    d8 = {"Bard","Cleric","Druid","Monk","Rogue","Warlock"}
    d6 = {"Sorceror","Wizard"}
    hp = 0
    if(clas in d12 ):
        hp = 12 + calcBonus(con)
    elif(clas in d10):
        hp = 10 + calcBonus(con)  
    elif(clas in d8):
        hp = 8 + calcBonus(con)
    elif(clas in d6):
        hp = 6 + calcBonus(con)
        
    return hp

def savingThrowCalc(stats,clas,profBonus):
    saves = [0,0,0,0,0,0]
    #can't think of way to do this efficiently right now, I'll do it manually for now
    #str
    for i in range(0,6):
        saves[i] = calcBonus(stats[i])
    
    #fighter and paladin
    #strength and constitution
    if(clas in {"Fighter","Paladin"}):
        saves[0] += profBonus
        saves[2] += profBonus
    #Monk and Ranger
    #Strength & Dexterity
    elif(clas in {"Monk","Ranger"}):
        saves[0] += profBonus
        saves[1] += profBonus
    #Cleric,Paladin, & Warlock
    #Wisdom and Charisma
    elif(clas in {"Cleric","Paladin","Warlock"}):
        saves[4] += profBonus
        saves[5] += profBonus
    #Druid and Wizard
    #Int and Wis 
    elif(clas in {"Druid","Wizard"}):
        saves[3] += profBonus
        saves[4] += profBonus
    #Bard
    #Dex and Cha
    elif(clas in {"Bard"}):
        saves[1] += profBonus
        saves[5] += profBonus
    #Rogue
    #Dex and Int
    elif(clas in {"Rogue"}):
        saves[1] += profBonus
        saves[3] += profBonus
    #Sorceror
    #Con and Cha
    elif(clas in {"Sorceror"}):
        saves[2] += profBonus
        saves[5] += profBonus

    return saves  

def profCalc(clas,background):
    proficiencies = ""
    with open("proficiencies.txt") as f:
        for line in f:
            if clas in line:
                proficiencies += line
    return proficiencies

def langCalc(race,background):
    lang = ["Common"]
    
    
    return lang
    
if __name__ == "__main__":
    #check for arguments
    if(len(sys.argv) != 2):
        print("Format of argument is python "+sys.argv[0]+" statGenMethod")
    else:
        #1st generates stats
        stats = statGen(sys.argv[1])
        #2nd then choose class
        print("Class:")
        clas = classGen(stats)
        print(clas)
        #3rd choose race
        print("Race:")
        race = raceGen(clas)
        print(race)
        #show modded stats with racials
        stats = raceStatChanges(stats,race)
        print("Stats: (Str,Dex,Con,Int,Wis,Cha)")
        print(stats)
        #4th alignment
        print("Alignment:")
        print(alignmentGen())
        #5th background
        print("Background: ")
        background = backgroundGen()
        print(background)
        #6th gender
        print("Gender: ")
        gender = random.choice(["Male","Female"])
        print(gender)
        #7th name
        name = nameGen(race,gender);
        print("Name: ")
        print(name)
        
        #HP and Hit Dice
        print("HP: ")
        print(hpCalc(clas,stats[2]))
        #Proficiency bonus
        profBonus = 2
        print("Proficiency Bonus: ")
        print(profBonus)
        #saving throws
        print("Saving Throws: ")
        print(savingThrowCalc(stats,clas,profBonus))
        #proficiencies
        print("Proficiences: ")
        print(profCalc(clas,background))
        #languages
        #skills
        
        #equipment
        #Armor Class and Speed
        #spells
        #other
        
        
        
        
        