from cmu_112_graphics import *
from PlayerSelection import *
from MazeGenerator import *
from DijkstraSearch import *
from StartScreen import *
# from leaderboard import *
import math, time, random, os, copy

######################################################################
# From: https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen
    
def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows, cols = len(a), len(a[0])
    fieldWidth = maxItemLength(a)
    print('[')
    for row in range(rows):
        print(' [ ', end='')
        for col in range(cols):
            if (col > 0): print(', ', end='')
            print(str(a[row][col]).rjust(fieldWidth), end='')
        print(' ]')
    print(']')
######################################################################

##########################################
# Game mode
##########################################

def getCorridorDirs(app, row, col):
    directions = ['down', 'right', 'left', 'up']
    foundDirections = []
    count = 0
    for (drow, dcol) in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
        newRow, newCol = row + drow, col + dcol
        if 0 <= newRow < len(app.map) and 0 <= newCol < len(app.map[0]):
            if app.map[newRow][newCol] in ['c', 's', 'f']:
                foundDirections.append(directions[count])
        count += 1
    return foundDirections

# Set boundry coordinates
def setWallCoords(app):
    for row in range(len(app.map)):
        for col in range(len(app.map[0])):
            if app.map[row][col] == 'w':
                directions = getCorridorDirs(app, row, col)
                for direction in directions:
                    r = 100
                    incr = 2
                    if direction == 'up':
                        for x in range(col*r, (col+1)*r,incr):
                            app.wallCoords.add((x, row*r))
                            app.wallDirs[direction].append((x, row*r))
                    if direction == 'right':
                        for y in range(row*r, (row+1)*r,incr): 
                            app.wallCoords.add(((col+1)*r, y))
                            app.wallDirs[direction].append(((col+1)*r, y))
                    if direction == 'left':
                        for y in range(row*r, (row+1)*r,incr):  
                            app.wallCoords.add(((col)*r, y))
                            app.wallDirs[direction].append(((col)*r, y))
                    if direction == 'down':
                        for x in range(col*r, (col+1)*r,incr):
                            app.wallCoords.add((x, (row+1)*r))
                            app.wallDirs[direction].append((x, (row+1)*r))

def updateWallCoords(app):
    newWall = set()
    for (x, y) in app.wallCoords:
        newX = x - app.scrollXtot
        newY = y - app.scrollYtot
        newWall.add((newX, newY))
    app.actualWallCoords = newWall   

def setPlayerLocation(app):
    for col in range(len(app.map[0])):
        if app.map[0][col] == 's':
            app.cx = col*100 + 50
    app.cy = 50

def checkForWin(app):
    row, col = getPlayerCell(app)
    if app.map[row][col] == 'f':
        createNewStage(app)

def createNewStage(app):
    app.map = []
    createMap(app)
    app.edgeCoords = set()  #Coordinates of player border
    app.wallCoords = set()  #Coordinates of level borders
    setWallCoords(app)
    setPlayerLocation(app)

