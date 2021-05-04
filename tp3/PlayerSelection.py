import math, time, random
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
    if x5 < event.x < x6 and y5 < event.y < y6 and app.selected != '': #Continue button
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