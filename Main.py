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
    elif("Elf" in race or "Drow" in race):
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
                proficiencies += "\n"
            elif background in line:
                proficiences += line
                proficiencies += "\n"

    return proficiencies

def langCalc(race,background):
    languages = ["Elvish","Dwarvish","Orc","Gnomish","Giant","Goblin","Halfling"]
    known = ["Common"]
    if("Elf" in race or "Drow" in race):
        known.append("Elvish")
        languages.remove("Elvish")
    elif("Dwarf" in race):
        known.append("Dwarvish")
        languages.remove("Dwarvish")
    elif("orc" in race):
        known.append("Orc")
        languages.remove("Orc")
    elif("Gnome" in race):
        known.append("Gnomish")
        languages.remove("Gnomish")
    elif("Halfling" in race):
        known.append("Halfling")
        languages.remove("Halfling")
    elif("Tiefling" in race):
        known.append("Infernal")
    elif("Dragonborn" in race):
        known.append("Draconic")
        
    if("Human" in race or "Half-Elf" in race):
        choice = random.choice(languages)
        known.append(choice)
        languages.remove(choice)
        
    #background languages
    random.shuffle(languages)
    if(background is "Guild Artisan" or background is "Hermit" or background is "Noble" or background is "Outlander"):
         known.append(languages.pop())
    elif(background is "Acolyte" or background is "Sage"):
        #add two languages
        known.append(languages.pop())
        known.append(languages.pop())
    
    return known
#list of what my skill proficiences are
def skillProfCalc(clas,background):
    profs = []
    if(clas is "Barbarian"):
        skills = ["Animal Handling","Athletics","Intimidation","Nature","Perception","Survival"]
    elif(clas is "Bard"):
        skills = ["Acrobatics","Animal Handling","Arcana","Athletics","Deception","History","Insight","Intimidation","Investigation","Medicine","Nature","Perception","Performance","Persuasion","Religion","Sleight of Hand", "Stealth","Survival"]
    elif(clas is "Cleric"):
        skills = ["History","Insight","Medicine","Persuasion","Religion"]
    elif(clas is "Druid"):
        skills = ["Arcana","Animal Handling","Insight","Medicine","Nature","Perception","Religion","Survival"]
    elif(clas is "Fighter"):
        skills = ["Acrobatics","Animal Handling","Athletics","History","Insight","Intimidation","Perception","Survival"]
    elif(clas is "Monk"):
        skills = ["Acrobatics","Athletics","History","Insight","Insight","Religion","Stealth"]
    elif(clas is "Paladin"):
        skills = ["Athletics","Insight","Intimidation","Medicine","Persuasion","Religion"]
    elif(clas is "Ranger"):
        skills = ["Animal Handling","Athletics","Insight","Investigation","Nature","Perception","Stealth","Survival"]
    elif(clas is "Rogue"):
        skills = ["Acrobatics", "Athletics","Deception","Insight","Intimidation","Investigation","Perception","Performance","Persuasion","Sleight of Hand","Stealth"]
    elif(clas is "Sorceror"):
        skills = ["Arcana","Deception","Insight","Intimidation","Persuasion","Religion"]
    elif(clas is "Warlock"):   
        skills = ["Arcana","Deception","History","Investigation","Intimidation","Nature","Religion"]
    elif(clas is "Wizard"):
        skills = ["Arcana","History","Insight","Investigation","Medicine","Religion"]
    
    #background skills here
    #add skills profs and then remove from random list
    if(background is "Acolyte"):
        profs.append("Insight")
        profs.append("Religon")
        skills = list(filter(("Insight").__ne__, skills))
        skills = list(filter(("Religion").__ne__, skills))
    elif(background is "Charlatan"):
        profs.append("Deception")
        profs.append("Sleight of Hand")
        skills = list(filter(("Deception").__ne__, skills))
        skills = list(filter(("Sleight of Hand").__ne__, skills))
    elif(background is "Criminal"):
        profs.append("Deception")
        profs.append("Stealth")
        skills = list(filter(("Deception").__ne__, skills))
        skills = list(filter(("Stealth").__ne__, skills))
    elif(background is "Entertainer"):
        profs.append("Acrobatics")
        profs.append("Performance")
        skills = list(filter(("Acrobatics").__ne__, skills))
        skills = list(filter(("Performance").__ne__, skills))
    elif(background is "Folk Hero"):
        profs.append("Animal Handling")
        profs.append("Survival")
        skills = list(filter(("Animal Handling").__ne__, skills))
        skills = list(filter(("Survival").__ne__, skills))
    elif(background is "Guild Artisan"):
        profs.append("Insight")
        profs.append("Persuasion")
        skills = list(filter(("Insight").__ne__, skills))
        skills = list(filter(("Persusasion").__ne__, skills))
    elif(background is "Hermit"):
        profs.append("Medicine")
        profs.append("Religion")
        skills = list(filter(("Medicine").__ne__, skills))
        skills = list(filter(("Religion").__ne__, skills))
    elif(background is "Noble"):
        profs.append("History")
        profs.append("Persuasion")
        skills = list(filter(("History").__ne__, skills))
        skills = list(filter(("Persusasion").__ne__, skills))
    elif(background is "Outlander"):
        profs.append("Athletics")
        profs.append("Survival")
        skills = list(filter(("Athletics").__ne__, skills))
        skills = list(filter(("Survival").__ne__, skills))
    elif(background is "Sage"):
        profs.append("History")
        profs.append("Arcana")
        skills = list(filter(("History").__ne__, skills))
        skills = list(filter(("Arcana").__ne__, skills))
    elif(background is "Sailor"):
        profs.append("Athletics")
        profs.append("Perception")
        skills = list(filter(("Athletics").__ne__, skills))
        skills = list(filter(("Perception").__ne__, skills))
    elif(background is "Soldier"):
        profs.append("Athletics")
        profs.append("Intimidation")
        skills = list(filter(("Athletics").__ne__, skills))
        skills = list(filter(("Intimidation").__ne__, skills))
    elif(background is "Urchin"):
        profs.append("Sleight of Hand")
        profs.append("Stealth")
        skills = list(filter(("Sleight of Hand").__ne__, skills))
        skills = list(filter(("Stealth").__ne__, skills))
        
    random.shuffle(skills)
    profs.append(skills.pop())
    profs.append(skills.pop())
    if(clas is "Ranger" or clas is "Bard" or clas is "Rogue"):
        profs.append(skills.pop())
        if(clas is "Rogue"):
            profs.append(skills.pop())
     
        
    return profs

