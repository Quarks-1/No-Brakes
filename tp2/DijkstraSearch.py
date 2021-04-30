import random, math, copy

def moveAI(app):
    AIpath = dijkstra(app)
    # print(AIpath)
    app.rowAI, app.colAI = AIpath[0]
    app.enemyMoves.append((app.rowAI, app.colAI))
    app.map[app.rowAI][app.colAI] = 'AI'
    if len(app.enemyMoves) > 1:
        prevRow, prevCol = app.enemyMoves[-2]
        app.map[prevRow][prevCol] = 'c'


def getPlayerCell(app):
    row = int(app.cy//100)
    col = int(app.cx//100)
    return row, col

def chooseStart(app):
    isValid = False
    while not isValid:
        row = len(app.map)-2
        col = random.randint(1, 4)
        if app.map[row][col] == 'c':
            isValid = True
    return row, col

def surroundingCells(app, P, row, col, visited):
    L = copy.deepcopy(P)
    for (drow, dcol) in [(1, 0), (0, 1), (0, -1), (-1, 0), 
                        (1, 1), (-1, -1), (1, -1), (-1, 1)]:
        newRow, newCol = row + drow, col + dcol
        if app.map[newRow][newCol] == 'c' and (newRow, newCol) not in visited:
            L.append((newRow, newCol))
    # if len(L) == 0:
    #     L.append((-1,0))
    print(L, 'dis L')
    return L

def getDist(row, col, endRow, endCol):
    return (abs(endRow-row)**2 + abs(endCol - col)**2)**(1/2)

def dijkstra(app):
    print('entered')
    startRow, startCol = app.rowAI, app.colAI
    # print(startRow, startCol)
    endRow, endCol = getPlayerCell(app)
    h = getDist(startRow, startCol, endRow, endCol)
    path = []
    unvisited = []
    visited = []
    unvisited = surroundingCells(app, unvisited, startRow, startCol, visited)
    currRow, currCol = startRow, startCol
    while unvisited != []:
        for (row, col) in unvisited:
            currH = getDist(row, col, endRow, endCol)
            visited.append((row, col))
            if currH < h:
                currRow, currCol = row, col
                h = currH
        path.append((currRow, currCol))
        # print(visited, unvisited, 'too', currRow, currCol)
        unvisited = []
        if (currRow, currCol) != (endRow, endCol):
            unvisited = surroundingCells(app, unvisited, currRow, currCol, visited)
            # if set(unvisited).intersection(path):
            #     path.pop()
            #     currRow, currCol = path[-1]
# write simple algorithim to just choose any direction to move
    return path
