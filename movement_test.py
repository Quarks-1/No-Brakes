from cmu_112_graphics import *
import math, time, random

############## THINGS TO DO ##############
# adjust cases for top and bottom collision (maybe revamp system idk)
# within four ranges have cases for hitting forwards or backwards
##########################################


######################################################################
# From: https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing
# Helper function for print2dList.
# This finds the maximum length of the string
# representation of any item in the 2d list
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

# Because Python prints 2d lists on one row,
# we might want to write our own function
# that prints 2d lists a bit nicer.
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
# Player Selection Mode
##########################################

def playerSelect_mouseMoved(app, event):
    x1, y1 = app.b1x - app.br - 20, app.b1y - app.br - 20
    x2, y2 = app.b1x + app.br, app.b1y + app.br
    x3, y3 = app.b2x - app.br - 20, app.b2y - app.br - 20
    x4, y4 = app.b2x + app.br, app.b2y + app.br
    x5, y5 = app.b3x - 220, app.b3y - app.br - 20
    x6, y6 = app.b3x + 180, app.b3y + app.br
    x7, y7 = app.b4x - 130, app.b4y - app.br - 20
    x8, y8 = app.b4x + 130, app.b4y + app.br
    if x1 < event.x < x2 and y1 < event.y < y2: #Circle button
        app.hovering = 'circle'
    elif x3 < event.x < x4 and y3 < event.y < y4: #Rectangle button
        app.hovering = 'rectangle'
    elif x5 < event.x < x6 and y5 < event.y < y6: #Continue button
        app.hovering = 'continue'
    elif x7 < event.x < x8 and y7 < event.y < y8: #Continue button
        app.hovering = 'AImode'
    else:
        app.hovering = ''
        app.hoverWidth1, app.hoverWidth2, app.hoverWidth3 = 1, 1, 1
        app.hoverWidth4 = 1
    print(event.x, event.y)

def playerSelect_mousePressed(app, event):
    x1, y1 = app.b1x - app.br - 20, app.b1y - app.br - 20
    x2, y2 = app.b1x + app.br, app.b1y + app.br
    x3, y3 = app.b2x - app.br - 20, app.b2y - app.br - 20
    x4, y4 = app.b2x + app.br, app.b2y + app.br
    x5, y5 = app.b3x - 220, app.b3y - app.br - 20
    x6, y6 = app.b3x + 180, app.b3y + app.br
    x7, y7 = app.b4x - 130, app.b4y - app.br - 20
    x8, y8 = app.b4x + 130, app.b4y + app.br
    if x1 < event.x < x2 and y1 < event.y < y2: #Circle button
        app.shape = 'circle'
        app.selected = 'circle'
        app.b1Color = 'firebrick'
        app.b2Color = 'green'
    if x3 < event.x < x4 and y3 < event.y < y4: #Rectangle button
        app.shape = 'rectangle'
        app.selected = 'rectangle'
        app.b1Color = 'red'
        app.b2Color = 'darkGreen'
    if x5 < event.x < x6 and y5 < event.y < y6: #Continue button
        app.mode = 'gameMode'
    if x7 < event.x < x8 and y7 < event.y < y8: #AI mode button
        app.enemyAI = not app.enemyAI

