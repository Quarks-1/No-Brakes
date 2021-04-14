from cmu_112_graphics import *
import math

def appStarted(app):
    app.cx = app.width/2
    app.cy = app.height/2
    app.r = 40
    app.move = 2
    app.edgeX = set()
    app.edgeY = set()

def updateEdge(app):
    app.edgeX = set()
    app.edgeY = set()
    for angle in range(0, 361):
        app.edgeX.add(int(app.cx + app.r*math.cos(angle/(2*math.pi))))
        app.edgeY.add(int(app.cy + app.r*math.sin(angle/(2*math.pi))))
    print(app.edgeX, app.edgeY)

def timerFired(app):
    app.cx += app.move
    if (app.width in app.edgeX or app.height in app.edgeY or
                                    0 in app.edgeX or 0 in app.edgeY):
        app.move *= -1
        app.cx -= 20
    updateEdge(app)

def redrawAll(app, canvas):
    canvas.create_text(app.width/2, 20,
                       text='Watch the dot move!')
    canvas.create_oval(app.cx-app.r, app.cy-app.r,
                       app.cx+app.r, app.cy+app.r,
                       fill='darkGreen')

runApp(width=400, height=400)