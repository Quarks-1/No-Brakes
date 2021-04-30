import random, copy, math

def DFS(app):
    endRow, endCol = getPlayerCell(app)
    startRow, startCol = chooseStart(app)
    visited = set()
    path = helper(app, visited, startRow, startCol, endRow, endCol)
    print(path)

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

def helper(app, visited, startRow, startCol, endRow, endCol): #Check one way trip
    if (startRow, startCol) == (endRow, endCol):
        return True
    else:
        for (drow, dcol) in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
            newRow, newCol = startRow + drow, startCol + dcol
            if (newRow, newCol) in visited:
                return False
            if 0 <= newRow < len(app.map) and 0 <= newCol < len(app.map[0]):
                if app.map[newRow][newCol] == 'c':
                    visited.add((newRow, newCol))
                    solved = helper(app, visited, newRow, newCol, endRow, endCol)
                    if solved == True:
                        return visited
        visited.remove((startRow, startCol))
        return False

'''
[
 [ w, s, w, w, w, w, w, w, w, w, w, w, w, w ]
 [ w, c, c, w, c, w, c, c, w, c, c, w, c, w ]
 [ w, w, c, w, c, c, c, w, c, w, c, c, c, w ]
 [ w, c, c, c, c, w, c, c, c, c, c, w, c, w ]
 [ w, w, c, w, c, c, w, w, c, w, c, w, w, w ]
 [ w, w, c, c, w, c, w, c, c, c, w, c, c, w ]
 [ w, c, c, w, c, c, w, c, w, c, c, c, w, w ]
 [ w, c, w, c, c, w, c, c, c, w, c, w, w, w ]
 [ w, w, w, w, w, w, w, w, w, w, f, w, w, w ]
]

'''