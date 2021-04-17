from cmu_112_graphics import *
import math, time

def appStarted(app):
    app.cx = app.width/2
    app.cy = app.height/2
    app.r = 40
    app.move = 1
    app.mph = app.move * 1.6440444056709e-07
    app.edgeX = set()
    app.edgeY = set()
    app.moveIncr = 0
    app.timerDelay = 10
    app.colliding = False

def updateEdge(app):
    app.edgeX = set()
    app.edgeY = set()
    for angle in range(0, 361):
        app.edgeX.add(int(app.cx + app.r*math.cos(angle/(2*math.pi))))
        app.edgeY.add(int(app.cy + app.r*math.sin(angle/(2*math.pi))))




def collide(app):
    if app.colliding:
        steps = [x / 7.0 for x in range(20, 0, -1)]
        steps += (x / 40.0 for x in range(20, 0, -1))
        print(steps)
        app.cy -= steps[app.moveIncr]
        if app.moveIncr < len(steps)-1:
            app.moveIncr += 1
        else:
            app.moveIncr = -1

def timerFired(app):
    if not app.colliding:
        app.cy += app.move
    if (app.width in app.edgeX or app.height in app.edgeY or
                                    0 in app.edgeX or 0 in app.edgeY):
        app.colliding = True
    if app.moveIncr != -1:
        collide(app)
    else:
        app.colliding = False
        app.moveIncr = 0
        app.move = 0
    updateEdge(app)

def redrawAll(app, canvas):
    canvas.create_text(app.width/2, 20,
                       text=f'Watch the dot move! speed: {app.mph}')
    canvas.create_oval(app.cx-app.r, app.cy-app.r,
                       app.cx+app.r, app.cy+app.r,
                       fill='darkGreen')

runApp(width=400, height=400)