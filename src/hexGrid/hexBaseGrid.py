'''
Created on Mar 23, 2021

@author: Liam
'''
from util.math import fullRange


def hexDist(x, y):
    if x * y <= 0:
        return abs(x - y)
    else:
        return max(abs(x), abs(y))

    
def neighbors(x, y, d=1):
    return [(x + d, y), (x + d, y + d), (x, y + d), (x - d, y), (x - d, y - d), (x, y - d)]


# def unit(u):
#     if u = "x": return (1,0,0)
#     if u
def xyz(x, y):
#     if x == 0 or y == 0:
#         return (x,y,0)
#     if y == x:
#         return (0,0,-x)
    if x >= 0:
        if y <= 0:
            return (x, y, 0)
        elif y <= x:
            return (x - y, 0, -y)
        else:  # if y>x:
            return (0, y - x, -x)
    else:
        if y >= 0:
            return (x, y, 0)
        elif y >= x:
            return (x - y, 0, -y)
        else:  # if y<x:
            return (0, y - x, -x)

        
def zig(x, y, z=None):
    if z == None:
        (x, y, z) = xyz(x, y)
    if x == 0:
        return abs(y) - abs(z)
    if y == 0:
        return abs(x) - abs(z)
    if z == 0:
        return abs(x) - abs(y)


def directions(x, y):
    if x == y == 0:
        return "0"
    if x == y:
        return str(-x) + "z"
    if x == 0:
        return str(x) + "x"
    if y == 0:
        return str(y) + "y"
    if x > 0:
        if y < 0:
            return str(x) + "x" + str(y) + "y"
        if y < x:
            return str(x - y) + "x" + str(-y) + "z"
        if y > x:
            return str(y - x) + "y" + str(-x) + "z"
    else:
        if y > 0:
            return str(y) + "y" + str(x) + "x"
        if y > x:
            return str(-y) + "z" + str(x - y) + "x"
        if y < x:
            return str(-x) + "z" + str(y - x) + "y"


def parrallagram(x1, y1, x2, y2):
    (x, y, z) = xyz(x2 - x1, y2 - y1)
#     print(x,y,z)
    out = []
    if x == 0:
        for i in fullRange(0, y):
            for j in fullRange(0, z):
                out.append((x1 - j, y1 + i - j))
#         if y < 0:
#             for i in range(-y + 1):
#                 for j in range (z + 1):
#                     out.append((x1 - j, y1 - i - j))
#         else:
#             for i in range(y + 1):
#                 for j in range (-z + 1):
#                     out.append((x1 + j, y1 + i + j))
                
    elif y == 0:
        for i in fullRange(0, x):
            for j in fullRange(0, z):
                out.append((x1 + i - j, y1 - j))
#         if x < 0:
#             for i in range(-x + 1):
#                 for j in range (z + 1):
#                     out.append((x1 - i - j, y1 - j))
#         else:
#             for i in range(x + 1):
#                 for j in range (-z + 1):
#                     out.append((x1 + j, y1 + i + j))
                
    else:
        for i in fullRange(0, x):
            for j in fullRange(0, y):
                out.append((x1 + i, y1 + j))
#         if x < 0:
#             for i in range(-x + 1):
#                 for j in range (y + 1):
#                     out.append((x1 - i, y1 + j))
#         else:
#             for i in range(x + 1):
#                 for j in range (-y + 1):
#                     out.append((x1 + i, y1 - j))
    return out




def line(x1, y1, x2, y2):
    line = []
    # straight lines
    if x1 == x2:
        for y in fullRange(y1, y2):
            line.append((x1, y))
    elif y1 == y2:
        for x in fullRange(x1, x2):
            line.append((x, y1))
    elif y1 - x1 == y2 - x2:
        o = y1 - x1
        for x in fullRange(x1, x2):
            line.append((x, x + o))
    else:
        (x, y, z) = xyz(x2 - x1, y2 - y1)
        if x == 0:
            Zig = abs(y) - abs(z)
            if Zig == 1:
                pass
                    
#         Zig = zig(x, y, z)
#         if -1<=Zig<=1:
#             pass
    return line
#     if x1 == x2:
#         
#     (x,y,z) = xyz(x2-x1,y2-y1)
#     u = max(abs(x),abs(y),abs(z))
#     if abs(x) == u:
#         if 
            
    
class HexGrid:

    def __init__(self, size, span, baseTile=0):
        self.Y = 2 * size + 1
        self.X = self.Y + span
        self.grid = []
        self.entities = {}
        for x in range(self.X):
            self.grid.append([])
            app = self.grid[x].append
            for y in range(self.Y):
                if self.inBounds(x, y):
                    app(baseTile)
                else:
                    app(None)
                
    def setPos(self, e, x, y):
        if self.inBounds(x, y):
            self.entities[e] = (x, y)
    
    def remove(self, e):
        self.entities.pop(e)
    
    def inBounds(self, x, y):
        if x < 0 or y < 0 or y >= self.Y or x >= self.X or x - y >= self.X - self.Y / 2 or y - x >= self.Y / 2:
            return False
        return True
    
    def setTile(self, x, y, tile):
        if self.inBounds(x, y):
            self.forceTile(x, y, tile)
            
    def forceTile(self, x, y, tile):
            self.grid[x][y] = tile
            
    def draw(self, Set, tile):
        for (x, y) in Set:
            self.forceTile(x, y, tile)
    
    def drawParrallagram(self, x1, y1, x2, y2, tile):
        if self.inBounds(x1, y1) and self.inBounds(x2, y2):
            self.draw(parrallagram(x1, y1, x2, y2), tile)
                
    def getCirc(self, x, y, d):
        circ = []
        for i in range(self.X):
            for j in range(self.Y):
                if hexDist(i - x, j - y) <= d and self.inBounds(x, y):
                    circ.append((i, j))
        return circ
    
    def getRing(self, x, y, d):
        pass
    
    def drawRing(self, x, y, d, tile):
        self.draw(self.getRing(x, y, d), tile)
        
    def drawLine(self, x1, y1, x2, y2, tile):
        self.draw(line(x1, y1, x2, y2), tile)
            
#     def dist(self, x1, y1, x2, y2):
#         return self.dist(x2 - x1, y2 - y1)


# hexG = HexGrid(3, 2)
# print(hexG.grid)
# print(directions(7,9))
# print(parrallagram(0, 4, 1, 0))
print(line(0, 3, 0, 0))
print(line(3, 0, 0, 0))
print(line(0, 3, 0, 3))
print(line(0, 0, 3, 3))