def appStarted(app):
    ##########################
    # Start Screen Variables
    ##########################
    app.sb1x = app.width/2
    app.sb1y = 350
    app.sb2x = app.sb1x
    app.sb2y = app.sb1y + 200
    app.sb3x = app.sb1x
    app.sb3y = app.sb2y + 200
    app.sbrx = 300
    app.sbry = 75
    app.sHovering = ''
    app.sHoverWidth1, app.sHoverWidth2, app.sHoverWidth3 = 1,1,1
    app.startSpritey = app.height/2
    app.startSpritex2 = 175
    app.startSpritex1 = app.width - 175
    app.incr = 10
    ##########################
    # Player Selection Variables
    ##########################
    app.b1x = 250
    app.b1y = 700
    app.b2x = 650
    app.b2y = app.b1y
    app.b3x = 1100
    app.b3y = app.b1y
    app.b4x = app.b3x
    app.b4y = 400
    app.br = 100
    app.mouseX = 0
    app.mouseY = 0
    app.selected = ''
    app.b1Color = 'red'
    app.b2Color = 'green'
    app.selectBorderInr = 0
    app.hoverWidth1, app.hoverWidth2, app.hoverWidth3, app.hoverWidth4 = 1,1,1,1
    app.hovering = ''
    app.choiceAngle = 0
    app.choiceR = 50
    app.choiceXR = 60
    app.choiceYR = 30
    ##########################
    # Game Variables
    ##########################
    # player setup
    app.cx = 0
    app.cy = 0 
    app.cr = 15
    app.xr = 20
    app.yr = 10
    app.angle = math.pi/2
    app.impactAngle = 0
    app.move = 0.25
    app.xTotalSpeed = 0
    app.yTotalSpeed = 0
    app.speed = 0   #Measured in mph
    app.maxSpeed = 0    ##Measured in mph
    app.xMomentum = 0
    app.yMomentum = 0
    app.scrollX = 0
    app.scrollY = 0
    app.scrollXtot = 0
    app.scrollYtot = 0
    app.playerCell = tuple()
    app.impactx = 0
    app.impacty = 0
    # Map generation
    app.map = []
    createMap(app)
    app.edgeCoords = set()  #Coordinates of player border
    app.wallCoords = set()  #Coordinates of level borders
    app.wallDirs = {'up' : [], 'left' : [], 'right' : [], 'down' : []}   #Directions for each of the coordinates
    setWallCoords(app)
    setPlayerLocation(app)
    # Enemy AI setup
    app.enemyAI = False
    app.enemyMoves = []
    app.rowAI, app.colAI = chooseStart(app)
    # Other
    app.moveIncr = 0
    app.timerDelay = 10
    app.shape = 'reactangle'
    app.playerColor = 'red'
    app.timeStarted = time.time()
    app.time0 = time.time()
    app.timeElapsed = 0
    app.mode = 'startScreen'
    app.input = ''
    app.name = ''


def gameMode_keyPressed(app, event):
    app.input = event.key

def gameMode_keyReleased(app, event):
    app.input = ''

def rotatePlayer(app):
    if app.input == 'Right':
        app.angle += 0.085
    if app.input == 'Left':
        app.angle -= 0.085
    if app.input == "c":
        app.shape = 'circle'
    if app.input == 'r':
        app.shape = 'rectangle'
    if app.input == 'u':
        appStarted(app)
    if app.angle > 2*math.pi or app.angle < -2*math.pi:
        app.angle = 0

def updateEdge(app):
    app.edgeCoords = set()
    if app.shape == 'circle':
        for angle in range(0, 360):
            angle = angle*(math.pi/180)
            app.edgeCoords.add((int(app.cx+app.cr*math.cos(angle)), 
                              int(app.cy+app.cr*math.sin(angle))))
    if app.shape == 'rectangle':
    # Find initial values before rotation
        tempEdgeCoords = set()
        for x in range(-app.xr, app.xr+1):
            tempEdgeCoords.add((x, -app.yr))
            tempEdgeCoords.add((x, app.yr))
        for y in range(-app.yr, app.yr+1):
            tempEdgeCoords.add((-app.xr, y))
            tempEdgeCoords.add((app.xr, y))
        # Rotate by angle of player
        for (x, y) in tempEdgeCoords:
            xr = x*math.cos(app.angle) - y*math.sin(app.angle)
            yr = x*math.sin(app.angle) + y*math.cos(app.angle)
            # Add to actual edge coordinate list
            app.edgeCoords.add((int(app.cx + xr), int(app.cy + yr)))

def checkLevel(app):
    if 0 < app.maxSpeed < 25:
        app.move = 0.25
        app.playerColor = 'red'
    if 25 < app.maxSpeed < 45:
        app.move = 0.35
        app.playerColor = 'yellow'
    if 45 < app.maxSpeed < 65:
        app.move = 0.45
        app.playerColor = 'green'
    if app.maxSpeed > 65:
        app.move = 0.65
        app.playerColor = 'blue'
    
