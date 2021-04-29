import random, math

def moveAI(app):
    print('dur')
    AIpath = dijkstra(app)
    row, col = AIPath[0]
    app.enemyMoves.append((row, col))
    app.map[row][col] = 'AI'
    if len(app.enemyMoves) > 1:
        prevRow, prevCol = app.enemyMoves[-1]
        app.map[prevRow][prevCol] = 'c'


def getPlayerCell(app):
    row = int(app.cy//100)
    col = int(app.cx//100)
    return row, col

def chooseStart(app):
    isValid = False
    while not isValid:
        row = random.randint(len(app.map)-4, len(app.map)-2)
        col = random.randint(len(app.map[0])-4, len(app.map[0])-2)
        if app.map[row][col] == 'c':
            isValid = True
    return row, col

def surroundingCells(app, L, row, col):
    for (drow, dcol) in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
        newRow, newCol = row + drow, col + dcol
        if app.map[newRow][newCol] == 'c' and (newRow, newCol) not in unvisited:
            L.append((newRow, newCol))

def getDist(row, col, endRow, endCol):
    return abs(endRow-row) + abs(endCol - col)

def dijkstra(app):
    startRow, startCol = chooseStart(app)
    endRow, endCol = getPlayerCell(app)
    h = getDist(startRow, startCol, endRow, endCol)
    path = []
    unvisited = []
    surroundingCells(app, unvisited, startRow, startCol)
    currRow, currCol = startRow, startCol
    while unvisited != []:
        for (row, col) in unvisited:
            currH = getDist(row, col, endRow, endCol)
            if currH < h:
                currRow, currCol = row, col
                h = currH
        path.append((currRow, currCol))
        unvisited = []
        if (currRow, currCol) != (endRow, endCol):
            surroundingCells(app, unvisited, currRow, currCol)
            print('here')
    return path
    print(path)

    
            