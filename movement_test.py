from cmu_112_graphics import *
import math, time

##########################################
# THINGS TO DO
# create cases for four angle ranges of collision
# within four ranges have cases for hitting forwards or backwards
# Fix finding rectangle edge coords
##########################################

##########################################
# Game mode
##########################################

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
    app.speed = 0   #Measured in mph
    app.maxSpeed = 0    ##Measured in mph
    app.xMomentum = 0
    app.yMomentum = 0
    app.edgeX = set()
    app.edgeY = set()
    app.moveIncr = 0
    app.timerDelay = 10
    app.shape = 'circle'
    app.playerColor = 'red'
    app.timeStart = time.time()
    app.colliding = False
    app.gameOver = False
    app.mode = 'gameMode'

def gameMode_mousePressed(app, event):
    print(event.x, event.y)

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
    if app.shape == 'circle':
        for angle in range(0, 361):
            app.edgeX.add(int(app.cx + app.cr*math.cos(angle/(2*math.pi))))
            app.edgeY.add(int(app.cy + app.cr*math.sin(angle/(2*math.pi))))

# calc intial values using trig
# front: h/2 cos(315-45)
# top = h/2 sin(45-135)
# back = h/2 cos(135-225)
# bottom = h/2 sin(225-315)

########################################################
    if app.shape == 'rectangle':
        for xCoord in range(app.cx - app.xr, app.cx + app.xr + 1, 1):
            app.edgeX.add(xCoord)
        for yCoord in range(app.cy - app.yr, app.cy + app.yr + 1, 1):
            app.edgeY.add(yCoord)
#########################################################

def checkLevel(app):
    if 0 < app.maxSpeed < 25:
        app.move = 0.15
        app.playerColor = 'red'
        # print('updated color')
    if 25 < app.maxSpeed < 45:
        app.move = 0.25
        app.playerColor = 'yellow'
    if 45 < app.maxSpeed < 65:
        app.move = 0.45
        app.playerColor = 'green'
    if app.maxSpeed > 65:
        app.move = 0.65
        app.playerColor = 'blue'
    

def gameMode_timerFired(app):
    updateEdge(app)
    # Movement
    if not app.colliding:
        moveX = app.move*math.cos(app.angle)
        moveY = app.move*math.sin(app.angle)
        app.xMomentum += (app.move/15)*math.cos(app.angle)
        app.yMomentum += (app.move/15)*math.sin(app.angle)
        app.cx += (app.xMomentum + moveX)
        app.cy += (app.yMomentum + moveY)
        app.speed = (((app.xMomentum + moveX)**2 + 
                        (app.yMomentum + moveY)**2)**(1/2))*10
        if app.maxSpeed < app.speed:
            app.maxSpeed = app.speed
        checkLevel(app)
    # Collision statements
    if (app.width in app.edgeX or app.height in app.edgeY or
                                    0 in app.edgeX or 0 in app.edgeY):
        print('into loop')
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
                            fill=app.playerColor)
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

def collide(app):
    maxBounce = int(app.speed/1.5)
    steps = [x / 9.0 for x in range(maxBounce, 0, -1)]  #initial bounce values
    steps += (x / 40.0 for x in range(3*maxBounce, 0, -1))  #smoothing values
    steps.sort(reverse = True)
    if app.impactAngle > 0:
        if app.impactAngle > 3*math.pi/2 or app.impactAngle < math.pi/2:
            app.cx -= steps[app.moveIncr]*math.cos(app.impactAngle)
            app.cy += steps[app.moveIncr]*math.sin(app.impactAngle)
            app.angle += steps[app.moveIncr]*math.sin(app.impactAngle)*0.02
        elif math.pi/2 < app.impactAngle < 3*math.pi/2:
            app.cx += steps[app.moveIncr]*math.cos(app.impactAngle)
            app.cy += steps[app.moveIncr]*math.sin(app.impactAngle)
            app.angle += steps[app.moveIncr]*math.sin(app.impactAngle)*0.02
    elif app.impactAngle < 0:
        if app.impactAngle > -math.pi/2 or app.impactAngle < -3*math.pi/2:
            app.cx -= steps[app.moveIncr]*math.cos(app.impactAngle)
            app.cy += steps[app.moveIncr]*math.sin(app.impactAngle)
            app.angle += steps[app.moveIncr]*math.sin(app.impactAngle)*0.02
        elif -3*math.pi/2 < app.impactAngle < -math.pi/2:
            app.cx += steps[app.moveIncr]*math.sin(app.impactAngle)
            app.cy += steps[app.moveIncr]*math.cos(app.impactAngle)
            app.angle += steps[app.moveIncr]*math.sin(app.impactAngle)*0.02
    else:
        pass
    
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

runApp(width=800, height=450)