def momentumCalc(app):
    if ((app.xMomentum < 0 and math.cos(app.angle) > 0) or
            (app.xMomentum > 0 and math.cos(app.angle) < 0)):
        app.xMomentum *= .95
    if ((app.yMomentum < 0 and math.sin(app.angle) > 0) or
            (app.yMomentum > 0 and math.sin(app.angle) < 0)):
        app.yMomentum *= .95

def gameMode_timerFired(app):
    # Movement
    app.timeElapsed = int(time.time() - app.time0)
    currTime = int(time.time() - app.timeStarted)
    checkForWin(app)
    rotatePlayer(app)
    if app.enemyAI and currTime > 2:    #Move enemy once per second
        moveAI(app)
        app.timeStarted = int(time.time())
        prow, pcol = getPlayerCell(app)
        if app.rowAI == prow and app.colAI == pcol:
            app.mode = 'gameOver'
    moveX = app.move*math.cos(app.angle)
    moveY = app.move*math.sin(app.angle)
    app.xMomentum += (app.move/15)*math.cos(app.angle)
    app.yMomentum += (app.move/15)*math.sin(app.angle)
    momentumCalc(app)      # This adjusts for sharp turns
    app.xTotalSpeed = (app.xMomentum + moveX)
    app.yTotalSpeed = (app.yMomentum + moveY)
    app.cx += app.xTotalSpeed
    app.cy += app.yTotalSpeed
    updateEdge(app)
    app.speed = ((app.xTotalSpeed**2 + app.yTotalSpeed**2)**(1/2))*10
    if app.maxSpeed < app.speed:
        app.maxSpeed = app.speed
    checkLevel(app)

    # Collision detection
    if app.wallCoords.intersection(app.edgeCoords) != set():
        impactSet = app.wallCoords.intersection(app.edgeCoords)
        impactSet = list(impactSet)
        app.impactx = impactSet[0][0]
        app.impacty = impactSet[0][1]
        app.mode = 'gameOver'
        app.impactAngle = app.angle


def drawPlayer(app, canvas):
    if app.shape == 'rectangle':
        # top right, bottom left
        xr1 = app.xr*math.cos(app.angle) - app.yr*math.sin(app.angle)
        yr1 = app.xr*math.sin(app.angle) + app.yr*math.cos(app.angle)
        # top left, bottom right
        xr2 = app.yr*math.sin(app.angle) + app.xr*math.cos(app.angle)
        yr2 = app.yr*math.cos(app.angle) - app.xr*math.sin(app.angle)
        # Coordinate pairs
        x1, y1 = app.cx+xr1, app.cy+yr1
        x2, y2 = app.cx-xr2, app.cy+yr2
        x3, y3 = app.cx-xr1, app.cy-yr1
        x4, y4 = app.cx+xr2, app.cy-yr2
        canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4,
                            fill=app.playerColor, outline = 'black', width = 2)
    elif app.shape == 'circle':
        xr = app.cr*math.cos(app.angle)
        yr = app.cr*math.sin(app.angle)
        x1, y1 = app.cx+app.cr, app.cy+app.cr
        x2, y2 = app.cx-app.cr, app.cy-app.cr
        canvas.create_oval(x1, y1, x2, y2, fill=app.playerColor)
        x3, y3 = app.cx+xr, app.cy+yr
        canvas.create_line(app.cx, app.cy, x3, y3, width = 2, fill = 'black')

