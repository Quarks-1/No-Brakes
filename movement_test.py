from cmu_112_graphics import *
import math, time, random

############## THINGS TO DO ##############
# adjust cases for top and bottom collision (maybe revamp system idk)
# within four ranges have cases for hitting forwards or backwards
# 
##########################################

##########################################
# Game mode
##########################################

# Create possible map
# def createMap(app):
#     rows = app.height//100
#     cols = app.width//100
#     app.map = [[0]*(cols) for x in range(rows)]
#     app.map[1][1] = 1
#     mapBlocks = []
#     # Create all possible blocks
#     for i in range(2):
#         for j in range(2):
#             for k in range(2):
#                 for l in range(2):
#                     mapBlocks += ([(i, j, k, l)])
#     # randomly add them to level
#     for row in range(1, rows-1, 2):
#         for col in range(1, cols-1, 2):
#             if app.map[row][col] == 0:
#                 block = random.choice(mapBlocks)
#                 app.map[row][col] = block[0]
#                 app.map[row][col+1] = block[1]
#                 app.map[row+1][col] = block[2]
#                 app.map[row+1][col+1] = block[3]
    
#     print(app.map)
def getWalls(map, row, col, walls):
    for (drow, dcol) in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
        newRow, newCol = row + drow, col + dcol
        if map[newRow][newCol] == 2:
            walls += [(newRow, newCol)]
    return walls

def createMap(app):
    app.map = [ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 1],
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [1, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 1],
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [1, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 1],
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [1, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 1],
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [1, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 1],
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [1, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] ]
    startRow, startCol = 1, 1
    walls = []
    walls = getWalls(app.map, startRow, startCol, walls)
    while len(walls) > 0:
        wallRow, wallCol = random.choice(walls)
        
        





# def createMaze(map, startRow, startCol, solved):

#     while 

# # Check for solution
# def mapChecker(app, L):
#     startRow, startCol = 1, 1
#     P = copy.deepcopy(L)
#     if helper(app, P, startRow, startCol):
#         return True
#     return False


# def helper(app, L, startRow, startCol): #Check one way trip
#     if (startRow, startCol) == (len(L)-2, len(L[0])-2):
#         return True
#     else:
#         for (drow, dcol) in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
#             newRow, newCol = startRow + drow, startCol + dcol
#             if (newRow, newCol) in app.visited:
#                 continue
#             if 0 <= newRow < len(L) and 0 <= newCol < len(L[0]):
#                 if L[newRow][newCol] == 1:
#                     app.visited.add((startRow, startCol))
#                     solved = helper(app, L, newRow, newCol)
#                     if solved == True:
#                         return True
#         return None
    
# def helper2(app, L, startRow, startCol): #Check way back
#     if (startRow, startCol) == (1, 1):
#         return True
#     else:
#         for (drow, dcol) in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
#             newRow, newCol = startRow + drow, startCol + dcol
#             if (newRow, newCol) in app.visited:
#                 continue
#             if 0 <= newRow < len(L) and 0 <= newCol < len(L[0]):
#                 if L[newRow][newCol]==1 and (newRow, newCol) not in app.visited:
#                     app.visited.add((startRow, startCol))
#                     solved = helper(app, L, newRow, newCol)
#                     if solved == True:
#                         return True
#         return None



# Set boundry coordinates
def setWallCoords(app):
    for x in range(app.width):
        app.wallCoords.add((x, 0))
        app.wallCoords.add((x, app.height))
    for y in range(app.height):
        app.wallCoords.add((0, y))
        app.wallCoords.add((app.width, y))

def appStarted(app):
    # payer setup
    app.cx = int(app.width/2)
    app.cy = int(app.height/2)
    app.cr = 15
    app.xr = 20
    app.yr = 10
    app.angle = 0
    app.impactAngle = 0
    app.move = 0.25
    app.xTotalSpeed = 0
    app.yTotalSpeed = 0
    app.speed = 0   #Measured in mph
    app.maxSpeed = 0    ##Measured in mph
    app.xMomentum = 0
    app.yMomentum = 0
    app.map = []
    app.visited = set()
    createMap(app)
    app.edgeCoords = set()  #Coordinates of player border
    app.wallCoords = set()  #Coordinates of level borders
    setWallCoords(app)
    app.moveIncr = 0
    app.timerDelay = 10
    app.shape = 'circle'
    app.playerColor = 'red'
    app.timeStart = time.time()
    app.mode = 'gameMode'

def gameMode_mousePressed(app, event):
    print(event.x, event.y)
    if (event.x, event.y) in app.edgeCoords:
        print('It works')

def gameMode_keyPressed(app, event):
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
        app.move = 0.15
        app.playerColor = 'red'
    if 25 < app.maxSpeed < 45:
        app.move = 0.25
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
        canvas.create_polygon(app.cx+xr1, app.cy+yr1, app.cx-xr2, app.cy+yr2, 
                            app.cx-xr1, app.cy-yr1, app.cx+xr2, app.cy-yr2,
                            fill=app.playerColor, outline = 'black', width = 2)
    elif app.shape == 'circle':
        xr = app.cr*math.cos(app.angle)
        yr = app.cr*math.sin(app.angle)
        canvas.create_oval(app.cx+app.cr, app.cy+app.cr, 
                            app.cx-app.cr, app.cy-app.cr, 
                            fill=app.playerColor)
        canvas.create_line(app.cx, app.cy, app.cx+xr, app.cy+yr,
                            width = 2, fill = 'black')

def gameMode_redrawAll(app, canvas):
    canvas.create_text(app.width/2, 20,
                text=(f'Watch the dot move! Speed: {str(int(app.speed))}mph'),
                            font = 'Arial 20 bold')
    drawPlayer(app, canvas)

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
    canvas.create_text(app.width/2, 20,
                text=(f'Game over! Top speed: {str(int(app.maxSpeed))}mph'),
                font = 'Arial 20 bold')
    drawPlayer(app, canvas)

runApp(width=1300, height=850)