import json
import os
import os.path
import random
import sys
from pprint import pprint
from msvcrt import getch

VALID_YN = {
    "yes": True,
    "y":   True,
    "ye":  True,
    "no":  False,
    "n":   False
}
PROMPTS_YN = {
    "yes": " [Y/n] ",
    "no":  " [y/N] ",
    None:  " [y/n] "
}
def query_yes_no(question, default="yes"):
    prompt = PROMPTS_YN.get(default)
    if prompt is None:
        raise ValueError("Invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice == '' and default is not None:
            return VALID_YN[default]
        elif choice in VALID_YN:
            return VALID_YN[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' ('y'/'n').\n")

def loadNamesJson(file):
    with open(file, encoding='utf-8') as f:
        return json.load(f)

INITIAL_SCORE = 100 #Initial points for each name.
def translateNamesDictToMap(namesDict):
    namesData = dict()
    for name in namesDict['names']:
        namesData[name] = INITIAL_SCORE
    return namesData

NAMES_JSON = 'names.json'
NAMES_DB = 'db.json'
def loadNamesDict():
    if os.path.isfile(NAMES_DB):
        print('    Loading session...')
        with open(NAMES_DB, encoding='utf-8') as f:
            return json.load(f)
    else:
        print('    Starting session...')
        namesDict = loadNamesJson(NAMES_JSON)
        return translateNamesDictToMap(namesDict)

def saveNamesDict(data):
    print('    Saving session...')
    with open(NAMES_DB, 'w+') as f:
        json.dump(data, f)

def indexDb(nameDb):
    nameIndex = []
    for name, score in nameDb.items():
        for _ in range(score):
            nameIndex.append(name)
    return nameIndex

def randomNames(namesIndex):
    namesIndexC = len(namesIndex)-1
    while True:
        fstNameIndex = random.randint(0, namesIndexC)
        sndNameIndex = random.randint(0, namesIndexC)
        fstName = namesIndex[fstNameIndex]
        sndName = namesIndex[sndNameIndex]
        if(fstName != sndName):
            return [fstName, sndName]

PRECENT_OF_POINTS_TAKEN = 0.25 #How much points will transfer from looser to winner.
def scoreNames(namesDb, winner, looser):
    if namesDb[looser] == 1:
        del namesDb[looser]
        namesDb[winner] = namesDb[winner] + 1
    else:
        scores = max(1, int(namesDb[looser] * PRECENT_OF_POINTS_TAKEN))
        namesDb[looser] = namesDb[looser] - scores
        namesDb[winner] = namesDb[winner] + scores

def printTopTen(namesDb):
    os.system('cls')
    print( "  =============================")
    print('    TOP10 names (with score):')
    print( "  =============================")
    sorted_d = reversed(sorted((value, key) for (key,value) in namesDb.items()))
    for idx, val in enumerate(sorted_d):
        if idx == 10:
            break
        print('      {} - {} ({})'.format(idx, val[1], val[0]))
    print( "  =============================")
    os.system("pause")
	
message = None
os.system('cls')
namesDb = loadNamesDict()
while True:
    namesIndex = indexDb(namesDb)
    namePair = randomNames(namesIndex)
    print( "    ")
    print( "    ======================================")
    print( "    Playing with {} names".format(len(namesDb)))
    print( "    ======================================")
    if message is not None:
        print( "    ### {}".format(message))
        print( "    ======================================")
        message = None
    print( "    ESC   -exit")
    print( "    s     -save")
    print( "    Del   -eliminate left")
    print( "    PgDwn -eliminate right")
    print( "    End   -eliminate both")
    print( "     ↑    -show TOP10")
    print( "     ↓    -draw round")
    print( "    ======================================")
    print( "    Use ← → to choose one You like more.")
    print( "    ----------------------------")
    print( "    {} vs {}".format(namePair[0], namePair[1]))
    print( "    ======================================")
    keycode = ord(getch())
    if keycode in [27, 113]: #ESC, q
        if query_yes_no("    Really wana save and exit?", 'yes'):
            break
    if keycode in [115]: #s
        if query_yes_no("    Shall I save?", 'yes'):
            saveNamesDict(namesDb)
            message = 'Saved...'
    elif keycode == 224: #Special keys (arrows, f keys, ins, del, etc.)
        keycode = ord(getch())
        if keycode == 77: #Right arrow
            scoreNames(namesDb, namePair[1], namePair[0])
        elif keycode == 75: #Left arrow
            scoreNames(namesDb, namePair[0], namePair[1])
        elif keycode == 80: #Down arrow
            message = 'Drawn...'
        elif keycode == 72: #Home
            printTopTen(namesDb)
        elif keycode == 83: #Del
            message = "Eliminated {}".format(namePair[0])
            del namesDb[namePair[0]]
        elif keycode == 79: #End
            message = "Eliminated {} and {}".format(namePair[0], namePair[1])
            del namesDb[namePair[0]]
            del namesDb[namePair[1]]
        elif keycode == 81: #Pgd
            message = "Eliminated {}".format(namePair[1])
            del namesDb[namePair[1]]
        else:
            pprint(keycode)
            os.system('pause')
    else:
        pprint(keycode)
        os.system('pause')
    os.system('cls')
saveNamesDict(namesDb)