def drawMaze(app, canvas):
    for row in range(len(app.map)):
        for col in range(len(app.map[0])):
            if app.map[row][col] == 'w':
                color = 'black'
            if app.map[row][col] == 'c':
                color = 'lightblue'
            if app.map[row][col] == 's':
                color = 'salmon'
            if app.map[row][col] == 'f':
                color = 'lightgreen'
            if app.map[row][col] == 'AI':
                color = 'darkviolet'
            r = 50
            cx = col*100 + r
            cy = row*100 + r
            canvas.create_rectangle(cx-r,cy-r,cx+r,cy+r, fill = color, width=0)

def gameMode_redrawAll(app, canvas):
    drawMaze(app, canvas)
    drawPlayer(app, canvas)
    text = ((f'Watch the dot move! Speed: {str(int(app.speed))}mph', 
                                            f'Time: {app.timeElapsed}'))
    canvas.create_text(app.width/2, 20, text=text, font = 'Arial 20 bold',
                        fill = 'white')
    

##########################################
# Game Over Mode
##########################################

def storeScore(app):
    leaderboardData = open("leaderboardData.txt", 'a')
    playerData = str(app.name + ',' + str(int(app.maxSpeed)) + ',')
    leaderboardData.write(playerData)
    leaderboardData.close()

def gameOver_keyPressed(app, event):
    if event.key == 'Escape':
        appStarted(app)
    if event.key == 'Enter' and 0 < len(app.name) < 4:
        storeScore(app)
        app.mode = 'leaderboard'
    inputKey = event.key.upper()
    if len(inputKey) == 1 and len(app.name) < 3:
        app.name += inputKey
    if event.key == 'Backspace' and len(app.name) > 0:
        app.name = app.name[:-1]

def angleChange(app, steps, angle):
    if app.shape == 'circle':
        app.angle += steps[app.moveIncr]*math.sin(angle)*0.02
    else:
        app.angle -= steps[app.moveIncr]*math.sin(angle)*0.02

def collide(app):
    maxBounce = int(app.speed/1.5)
    steps = [x / 9.0 for x in range(maxBounce, 0, -1)]  #initial bounce values
    steps += (x / 40.0 for x in range(3*maxBounce, 0, -1))  #smoothing values
    steps.sort(reverse = True)
    # Many different cases for front/back player impact 
    # and left/right side level impact
    xDir = 1
    yDir = 1
    angleDir = 1
    if app.impactAngle > 0:
        if app.xMomentum > 0:
            if app.impactAngle > 3*math.pi/2 or app.impactAngle < math.pi/2:
                xDir = -1
                yDir = 1
                angleDir = 1
            elif math.pi/2 < app.impactAngle < 3*math.pi/2:
                xDir = 1
                yDir = 1
                angleDir = 1
            angleChange(app, steps, app.impactAngle)
        else:
            if app.impactAngle > 3*math.pi/2 or app.impactAngle < math.pi/2:
                xDir = 1
                yDir = 1
                angleDir = -1
            elif math.pi/2 < app.impactAngle < 3*math.pi/2:
                xDir = -1
                yDir = 1
                angleDir = -1
            angleChange(app, steps, -app.impactAngle)
    elif app.impactAngle < 0:
        if app.xMomentum > 0:
            if app.impactAngle > -math.pi/2 or app.impactAngle < -3*math.pi/2:
                xDir = -1
                yDir = 1
                angleDir = 1
            elif -3*math.pi/2 < app.impactAngle < -math.pi/2:
                xDir = 1
                yDir = 1
                angleDir = 1
            angleChange(app, steps, app.impactAngle)
        else:
            if app.impactAngle > -math.pi/2 or app.impactAngle < -3*math.pi/2:
                xDir = 1
                yDir = 1
                angleDir = -1
            elif -3*math.pi/2 < app.impactAngle < -math.pi/2:
                xDir = -1
                yDir = 1
                angleDir = -1
            angleChange(app, steps, -app.impactAngle)
    for dirs in app.wallDirs:
        if (app.impactx, app.impacty) in app.wallDirs[dirs]:
            if dirs == 'up':
                yDir = -1
            if dirs == 'down':
                yDir = -1
            if dirs == 'up' and app.shape == 'circle':
                xDir = 1
            if dirs == 'down' and app.shape == 'circle':
                xDir = 1
            
    app.cx += (steps[app.moveIncr]*math.cos(app.impactAngle))*xDir
    app.cy += (steps[app.moveIncr]*math.sin(app.impactAngle))*yDir
    angleChange(app, steps, app.impactAngle*angleDir)
    if app.moveIncr < len(steps)-1:
        app.moveIncr += 1
    else:
        app.moveIncr = -1