def skillNum(skillProfs):
    skillProfsNum = []
    for skill in skillProfs:
        if(skill is "Acrobatics"):
            skillProfsNum.append(0)
        elif(skill is "Animal Handling"):
            skillProfsNum.append(1)
        elif(skill is "Arcana"):
            skillProfsNum.append(2)
        elif(skill is "Athletics"):
            skillProfsNum.append(3)
        elif(skill is "Deception"):
            skillProfsNum.append(4)
        elif(skill is "History"):
            skillProfsNum.append(5)
        elif(skill is "Insight"):
            skillProfsNum.append(6)
        elif(skill is "Intimidation"):
            skillProfsNum.append(7)
        elif(skill is "Investigation"):
            skillProfsNum.append(8)
        elif(skill is "Medicine"):
            skillProfsNum.append(9)
        elif(skill is "Nature"):
            skillProfsNum.append(10)
        elif(skill is "Perception"):
            skillProfsNum.append(11)
        elif(skill is "Performance"):
            skillProfsNum.append(12)
        elif(skill is "Persuasion"):
            skillProfsNum.append(13)
        elif(skill is "Religion"):
            skillProfsNum.append(14)
        elif(skill is "Sleight of Hand"):
            skillProfsNum.append(15)
        elif(skill is "Stealth"):
            skillProfsNum.append(16)
        elif(skill is "Survival"):
            skillProfsNum.append(17)
    return skillProfsNum
    
