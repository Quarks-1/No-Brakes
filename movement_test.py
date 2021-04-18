from cmu_112_graphics import *
import math, time

def appStarted(app):
    # payer setup
    app.cx = int(app.width/2)
    app.cy = int(app.height/2)
    app.cr = 30
    app.xr = 40
    app.yr = 20
    app.angle = 0
    app.move = 0.5
    app.xMomentum = 0
    app.yMomentum = 0
    app.edgeX = set()
    app.edgeY = set()
    app.moveIncr = 0
    app.timerDelay = 10
    app.shape = 'rectangle'
    app.timeStart = time.time()

def mousePressed(app, event):
    print(event.x, event.y)

def keyPressed(app, event):
    if event.key == 'Right':
        app.angle += 0.1
    if event.key == 'Left':
        app.angle -= 0.1
    changeVelocity(app)
    print(app.angle)

def changeVelocity(app):

    app.xMomentum = app.move*math.sin(app.angle)
    app.yMomentum = app.move*math.cos(app.angle)
    print(app.xMomentum, app.yMomentum)

def updateEdge(app):
    app.edgeX = set()
    app.edgeY = set()
    if app.shape == 'circle':
        for angle in range(0, 361):
            app.edgeX.add(int(app.cx + app.cr*math.cos(angle/(2*math.pi))))
            app.edgeY.add(int(app.cy + app.cr*math.sin(angle/(2*math.pi))))
########################################################
    # if app.shape == 'rectangle':
    #     for xCoord in range(app.cx - app.xr, app.cx + app.xr + 1, 1):
    #         app.edgeX.add(xCoord)
    #     for yCoord in range(app.cy - app.yr, app.cy + app.yr + 1, 1):
    #         app.edgeY.add(yCoord)
#########################################################

def timerFired(app):
    updateEdge(app)
    currTime = time.time() - app.timeStart
    if currTime > 2:
        app.move += 0.1
        app.timeStart = time.time()
    moveX = app.move*math.cos(app.angle)
    moveY = app.move*math.sin(app.angle)
    app.cx += (app.xMomentum + moveX)
    app.cy -= (app.yMomentum + moveY)


def drawPlayer(app, canvas):
    # top right, bottom left
    xr1 = app.xr*math.cos(app.angle) - app.yr*math.sin(app.angle)
    yr1 = app.xr*math.sin(app.angle) + app.yr*math.cos(app.angle)
    # top left, bottom right
    xr2 = app.yr*math.sin(app.angle) + app.xr*math.cos(app.angle)
    yr2 = app.yr*math.cos(app.angle) - app.xr*math.sin(app.angle)
    canvas.create_polygon(app.cx+xr1, app.cy+yr1, app.cx-xr2, app.cy+yr2, 
                        app.cx-xr1, app.cy-yr1, app.cx+xr2, app.cy-yr2,
                       fill='darkGreen')


def redrawAll(app, canvas):
    canvas.create_text(app.width/2, 20,
                       text=f'Watch the dot move! speed: {app.move}')
    drawPlayer(app, canvas)

runApp(width=1600, height=900)