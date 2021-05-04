##########################################
# Leaderboard
##########################################

def leaderboard_keyPressed(app, event):
    if event.key == 'Escape':
        app.mode = 'startScreen'

def drawNames(app, canvas):
    leaderboardData = open("leaderboardData.txt", 'r')
    prev = leaderboardData.read()
    listedData = prev
    listedData = listedData.split(',')
    if len(listedData)//2 != 0:
        listedData.pop()
    sortedData = []
    # Sort leaderboard
    while len(listedData) != len(sortedData):
        bestScore = 0
        bestName = ''    
        for spot in range(0, len(listedData), 2):
            currNum = listedData[spot+1]
            currName = listedData[spot]
            currNum = int(currNum)
            if currNum > bestScore and currName not in sortedData:
                bestScore = currNum
                bestName = listedData[spot]
        sortedData.append(bestName)
        sortedData.append(bestScore)
    print(sortedData)
    counter = 0
    # Draw sorted leaderboard
    for data in range(0, len(sortedData), 2):
        name = sortedData[data]
        speed = sortedData[data+1]
        if name == '':
            continue
        yPos = 150 + counter*100
        canvas.create_rectangle(0, yPos-50, app.width, yPos+50, fill = 'whitesmoke')
        canvas.create_text(app.width/5, yPos, text = name,
                            font = 'Arial 40 bold')
        canvas.create_text(app.width*(4/5), yPos, text = f'{speed}  mph',
                            font = 'Arial 40 bold')
        counter += 1
        if counter > 6:
            break

def leaderboard_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'silver')
    canvas.create_text(app.width/2, 50, text = 'Leaderboard',
                        font = 'Arial 50 bold')
    canvas.create_text(app.width/5, 50, text = 'Player',
                        font = 'Arial 40 bold')
    canvas.create_text(app.width*(4/5), 50, text = 'Speed',
                        font = 'Arial 40 bold')
    drawNames(app, canvas)
    canvas.create_text(app.width/2, app.height-50, text = 'Press escape to return home',
                        font = 'Arial 35 bold')