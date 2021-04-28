from cmu_112_graphics import *
from PlayerSelection import *
from MazeGenerator import *
from DijkstraSearch import *
import math, time, random

############## THINGS TO DO ##############
# adjust cases for top and bottom collision (maybe revamp system idk)
# within four ranges have cases for hitting forwards or backwards
##########################################


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
    directions = ['up', 'right', 'left', 'down']
    foundDirections = []
    count = 0
    for (drow, dcol) in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
        newRow, newCol = row + drow, col + dcol
        if 0 <= newRow < len(app.map) and 0 <= newCol < len(app.map[0]):
            if app.map[newRow][newCol] == 'c':
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
                    r = 200
                    incr = 3
                    if direction == 'up':
                        for x in range(col*r, (col+1)*r,incr):
                            app.wallCoords.add((x, row*r))
                            # app.wallDirs[direction].append((x, row*r))
                    if direction == 'right':
                        for y in range(row*r, (row+1)*r,incr): 
                            app.wallCoords.add(((col+1)*r, y))
                            # app.wallDirs[direction].append(((col+1)*r, y))
                    if direction == 'left':
                        for y in range(row*r, (row+1)*r,incr):  
                            app.wallCoords.add(((col)*r, y))
                            # app.wallDirs[direction].append(((col)*r, y))
                    if direction == 'down':
                        for x in range(col*r, (col+1)*r,incr):
                            app.wallCoords.add((x, (row+1)*r))
                            # app.wallDirs[direction].append((x, (row+1)*r))
                
def updateWallCoords(app):
    newWall = set()
    for (x, y) in app.wallCoords:
        newX = x - app.scrollX
        newY = y - app.scrollY
        newWall.add((newX, newY))
    print(newWall == app.wallCoords)
    app.wallCoords = newWall
    
    # print(app.wallDirs)

def setPlayerLocation(app):
    for col in range(len(app.map[0])):
        if app.map[0][col] == 'c':
            app.cx = col*300

def appStarted(app):
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
    # payer setup
    app.cx = 150
    app.cy = 100
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
    # app.isTurning = False
    # Enemy AI setup
    app.enemyAI = False
    # Map generation
    app.map = []
    createMap(app)
    app.edgeCoords = set()  #Coordinates of player border
    app.wallCoords = set()  #Coordinates of level borders
    app.wallDirs = {'up' : [], 'left' : [], 'right' : [], 'down' : []}   #Directions for each of the coordinates
    setWallCoords(app)
    setPlayerLocation(app)
    # Other
    app.moveIncr = 0
    app.timerDelay = 10
    app.shape = 'circle'
    app.playerColor = 'red'
    app.timeStarted = time.time()
    app.currTime = 0
    app.mode = 'playerSelect'
    print('Please be sure to turn off Caps lock!!!')

def gameMode_mousePressed(app, event):
    print(event.x, event.y)
    if (event.x, event.y) in app.edgeCoords:
        print('It works')

def gameMode_keyPressed(app, event):
    # app.isTurning = True
    # while app.isTurning:
    if event.key == 'Right':
        app.angle += 0.1
    if event.key == 'Left':
        app.angle -= 0.1
    if event.key == "c":
        app.shape = 'circle'
    if event.key == 'r':
        app.shape = 'rectangle'
    if event.key == 'u':
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
    app.currTime = int(time.time() - app.timeStarted)
    moveX = app.move*math.cos(app.angle)
    moveY = app.move*math.sin(app.angle)
    app.xMomentum += (app.move/15)*math.cos(app.angle)
    app.yMomentum += (app.move/15)*math.sin(app.angle)
    momentumCalc(app)      # This adjusts for sharp turns
    app.xTotalSpeed = (app.xMomentum + moveX)
    app.yTotalSpeed = (app.yMomentum + moveY)
    app.cx += app.xTotalSpeed
    app.cy += app.yTotalSpeed
    app.scrollX = app.xTotalSpeed
    app.scrollY = app.yTotalSpeed
    app.scrollXtot += app.scrollX
    app.scrollYtot += app.scrollY
    updateEdge(app)
    updateWallCoords(app)
    app.speed = ((app.xTotalSpeed**2 + app.yTotalSpeed**2)**(1/2))*10
    if app.maxSpeed < app.speed:
        app.maxSpeed = app.speed
    checkLevel(app)

    # Collision detection
    if app.wallCoords.intersection(app.edgeCoords) != set():
        app.mode = 'gameOver'
        app.impactAngle = app.angle
        print(app.impactAngle)


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
            r = 200
            cx = col*200  + r
            cy = row*200  + r
            cx -= app.scrollXtot
            cy -= app.scrollYtot
            x1, y1, x2, y2 = cx-r,cy-r,cx+r,cy+r
            canvas.create_rectangle(x1, y1, x2, y2, fill = color, width=0)

def gameMode_redrawAll(app, canvas):
    canvas.create_rectangle(-app.width, -app.height, app.width, app.height, 
                            fill = 'black')
    drawMaze(app, canvas)
    drawPlayer(app, canvas)
    text = ((f'Watch the dot move! Speed: {str(int(app.speed))}mph', 
                                            f'Time: {app.currTime}'))
    canvas.create_text(app.width/2, 20, text=text, font = 'Arial 20 bold',
                        fill = 'white')
    

##########################################
# Game Over Mode
##########################################

def gameOver_keyPressed(app, event):
    if event.key == 'u':
        appStarted(app)

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

def gameOver_redrawAll(app, canvas):
    drawMaze(app, canvas)
    drawPlayer(app, canvas)
    canvas.create_text(app.width/2, 50,
                text=(f'Game over! Top speed: {str(int(app.maxSpeed))}mph'),
                font = 'Arial 20 bold', fill = 'white')
    

runApp(width=1400, height=850)