def skillCalc(stats,profBonus,skillProfsNum):
    skills = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #Acrobatics (Dex)
    skills[0] = calcBonus(stats[1])
    #Animal Handling (Wis)
    skills[1] = calcBonus(stats[4])
    #Arcana (Int)
    skills[2] = calcBonus(stats[3])
    #Athletics (Str)
    skills[3] = calcBonus(stats[0])
    #Deception (Cha)
    skills[4] = calcBonus(stats[5])
    #History (Int)
    skills[5] = calcBonus(stats[3])
    #Insight (Wis)
    skills[6] = calcBonus(stats[4])
    #Intimidation (Cha)
    skills[7] = calcBonus(stats[5])
    #Investigation (Int)
    skills[8] = calcBonus(stats[3])
    #Medicine (Wis)
    skills[9] = calcBonus(stats[4])
    #Nature (Int)
    skills[10] = calcBonus(stats[3])
    #Perception (Wis)
    skills[11] = calcBonus(stats[4])
    #Performance (Cha)
    skills[12] = calcBonus(stats[5])
    #Persuasion (Cha)
    skills[13] = calcBonus(stats[5])
    #Religion (Int)
    skills[14] = calcBonus(stats[3])
    #Sleight of Hand (Dex)
    skills[15] = calcBonus(stats[1])
    #Stealth (Dex)
    skills[16] = calcBonus(stats[1])
    #Survival (Wis)
    skills[17] = calcBonus(stats[4])
    
    for skillProf in skillProfsNum:
        skills[skillProf] += profBonus
        
    return skills

