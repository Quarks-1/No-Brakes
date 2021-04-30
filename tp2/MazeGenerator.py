import math, time, random

def getSurroundingCells(app, row, col):
    count = 0
    for (drow, dcol) in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
        newRow, newCol = row + drow, col + dcol
        if app.map[newRow][newCol] == 'c':
            count += 1
    return count


def createMap(app):
    rows = app.height//100
    cols = app.width//100
    app.map = [['u' for i in range(cols)] for j in range(rows)]
    startRow, startCol = 1, 1
    app.map[startRow][startCol] = 'c'
    walls = []
    illegalVals = [0, rows-1, cols-1]
    # Create first set of walls
    for (drow, dcol) in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
        newRow, newCol = startRow + drow, startCol + dcol
        walls.append((newRow, newCol))
        app.map[newRow][newCol] = 'w'
    # Connect walls and paths
    while len(walls) != 0:
        # Select random wall
        (wallRow, wallCol) = random.choice(walls)
        # Make sure it's in the map
        if 0 < wallRow < rows-1 and 0 < wallCol < cols-1:
            # Proceed to check which type of wall it is, then add as corridor
            # and update new surrounding walls
            # Right wall
            if (app.map[wallRow][wallCol-1] == 'c' and 
                app.map[wallRow][wallCol+1] == 'u'):
                sCells = getSurroundingCells(app, wallRow, wallCol)
                if sCells < 2:
                    app.map[wallRow][wallCol] = 'c'
                    for (drow, dcol) in [(0, 1), (-1, 0), (1, 0)]:
                        newRow, newCol = wallRow + drow, wallCol + dcol
                        if (wallCol != cols-1 or wallRow != rows-1 or 
                            wallRow !=0):
                            if app.map[newRow][newCol] != 'c':
                                app.map[newRow][newCol] == 'w'
                            if (newRow, newCol) not in walls:
                                walls.append((newRow, newCol))
                walls.remove((wallRow, wallCol))
                continue
            # Bottom wall
            if (app.map[wallRow-1][wallCol] == 'c' and 
                app.map[wallRow+1][wallCol] == 'u'):
                sCells = getSurroundingCells(app, wallRow, wallCol)
                if sCells < 2:
                    app.map[wallRow][wallCol] = 'c'
                    for (drow, dcol) in [(1, 0), (0, -1), (0, 1)]:
                        newRow, newCol = wallRow + drow, wallCol + dcol
                        if (wallRow != rows-1 or wallCol != 0 or 
                            wallCol != cols-1):
                            if app.map[newRow][newCol] != 'c':
                                app.map[newRow][newCol] == 'w'
                            if (newRow, newCol) not in walls:
                                walls.append((newRow, newCol))
                walls.remove((wallRow, wallCol))
                continue
            # Upper wall
            if (app.map[wallRow+1][wallCol] == 'c' and 
                app.map[wallRow-1][wallCol] == 'u'):
                sCells = getSurroundingCells(app, wallRow, wallCol)
                if sCells < 2:
                    app.map[wallRow][wallCol] = 'c'
                    for (drow, dcol) in [(0, 1), (0, -1), (-1, 0)]:
                        newRow, newCol = wallRow + drow, wallCol + dcol
                        if (wallRow!= 0 or wallCol != 0 or wallCol != cols - 1):
                            if app.map[newRow][newCol] != 'c':
                                app.map[newRow][newCol] == 'w'
                            if (newRow, newCol) not in walls:
                                walls.append((newRow, newCol))
                walls.remove((wallRow, wallCol))
                continue
            # Left Wall
            if (app.map[wallRow][wallCol+1] == 'c' and 
                app.map[wallRow][wallCol-1] == 'u'):
                sCells = getSurroundingCells(app, wallRow, wallCol)
                if sCells < 2:
                    app.map[wallRow][wallCol] = 'c'
                    for (drow, dcol) in [(1, 0), (0, -1), (-1, 0)]:
                        newRow, newCol = wallRow + drow, wallCol + dcol
                        if (wallRow != 0 or wallRow != rows-1 or wallCol != 0):
                            if app.map[newRow][newCol] != 'c':
                                app.map[newRow][newCol] == 'w'
                            if (newRow, newCol) not in walls:
                                walls.append((newRow, newCol))
                walls.remove((wallRow, wallCol))
                continue
            walls.remove((wallRow, wallCol))
        else:
            walls.remove((wallRow, wallCol))

    # Add border walls
    for row in range(rows):
        for col in range(cols):
            if app.map[row][col] == 'u':
                app.map[row][col] = 'w'

    # Create start
    for col in range(0, cols):
        if app.map[1][col] == 'c':
            app.map[0][col] = 's'
            break
    # Create finish line
    for col in range(cols-1, 0, -1):
        if app.map[rows-2][col] == 'c':
            app.map[rows-1][col] = 'f'
            break
