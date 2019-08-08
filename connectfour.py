import numpy as np
import random
import hashlib
import json


## Possible States https://oeis.org/A212693 in the ConnectFour game

## Config
play = False
useOld = True
rows_count = 6
columns_count = 7
terminating_length = 4

ai = 0 ## AI is Player 1
p = 1

## Init Values
e = 0.3
alpha = 0.1
gamma = 1
players = ['O','X']
columns = np.arange(columns_count)
actionQ = {}

# Rewards
rStep = 0
rDraw = -10
rLose = -100
rWin = 100
rInvalid = -2

if play:
    useOld = True ## Use not in Jupyter
    e = 0

## load old ActionQ
if(useOld):
    try:
        actionQ = json.load(open('actionQ.json'))
        print('old ActionQ loaded')
    except IOError:
        print('no old data')


def checkPos(field, pos, player, mv, stw):
    if(stw < 1):
        return True
    if (pos[0] < 0 or pos[0] >= rows_count) or (pos[1] < 0 or pos[1] >= columns_count):
        return False
    if(field[pos[0]][pos[1]] != player):
        return False
    return True and checkPos(field, (pos[0]+mv[0], pos[1]+mv[1]), player, mv, stw - 1)


def winningConditions(field, player):
    for r in range(rows_count):
        for c in range(columns_count):
            if(field[r][c] == player):
                if(checkPos(field, (r, c), player, (1, 0), terminating_length)): # Horizontal
                    #print("H")
                    return True
                if(checkPos(field, (r, c), player, (0, 1), terminating_length)): # Vertical
                    #print("V")
                    return True
                if(checkPos(field, (r, c), player, (-1,1), terminating_length)): # Diagonal Left
                    #print("DL")
                    return True
                if(checkPos(field, (r, c), player, (1,1), terminating_length)): # Diagonal Right
                    #print("DR")
                    return True
    return False

def Trainer(field):
    col = -1

    for r in range(rows_count):
        for c in range(columns_count):
            if(field[r][c] == p):
                if(checkPos(field, (r, c), p, (1, 0), terminating_length-1)): # Horizontal
                    if r-1 >= 0:
                        if field[r-1][c] == -1:
                            col = c
                            break
                if(checkPos(field, (r, c), p, (0, 1), terminating_length-1)): # Vertical
                    if c-1 >= 0:
                        if field[r][c-1] == -1:
                            col = c-1
                            break
                    if c+terminating_length-1 < columns_count:
                        if field[r][c+terminating_length-1] == -1:
                            col = c + terminating_length-1
                            break
    weights = np.full(columns_count, 1)
    if col >= 0 and col < columns_count:
        weights[col] = 7
    return random.choices(columns, weights)


def draw(field):
    for r in range(rows_count):
        for c in range(columns_count):
            if field[r][c] == -1:
                return False
    #print('Draw')
    return True

def placeStone(field, column, player):
    for r in reversed(range(rows_count)):
        if(field[r][column] == -1):
            field[r][column] = player
            return True
    return False # row is full

def printField(field):
    nField = np.chararray((rows_count, columns_count), itemsize=1, unicode=True)
    numbers = np.chararray((1, columns_count), itemsize=1, unicode=True)
    for r in range(rows_count):
        for c in range(columns_count):
            if(field[r][c] != -1):
                nField[r][c] = players[field[r][c]]
            else:
                nField[r][c] = '-'
    for c in range(columns_count):
        numbers[0][c] = str(c+1)
    print(nField)
    print('-' * (columns_count * 5) )
    print(numbers)

def policyDecideColumn(hState, actionQ):
    weights = np.full(len(columns), e / len(columns))
    # hState = StateHash
    if hState in actionQ:
        if play:
            print(actionQ[hState])
        result = np.argwhere(actionQ[hState] == np.amax(actionQ[hState]))
        bestColumn = random.choice(result)[0] #actionQ[hState].index(max(actionQ[hState]))
        weights[bestColumn] += 1 - e
    col = random.choices(columns, weights)
    return col[0]




def opponentTurn(field, p, ai):
    if (winningConditions(field, ai)):
        return rWin  # AI Winns
    if (draw(field)):
        return rDraw
    if not play:
        while True:
            if (placeStone(field, Trainer(field), p)):
                break
    else:
        printField(field)
        while True:
            try:
                column = int(input('Player ' + str(p+1) + ', Enter Postion (1-' + str(columns_count)+'): '))
                if (column > 0 and column <= columns_count):
                    column -= 1 ## Correct input for Array
                    if (placeStone(field, column, p)):
                        break
                    print('Invalid Input')
                print('Only Numbers between 1 and ' + str(columns_count))
            except ValueError:
                print('Only Numbers')
                continue


    # Reward
    if (winningConditions(field, p)):
        return rLose  # Player Winns
    if (draw(field)):
        return rDraw
    return rStep

def hashField(field):
    return hashlib.sha1(field).hexdigest()




def playGame():
    # print('New Game')
    field = np.full((rows_count, columns_count), -1)
    column = policyDecideColumn(hashField(field), actionQ)
    while True:
        oldField = np.copy(field) ## S
        oldColumn = column ## A
        if (placeStone(field, oldColumn, ai)):  ## Take Action
            reward = opponentTurn(field, p, ai) ## Reward
            hState = hashField(field) ## S'
            if not ( hState in actionQ):
                actionQ[hState] = np.zeros(columns_count).tolist()

        else:  ## Invalid Action
            reward = rInvalid

        column = policyDecideColumn(hashField(field), actionQ) ## A'

        hOldState = hashField(oldField)
        hState = hashField(field)
        if hOldState in actionQ and hState in actionQ:

            actionQ[hOldState][oldColumn] = actionQ[hOldState][oldColumn] + alpha * (
                    reward + gamma * actionQ[hState][column] - actionQ[hOldState][oldColumn])
        else:
            print("error")

        if reward > rStep or reward <= rDraw:
            # someone Winns
            return reward, field

## Debug Values
reward = 0
crandom = 0
cai = 0
last = 0
drw = 0
win = 1
lose = 1
# init StartValue
if not useOld:
    field = np.full((rows_count, columns_count), -1)
    actionQ[hashField(field)] = np.zeros(columns_count).tolist()

if play:
    while True:
        rwd, field = playGame()
        if rwd < rDraw:
            print('You Win')
        if rwd > rStep:
            print('You Loose')
        printField(field)
        if not (input('Restart? (y/n): ') == 'y'):
            break
else:
    for i in range(800000):
        newReward, field = playGame()
        if newReward == -10:
            drw += 1
        if newReward == -100:
            lose += 1
        if newReward == 100:
            win += 1
        # reward += newReward1
        if i % 10000 == 0:
            print(len(actionQ)-last)
            print(str(i/10000) + '%')
            print('Draw: ' + str(drw) + ' Win/Lose ' + str(win/lose))
            last = len(actionQ)
            print()
            #value = actionQ.values()
            #print (key, end=' => ')
            #print(value)
            #print(i)
        if i > 999999:
            rand = False
            e = 0
            #print(cai-crandom)
        #if(newReward == -100):
        #    crandom +=1
        #if (newReward == 100):
        #    cai += 1

print("Result:")
print(len(actionQ))
printField(field)

## Save ActionQ
json = json.dumps(actionQ)
f = open("ActionQ.json","w")
f.write(json)
f.close()