def equipCalc(clas,background):
    script_dir = os.path.dirname(__file__)
    with open('equipment/martialWeapons.txt') as f:
        martialWeapons = f.read().splitlines()
    with open('equipment/martialMeleeWeapons.txt') as f:
        martialMWeapons = f.read().splitlines()
    with open('equipment/simpleWeapons.txt') as f:
        simpleWeapons = f.read().splitlines()
    with open('equipment/simpleMeleeWeapons.txt') as f:
        simpleMeleeWeapons = f.read().splitlines()
    equipment = []
    if(clas is "Barbarian"):
        equipment.append(random.choice(martialMWeapons))
        equipment.append(random.choice(simpleWeapons))
        equipment.append("Explorer's Pack")
        equipment.append("4 Javelins")
    elif(clas is "Bard"):
        simpleWeapons.extend(("Rapier","Longsword"))
        equipment.append(random.choice(simpleWeapons))
        equipment.append(random.choice(["Diplomat's Pack","Entertainer's Pack"]))
        equipment.append(random.choice(["Bagpipes","Drum","Dulcimer","Flute","Lute","Lyre","Horn","Pan flute","Shawm","Viol"]))
        equipment.append("leather armor")
        equipment.append("Dagger")
    elif(clas is "Cleric"):
        equipment.append("Mace")
        equipment.append(random.choice(["scale mail","leather armor"]))
        simpleWeapons.append("light crossbow and 20 bolts")
        equipment.append(random.choice(simpleWeapons))
        equipment.append(random.choice(["Priest's Pack","Explorer's Pack"]))
        equipment.append("Shield")
        equipment.append("Holy Symbol")
    elif(clas is "Druid"):
        simpleWeapons.append("wooden shield")
        equipment.append(random.choice(simpleWeapons))
        simpleMeleeWeapons.append("scimitar")
        equipment.append(random.choice(simpleMeleeWeapons))
        equipment.append("Leather armor")
        equipment.append("Exporer's Pack")
        equipment.append("Druidic Focus")
    elif(clas is "Fighter"):
        equipment.append(random.choice(["chain mail","leather armor, longbow and 20 arrows"]))
        equipment.append(random.choice(martialWeapons))
        martialWeapons.append("shield")
        equipment.append(random.choice(martialWeapons))
        equipment.append(random.choice(["light crossbow and 20 bolts","2 Handaxes"]))
        equipment.append(random.choice(["Dungeoneers's Pack","Explorer's Pack"]))
    elif(clas is "Monk"):
        simpleWeapons.append("shortsword")
        equipment.append(random.choice(simpleWeapons))
        equipment.append(random.choice(["Dungeoneers's Pack","Explorer's Pack"]))
        equipment.append("10 darts")
    elif(clas is "Paladin"):
        equipment.append(random.choice(martialWeapons))
        martialWeapons.append("shield")
        equipment.append(random.choice(martialWeapons))
        simpleWeapons.append("5 Javelins")
        equipment.append(random.choice(simpleWeapons))
        equipment.append(random.choice(["Priest's Pack","Explorer's Pack"]))
    elif(clas is "Ranger"):
        equipment.append(["scale mail","leather armor"])
        equipment.append(random.choice(["2 shortswords",[random.choice(simpleMeleeWeapons),random.choice(simpleMeleeWeapons)]]))
        equipment.append(random.choice(["Dungeoneers's Pack","Explorer's Pack"]))
        equipment.append("Longbow and quiver with 20 arrows")
    elif(clas is "Rogue"):
        equipment.append(random.choice(["rapier","shortsword"]))
        equipment.append(random.choice(["Longbow and quiver with 20 arrows","shortsword"]))
        equipment.append(random.choice(["Burglar's Pack","Dungeoneers's Pack","Explorer's Pack"]))
        equipment.append("2 Daggers")
        equipment.append("leather armor")
        equipment.append("thieve's tools")
    elif(clas is "Sorceror"):
        simpleWeapons.append("light crossbow and 20 bolts")
        equipment.append(random.choice(simpleWeapons))
        equipment.append(random.choice(["Component Pouch","Arcane Focus"]))
        equipment.append(random.choice(["Dungeoneers's Pack","Explorer's Pack"]))
        equipment.append("2 Daggers")
    elif(clas is "Warlock"):   
        equipment.append(random.choice(simpleWeapons))
        simpleWeapons.append("light crossbow and 20 bolts")
        equipment.append(random.choice(simpleWeapons))
        equipment.append(random.choice(["Component Pouch","Arcane Focus"]))
        equipment.append(random.choice(["Dungeoneers's Pack","Scholar's Pack"]))
        equipment.append("2 Daggers")
        equipment.append("leather armor")
    elif(clas is "Wizard"):
        equipment.append(random.choice(["quarterstaff","dagger"]))
        equipment.append(random.choice(["Component Pouch","Arcane Focus"]))
        equipment.append(random.choice(["Explorer's Pack","Scholar's Pack"]))
        equipment.append("spellbook")
    
    artisanTools = ["Alchemist’s supplies","Brewer’s supplies","Calligrapher's supplies","Carpenter’s tools","Cartographer’s tools","Cobbler’s tools","Cook’s utensils","Glassblower’s tools","Jeweler’s tools","Leatherworker’s tools","Mason’s tools","Painter’s supplies","Potter’s tools","Smith’s tools","Tinker’s tools","Weaver’s tools","Woodcarver's tools"]
    #check background for stuff
    if(background is "Acolyte"):
        equipment.extend(("Holy Symbol","5 Sticks of incense","vestments","Set of Common Clothes","15 gp"))
        equipment.append(random.choice(["Prayer Book","Prayer Wheel"]))
    elif(background is "Charlatan"):
        equipment.extend(("Set of fine clothes","disguise kit","15gp"))
        equipment.append(random.choice(["Ten stoppered bottles filled with colored liquid","set of weighted dice","deck of market cards","signet ring of imaginary duke"]))
    elif(background is "Criminal"):
        equipment.extend(("crowbar","set of dark common clothes including a hood", "15gp"))
    elif(background is "Entertainer"):
        equipment.append(random.choice["Bagpipes","Drum","Dulcimer","Flute","Lute","Lyre","Horn","Pan flute","Shawm","Viol"])
        equipment.append(random.choice(["love letter","lock of hair","trinket"])
        equipment.extend(("costume","15 gp"))
    elif(background is "Folk Hero"):
        equipment.extend(("shovel","iron pot","set of common clothes","10 gp"))
        equipment.append(random.choice(artisanTools))
    elif(background is "Guild Artisan"):
        equipment.append(random.choice(artisanTools))
        equipment.extend(("letter of introduction from your guild","set of traveller's clothes","15gp"))
    elif(background is "Hermit"):
        equipment.extend(("A scroll case stuffed full of notes from your studies or prayers","winter blanket","set of common clothes","herbalism kit","5 gp"))
    elif(background is "Noble"):
        equipment.extend(("set of fine clothes","signet ring","scroll of pedigree","25 gp"))
    elif(background is "Outlander"):
        equipment.extend(("staff","hunting trap","trophy from animal you killed","set of traveller's clothes","10 gp"))
    elif(background is "Sage"):
        equipment.extend(("bottle of black ink","quill","small knife","letter from dead colleague posing a question you have not yet been able to answer","set of common clothes","10 gp"))
    elif(background is "Sailor"):
        equipment.extend(("A belaying pin","50 ft of silk rope","lucky charm","set of common clothes","10 gp"))
    elif(background is "Soldier"):
        equipment.extend(("insignia of rank","trophy from fallen enemy","set of common clothes","10 gp"))
        equipment.append(random.choice(["bone dice","deck of cards"]))
    elif(background is "Urchin"):
        equipment.extend(("small knife","map of the city you grew up in","pet mouse","token to remember parents by","set of common clothes","10 gp"))
    
    return equipment

def acspdCalc(race,equipment,stats):
    ac = 10
    spd = 30
    dex = calcBonus(stats[1])
    str = calcBonus(stats[0])
  
    if("Halfling" in race or "Gnome" in race):
        spd = 25
        
    #leather
    if("leather armor" in equipment):
        ac = 11 + dex
    #scale mail
    elif("scale mail" in equipment):
        if(dex >= 2):
            ac = 14 + 2
        else:
            ac = 14 + dex
    #chain mail
    elif("chain mail" in equipment):
        ac = 16
        #if str less than the required, reduce spd by 10
        if(str >= 13):
            spd = spd - 10
    #dwarves ignore heavy armor strength penalty        
    if("Dwarf" in race):
        spd = 25
        
    return ac,spd
    
def spellsCalc(clas):
    spells = []
    cantrips = []
    lvl1 = []
    if(clas is "Barbarian"):
        print()
    elif(clas is "Bard"):
        cantrips = ["dancing lights","vicious mockery"]
        lvl1 = ["charm person","detect magic","healing word","thunderwave"]
    elif(clas is "Cleric"):
        print()
    elif(clas is "Druid"):
        print()
    elif(clas is "Fighter"):
        print()
    elif(clas is "Monk"):
        print()
    elif(clas is "Paladin"):
        print()
    elif(clas is "Ranger"):
        print()
    elif(clas is "Rogue"):
        print()
    elif(clas is "Sorceror"):
        cantrips = ["light","prestidigation","ray of frost","shocking grasp"]
        lvl1 = ["shield","Magic missile"]
    elif(clas is "Warlock"):   
        cantrips = ["Eldritch Blast", "Chill touch"]
        lvl1 = ["Ray of sickness","witch bolt"]
    elif(clas is "Wizard"):
        cantrips = ["mage hand","light","ray of frost"]
        lvl1 = ["burning hands","charm person","feather fall","mage armor","magic missile","sleep"]
        
    spells.append(cantrips)
    spells.append(lvl1)
    return spells

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
        print("languages: ")
        print(langCalc(race,background))
        #skills
        print("Skills: ")
        print("     Proficiencies: ")
        skillProfs = skillProfCalc(clas,background)
        print(skillProfs)
        print(skillCalc(stats,profBonus,skillNum(skillProfs)))
        #equipment
        print("Equipment:")
        equipment = equipCalc(clas,background)
        print(equipment)
        #Armor Class and Speed
        ac,spd = acspdCalc(race,equipment,stats)
        print("AC: ")
        print(ac)
        print("Speed: ")
        print(spd,"ft")
        #spells
        print("Spell List: ")
        print(spellsCalc(clas))
        #other
        
        
        
        
        