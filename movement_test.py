from cmu_112_graphics import *
import math, time

def appStarted(app):
    app.cx = int(app.width/2)
    app.cy = int(app.height/2)
    app.cr = 30
    app.xr = 20
    app.yr = 40
    app.angle = 0
    app.move = 1
    app.mph = app.move * 1.6440444056709e-07
    app.edgeX = set()
    app.edgeY = set()
    app.moveIncr = 0
    app.timerDelay = 500
    app.shape = 'rectangle'

def mousePressed(app, event):
    print(event.x, event.y)

def keyPressed(app, event):
    if event.key == 'Right':
        app.angle += 1
    if event.key == 'Left':
        app.angle -= 1



def updateEdge(app):
    app.edgeX = set()
    app.edgeY = set()
    if app.shape == 'circle':
        for angle in range(0, 361):
            app.edgeX.add(int(app.cx + app.cr*math.cos(angle/(2*math.pi))))
            app.edgeY.add(int(app.cy + app.cr*math.sin(angle/(2*math.pi))))
    if app.shape == 'rectangle':
        for xCoord in range(app.cx - app.xr, app.cx + app.xr + 1, 1):
            app.edgeX.add(xCoord)
        for yCoord in range(app.cy - app.yr, app.cy + app.yr + 1, 1):
            app.edgeY.add(yCoord)
        

def timerFired(app):
    updateEdge(app)


def drawPlayer(app, canvas):
    xr1 = app.xr*math.cos(app.angle) - app.yr*math.sin(app.angle)
    yr1 = app.xr*math.sin(app.angle) + app.yr*math.cos(app.angle)
    canvas.create_polygon(app.cx-xr1, app.cy-yr1, app.cx+xr1, app.cy-yr1,
                       app.cx+xr1, app.cy+yr1, app.cx-xr1, app.cy+yr1,
                       fill='darkGreen')


def redrawAll(app, canvas):
    canvas.create_text(app.width/2, 20,
                       text=f'Watch the dot move! speed: {app.mph}')
    drawPlayer(app, canvas)

runApp(width=400, height=400)