def drawButtons(app, canvas):
    # Circle button
    offset = 10
    x1, y1 = app.b1x - app.br, app.b1y - app.br
    x2, y2 = app.b1x + app.br, app.b1y + app.br
    x3, y3 = app.b2x - app.br, app.b2y - app.br
    x4, y4 = app.b2x + app.br, app.b2y + app.br
    xr = 200
    x5, y5 = app.b3x - xr, app.b3y - app.br
    x6, y6 = app.b3x + xr, app.b3y + app.br
    aiR = 150
    x7, y7 = app.b4x - aiR, app.b4y - app.br
    x8, y8 = app.b4x + aiR, app.b4y + app.br
    if app.selected == 'circle':
        canvas.create_rectangle(x1, y1, x2, y2, fill = app.b1Color, width = 1)
        canvas.create_text((x1 + x2)/2, (y1 + y2)/2, 
                            text = 'Selected', font = 'Arial 20 bold')
    else:
        canvas.create_rectangle(x1, y1, x2, y2, fill = 'lightcoral', width = 0)
        x1 -= offset
        x2 -= offset
        y1 -= offset
        y2 -= offset
        canvas.create_rectangle(x1, y1, x2, y2, fill = app.b1Color, 
                                width = app.hoverWidth1)
        canvas.create_text((x1 + x2)/2, (y1 + y2)/2, text = 'Select', 
                            font = 'Arial 30 bold')
    # Rectangle button
    if app.selected == 'rectangle':
        canvas.create_rectangle(x3, y3, x4, y4, fill = app.b2Color, width = 1)
        canvas.create_text((x3 + x4)/2, (y3 + y4)/2, 
                            text = 'Selected', font = 'Arial 20 bold')
    else:
        canvas.create_rectangle(x3, y3, x4, y4, fill = 'lime', width = 0)
        x3 -= offset
        x4 -= offset
        y3 -= offset
        y4 -= offset
        canvas.create_rectangle(x3, y3, x4, y4, fill = app.b2Color, 
                                width = app.hoverWidth2)
        canvas.create_text((x3 + x4)/2, (y3 + y4)/2, text = 'Select', 
                            font = 'Arial 30 bold')
    # AI mode button:
    if app.enemyAI:
        canvas.create_rectangle(x7, y7, x8, y8, fill = 'darkorange4')
        canvas.create_text(app.b4x, app.b4y, text = 'Enabled', 
                            font = 'Arial 30 bold')
    else:
        canvas.create_rectangle(x7, y7, x8, y8, fill = 'darkorange2')
        x7 -= offset
        x8 -= offset
        y7 -= offset
        y8 -= offset
        canvas.create_rectangle(x7, y7, x8, y8, fill = 'orange', 
                                        width = app.hoverWidth4)
        canvas.create_text((x7 + x8)/2, (y7 + y8)/2, text = 'Disabled', 
                            font = 'Arial 30 bold')
    # Continue button
    canvas.create_rectangle(x5, y5, x6, y6, fill = 'goldenrod')
    x5 -= offset
    x6 -= offset
    y5 -= offset
    y6 -= offset
    canvas.create_rectangle(x5, y5, x6, y6, fill = 'gold', 
                                    width = app.hoverWidth3)
    canvas.create_text((x5 + x6)/2, (y5 + y6)/2, 
                        text = 'Continue', font = 'Arial 50 bold')

def drawChoices(app, canvas):
    y = 300
    # Circle
    x1, y1 = app.b1x - app.choiceR, y - app.choiceR
    x2, y2 = app.b1x + app.choiceR, y + app.choiceR
    canvas.create_oval(x1, y1, x2, y2, fill = 'red')
    xr = app.choiceR*math.cos(app.choiceAngle)
    yr = app.choiceR*math.sin(app.choiceAngle)
    x3, y3 = app.b1x+xr, y+yr
    canvas.create_line(app.b1x, y, x3, y3, width = 2, fill = 'black')
    # Rectangle - same calculations used in drawing player during gameplay
    # top right, bottom left
    xr1 = (app.choiceXR*math.cos(app.choiceAngle) - 
                app.choiceYR*math.sin(app.choiceAngle))
    yr1 = (app.choiceXR*math.sin(app.choiceAngle) + 
                app.choiceYR*math.cos(app.choiceAngle))
    # top left, bottom right
    xr2 = (app.choiceYR*math.sin(app.choiceAngle) + 
                app.choiceXR*math.cos(app.choiceAngle))
    yr2 = (app.choiceYR*math.cos(app.choiceAngle) - 
                app.choiceXR*math.sin(app.choiceAngle))
    # Coordinate pairs
    x1, y1 = app.b2x+xr1, y+yr1
    x2, y2 = app.b2x-xr2, y+yr2
    x3, y3 = app.b2x-xr1, y-yr1
    x4, y4 = app.b2x+xr2, y-yr2
    canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4,
                        fill= 'green', outline = 'black', width = 2)
    x = (app.b1x + app.b2x)/2
    canvas.create_text(x, 100, text = 'Choose your character:', fill = 'white',
                        font = 'Arial 40 bold')
    canvas.create_text(app.b4x, 200, text = 'Enable enemy AI?:',
                        font = 'Arial 35 bold', fill = 'white')


