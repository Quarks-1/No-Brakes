##########################################
# Leaderboard
##########################################


def leaderboard_keyPressed(app, event):
    pass

def leaderboard_timerFired(app):
    pass

def drawNames(app, canvas):
    leaderboardData = open("leaderboardData.txt", 'r')
    listedData = leaderboardData.read()
    listedData = listedData.split(',')
    print(listedData)
    sortedData = []
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
    # for data in sortedData:
    #     split = data.split(',')
    #     name = split[0]
    #     speed = split[1]
    #     yPos = 150 + counter*100
    #     canvas.create_rectangle(0, yPos-50, app.width, yPos+50, fill = 'whitesmoke')
    #     canvas.create_text(app.width/5, yPos, text = name,
    #                         font = 'Arial 40 bold')
    #     canvas.create_text(app.width*(4/5), yPos, text = speed,
    #                         font = 'Arial 40 bold')
    #     counter += 1
    #     if counter > 6:
    #         break
    


def leaderboard_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'silver')
    drawNames(app, canvas)