import math, time, random

##########################################
# Start Screen  Mode
##########################################

def startScreen_mouseMoved(app, event):
    x1, y1 = app.sb1x - app.sbrx, app.sb1y - app.sbry
    x2, y2 = app.sb1x + app.sbrx, app.sb1y + app.sbry
    x3, y3 = app.sb2x - app.sbrx, app.sb2y - app.sbry
    x4, y4 = app.sb2x + app.sbrx, app.sb2y + app.sbry
    x5, y5 = app.sb3x - app.sbrx, app.sb3y - app.sbry
    x6, y6 = app.sb3x + app.sbrx, app.sb3y + app.sbry
    if x1 < event.x < x2 and y1 < event.y < y2: #Play button
        app.sHovering = 'play'
    elif x3 < event.x < x4 and y3 < event.y < y4: #Leaderboard button
        app.sHovering = 'leaderboard'
    elif x5 < event.x < x6 and y5 < event.y < y6: #Quit button
        app.sHovering = 'quit'
    else:
        app.sHovering = ''
        app.sHoverWidth1, app.sHoverWidth2, app.sHoverWidth3 = 1, 1, 1



def startScreen_mousePressed(app, event):
    x1, y1 = app.sb1x - app.sbrx, app.sb1y - app.sbry
    x2, y2 = app.sb1x + app.sbrx, app.sb1y + app.sbry
    x3, y3 = app.sb2x - app.sbrx, app.sb2y - app.sbry
    x4, y4 = app.sb2x + app.sbrx, app.sb2y + app.sbry
    x5, y5 = app.sb3x - app.sbrx, app.sb3y - app.sbry
    x6, y6 = app.sb3x + app.sbrx, app.sb3y + app.sbry
    if x1 < event.x < x2 and y1 < event.y < y2: #Play button
        app.mode = 'playerSelect'
    if x3 < event.x < x4 and y3 < event.y < y4: #Leaderboard button
        app.mode = 'leaderboard'
    if x5 < event.x < x6 and y5 < event.y < y6: #Quit button
        app.mode = 'quit'

def startScreen_timerFired(app):
    if app.sHovering == 'play':
        if 0 <= app.sHoverWidth1 <= 6:
            app.sHoverWidth1 += 0.25
        else:
            app.sHoverWidth1 = 1
    if app.sHovering == 'leaderboard':
        if 0 <= app.sHoverWidth2 <= 6:
            app.sHoverWidth2 += 0.25
        else:
            app.sHoverWidth2 = 1
    if app.sHovering == 'quit':
        if 0 <= app.sHoverWidth3 <= 6:
            app.sHoverWidth3 += 0.25
        else:
            app.sHoverWidth3 = 1
    if app.startSpritey > app.height - 40 or app.startSpritey < 40:
        app.incr *= -1
    app.startSpritey += app.incr
    


def drawStartButtons(app, canvas):
    x1, y1 = app.sb1x - app.sbrx, app.sb1y - app.sbry
    x2, y2 = app.sb1x + app.sbrx, app.sb1y + app.sbry
    x3, y3 = app.sb2x - app.sbrx, app.sb2y - app.sbry
    x4, y4 = app.sb2x + app.sbrx, app.sb2y + app.sbry
    x5, y5 = app.sb3x - app.sbrx, app.sb3y - app.sbry
    x6, y6 = app.sb3x + app.sbrx, app.sb3y + app.sbry
    font = 'Comic 45'
    canvas.create_rectangle(x1, y1, x2, y2, fill = 'lightgreen',
                            width = app.sHoverWidth1)
    canvas.create_text(app.sb1x, app.sb1y, fill = 'whitesmoke',
                    text = 'Play', font = font)
    canvas.create_rectangle(x3, y3, x4, y4, fill = 'royalblue',
                            width = app.sHoverWidth2)
    canvas.create_text(app.sb2x, app.sb2y, fill = 'whitesmoke',
                    text = 'Leaderboard', font = font)
    canvas.create_rectangle(x5, y5, x6, y6, fill = 'darkred',
                            width = app.sHoverWidth3)
    canvas.create_text(app.sb3x, app.sb3y, fill = 'whitesmoke',
                    text = 'Quit', font = font)

def drawStartPlayers(app, canvas):
    xr = 20
    yr = 40
    cr = 30
    x1, y1 = app.startSpritex1 - xr, app.startSpritey - yr
    x2, y2 = app.startSpritex1 + xr, app.startSpritey + yr
    x3, y3 = app.startSpritex2 - cr, abs(app.height-app.startSpritey) - cr
    x4, y4 = app.startSpritex2 + cr, abs(app.height-app.startSpritey) + cr
    canvas.create_rectangle(x1, y1, x2, y2, fill = 'orangered', width = 2)
    canvas.create_oval(x3, y3, x4, y4, fill = 'aqua', width = 2)


def startScreen_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'grey')
    canvas.create_text(app.width/2, 150, font = 'Comic 75',
                        text = '🚀No Brakes!🚀', fill = 'snow')
    drawStartButtons(app, canvas)
    drawStartPlayers(app, canvas)