def playerSelect_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'darkblue')
    drawButtons(app, canvas)
    drawChoices(app, canvas)

def playerSelect_timerFired(app):
    currTime = time.time() - app.timeStarted
    if app.hovering == 'circle':
        if 0 <= app.hoverWidth1 <= 6:
            app.hoverWidth1 += 0.25
        else:
            app.hoverWidth1 = 1
    if app.hovering == 'rectangle':
        if 0 <= app.hoverWidth2 <= 6:
            app.hoverWidth2 += 0.25
        else:
            app.hoverWidth2 = 1
    if app.hovering == 'continue':
        if 0 <= app.hoverWidth3 <= 6:
            app.hoverWidth3 += 0.25
        else:
            app.hoverWidth3 = 1
    if app.hovering == 'AImode':
        if 0 <= app.hoverWidth4 <= 6:
            app.hoverWidth4 += 0.25
        else:
            app.hoverWidth4 = 1
    currTime = time.time()
    app.choiceAngle += 0.05

##########################################
# Game mode
##########################################

def getSurroundingCells(app, row, col):
    count = 0
    for (drow, dcol) in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
        newRow, newCol = row + drow, col + dcol
        if app.map[newRow][newCol] == 'c':
            count += 1
    return count


def createMap(app):
    rows = app.height//100
    cols = app.width//100
    app.map = [['u' for i in range(cols)] for j in range(rows)]
    startRow, startCol = 1, 1
    app.map[startRow][startCol] = 'c'
    walls = []
    illegalVals = [0, rows-1, cols-1]
    # Create first set of walls
    for (drow, dcol) in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
        newRow, newCol = startRow + drow, startCol + dcol
        walls.append((newRow, newCol))
        app.map[newRow][newCol] = 'w'
    # Connect walls and paths
    while len(walls) != 0:
        # Select random wall
        (wallRow, wallCol) = random.choice(walls)
        # Make sure it's in the map
        if 0 < wallRow < rows-1 and 0 < wallCol < cols-1:
            # Proceed to check which type of wall it is, then add as corridor
            # and update new surrounding walls
            # Right wall
            if (app.map[wallRow][wallCol-1] == 'c' and 
                app.map[wallRow][wallCol+1] == 'u'):
                sCells = getSurroundingCells(app, wallRow, wallCol)
                if sCells < 2:
                    app.map[wallRow][wallCol] = 'c'
                    for (drow, dcol) in [(0, 1), (-1, 0), (1, 0)]:
                        newRow, newCol = wallRow + drow, wallCol + dcol
                        if (wallCol != cols-1 or wallRow != rows-1 or 
                            wallRow !=0):
                            if app.map[newRow][newCol] != 'c':
                                app.map[newRow][newCol] == 'w'
                            if (newRow, newCol) not in walls:
                                walls.append((newRow, newCol))
                walls.remove((wallRow, wallCol))
                continue
            # Bottom wall
            if (app.map[wallRow-1][wallCol] == 'c' and 
                app.map[wallRow+1][wallCol] == 'u'):
                sCells = getSurroundingCells(app, wallRow, wallCol)
                if sCells < 2:
                    app.map[wallRow][wallCol] = 'c'
                    for (drow, dcol) in [(1, 0), (0, -1), (0, 1)]:
                        newRow, newCol = wallRow + drow, wallCol + dcol
                        if (wallRow != rows-1 or wallCol != 0 or 
                            wallCol != cols-1):
                            if app.map[newRow][newCol] != 'c':
                                app.map[newRow][newCol] == 'w'
                            if (newRow, newCol) not in walls:
                                walls.append((newRow, newCol))
                walls.remove((wallRow, wallCol))
                continue
            # Upper wall
            if (app.map[wallRow+1][wallCol] == 'c' and 
                app.map[wallRow-1][wallCol] == 'u'):
                sCells = getSurroundingCells(app, wallRow, wallCol)
                if sCells < 2:
                    app.map[wallRow][wallCol] = 'c'
                    for (drow, dcol) in [(0, 1), (0, -1), (-1, 0)]:
                        newRow, newCol = wallRow + drow, wallCol + dcol
                        if (wallRow!= 0 or wallCol != 0 or wallCol != cols - 1):
                            if app.map[newRow][newCol] != 'c':
                                app.map[newRow][newCol] == 'w'
                            if (newRow, newCol) not in walls:
                                walls.append((newRow, newCol))
                walls.remove((wallRow, wallCol))
                continue
            # Left Wall
            if (app.map[wallRow][wallCol+1] == 'c' and 
                app.map[wallRow][wallCol-1] == 'u'):
                sCells = getSurroundingCells(app, wallRow, wallCol)
                if sCells < 2:
                    app.map[wallRow][wallCol] = 'c'
                    for (drow, dcol) in [(1, 0), (0, -1), (-1, 0)]:
                        newRow, newCol = wallRow + drow, wallCol + dcol
                        if (wallRow != 0 or wallRow != rows-1 or wallCol != 0):
                            if app.map[newRow][newCol] != 'c':
                                app.map[newRow][newCol] == 'w'
                            if (newRow, newCol) not in walls:
                                walls.append((newRow, newCol))
                walls.remove((wallRow, wallCol))
                continue
            walls.remove((wallRow, wallCol))
        else:
            walls.remove((wallRow, wallCol))

    # Add border walls
    for row in range(rows):
        for col in range(cols):
            if app.map[row][col] == 'u':
                app.map[row][col] = 'w'

    # Create entrance
    for col in range(0, cols):
        if app.map[1][col] == 'c':
            app.map[0][col] = 'c'
            break

    for col in range(cols-1, 0, -1):
        if app.map[rows-2][col] == 'c':
            app.map[rows-1][col] = 'c'
            break