def gameOver_timerFired(app):
    if app.moveIncr != -1:
        collide(app)    
    updateEdge(app)

def drawNameBox(app, canvas):
    x1, y1 = app.width/2 - 200, app.height/2 - 100
    x2, y2 = app.width/2 + 200, app.height/2 + 100
    canvas.create_rectangle(x1, y1, x2, y2, fill = 'white', width = 3)
    canvas.create_text(app.width/2, app.height/2, text = app.name,
                    font = 'Arial 50 bold')

def drawMessages(app, canvas):
    speed = int(app.maxSpeed)
    canvas.create_text(app.width/2, 25,
                text=(f'Game over! Top speed: {speed}mph'),
                font = 'Arial 20 bold', fill = 'white')
    canvas.create_text(app.width/2, 50,
                text = 'Please type your name to store your score',
                font = 'Arial 20 bold', fill = 'white')
    canvas.create_text(app.width/2, 75,
                text = 'or press escape to restart',
                font = 'Arial 20 bold', fill = 'white')

def gameOver_redrawAll(app, canvas):
    drawMaze(app, canvas)
    drawPlayer(app, canvas)
    drawMessages(app, canvas)
    drawNameBox(app, canvas)

##########################################
# Leaderboard
##########################################

def leaderboard_keyPressed(app, event):
    if event.key == 'Escape':
        app.mode = 'startScreen'

def drawNames(app, canvas):
    leaderboardData = open("leaderboardData.txt", 'r')
    prev = leaderboardData.read()
    listedData = copy.deepcopy(prev)
    leaderboardData.close()
    listedData = listedData.split(',')
    if len(listedData)//2 != 0:
        listedData.pop()
    sortedData = []
    # Sort leaderboard
    while len(listedData) != len(sortedData):
        bestScore = 0
        bestName = ''    
        for spot in range(0, len(listedData), 2):
            currNum = listedData[spot+1]
            currName = listedData[spot]
            currNum = int(currNum)
            if currNum > bestScore and currName not in sortedData:
                bestScore = currNum
                bestName = listedData[spot]
        sortedData.append(bestName)
        sortedData.append(bestScore)
    counter = 0
    # Draw sorted leaderboard
    for data in range(0, len(sortedData), 2):
        name = sortedData[data]
        speed = sortedData[data+1]
        if name == '':
            continue
        yPos = 150 + counter*100
        canvas.create_rectangle(0, yPos-50, app.width, yPos+50, fill = 'whitesmoke')
        canvas.create_text(app.width/5, yPos, text = name,
                            font = 'Arial 40 bold')
        canvas.create_text(app.width*(4/5), yPos, text = f'{speed}  mph',
                            font = 'Arial 40 bold')
        counter += 1
        if counter > 6:
            break

def leaderboard_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'silver')
    canvas.create_text(app.width/2, 50, text = 'Leaderboard',
                        font = 'Arial 50 bold')
    canvas.create_text(app.width/5, 50, text = 'Player',
                        font = 'Arial 40 bold')
    canvas.create_text(app.width*(4/5), 50, text = 'Speed',
                        font = 'Arial 40 bold')
    drawNames(app, canvas)
    canvas.create_text(app.width/2, app.height-50, text = 'Press escape to return home',
                        font = 'Arial 35 bold')

def quit_timerFired(app):
    os._exit(0)

runApp(width=1400, height=900)