# Set boundry coordinates
def setWallCoords(app):
    for row in range(len(app.map)):
        for col in range(len(app.map[0])):
            if app.map[row][col] == 'w':
                for x in range(col*100, (col+1)*100):
                    x -= app.scrollX
                    app.wallCoords.add((x, row*100))
                    app.wallCoords.add((x, (row+1)*100))
                for y in range(row*100, (row+1)*100):
                    y-= app.scrollY
                    app.wallCoords.add(( col*100, y))
                    app.wallCoords.add(( (col+1)*100, y))
                

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
    # Enemy AI setup
    app.enemyAI = False
    # Map generation
    app.map = []
    createMap(app)
    app.edgeCoords = set()  #Coordinates of player border
    app.wallCoords = set()  #Coordinates of level borders
    setWallCoords(app)
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
    # setWallCoords(app)
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
    app.scrollX += app.xTotalSpeed
    app.scrollY += app.yTotalSpeed
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
            r = 50
            cx = col*100 + 50
            cy = row*100 + 50
            # cx -= app.scrollX
            # cy -= app.scrollY
            x1, y1, x2, y2 = cx-r,cy-r,cx+r,cy+r
            canvas.create_rectangle(x1, y1, x2, y2, fill = color, width=0)

def gameMode_redrawAll(app, canvas):
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
    canvas.create_text(app.width/2, 20,
                text=(f'Game over! Top speed: {str(int(app.maxSpeed))}mph'),
                font = 'Arial 20 bold')
    drawMaze(app, canvas)
    drawPlayer(app, canvas)

runApp(width=1400, height=900)