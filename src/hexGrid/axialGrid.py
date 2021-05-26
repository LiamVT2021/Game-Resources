'''
Created on May 5, 2021

@author: Liam
'''
from util.math import fullRange, roundUp, nonZeroRange


def cube_to_axial(cube):
    (x, _y, z) = cube
    return (x, z)


def axial_to_cube(axial):
    (x, z) = axial
    return (x, -x - z, z)


def hexAdd(a, b):
    (ax, az) = a
    (bx, bz) = b
    return (ax + bx, az + bz)


def hexSub(b, a):
    (ax, az) = a
    (bx, bz) = b
    return (bx - ax, bz - az)


def hexScale(a, d):
    (x, z) = a
    return (d * x, d * z)


def clockwise(a):
    (x, z) = a
    return (-z, x + z)


def counterClockwise(a):
    (x, z) = a
    return (x + z, -x)


axial_directions = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]


def neighbors(axial):
    (q, r) = axial
    neighbors = []
    for (i, j) in axial_directions:
        neighbors.append((q + i, r + j))
    return neighbors


def hexDist(a, b):
    (aq, ar) = a
    (bq, br) = b
    dq = aq - bq
    dr = ar - br
    return (abs(dq) + abs(dq + dr) + abs(dr)) // 2


def quickDist(d):
    (q, r) = d
    return (abs(q) + abs(q + r) + abs(r)) // 2

          
def lerp(a, b, t):  # for floats
    return a + (b - a) * t


def cube_lerp(ax, ay, az, bx, by, bz, t):  # for hexes
#     (ax,ay,az) = a
#     (bx,by,bz) = b
    return (lerp(ax, bx, t),
            lerp(ay, by, t),
            lerp(az, bz, t))


def cube_round(cube, ax=False):
    (x, y, z) = cube
    # print(cube)
    rx = roundUp(x)
    ry = roundUp(y)
    rz = roundUp(z)
    dx = abs(rx - x)
    dy = abs(ry - y)
    dz = abs(rz - z)
    # print(dx,dy,dz)
    if dx > dy and dx > dz:
        rx = -ry - rz
    elif dy > dz:
        ry = -rx - rz
    else:
        rz = -rx - ry
#     if dy >= dx and dy >= dz:
#         ry = -rx - rz
#     elif dx >= dz:
#         rx = -ry - rz
#     else:
#         rz = -rx - ry
    # print(rx,ry,rz)
    if ax:
        return (rx, rz)
    return (rx, ry, rz)


def triRound(axial):
    (x, z) = axial
    if x == 0 or z == 0 or z == -x:
        return axial
    y = -x - z
    dx = abs(x)
    dy = abs(y)
    dz = abs(z)
    if dx > dy and dx > dz:
        return (x, -x)
    elif dy > dz:
        return (-y, 0)
    else:
        return (0, z)


def getLine(a, b):
    N = hexDist(a, b)
    (ax, ay, az) = axial_to_cube(a)
    (bx, by, bz) = axial_to_cube(b)
    if ax == bx or ay == by or az == bz:
        return quickLine(a, b)
    line = []
    for i in range(N + 1):
        line.append(cube_round(cube_lerp(ax, ay, az, bx, by, bz,
                    1 / N * i), ax=True))
    # print(line)
    return line


def getCircCorners(center, radius):
    corners = []
    for Dir in axial_directions:
        corners.append(hexAdd(center, hexScale(Dir, radius)))
    return corners


def getCirc(center, radius):
    if radius <= 0:
        return [center]
    (cq, cr) = center
    circ = []
    for q in range(-radius, radius + 1):
        for r in range(max(-radius, -q - radius), min(radius, -q + radius) + 1):
#         var z = -x-y
            circ.append((cq + q, cr + r))
    return circ


def getRing(center, radius):
    if radius <= 0:
        return [center]
    ring = []
    cur = hexAdd(center, hexScale(axial_directions[4], radius))
    for i in range(6):
        Dir = axial_directions[i]
        for _j in range(radius):
            ring.append(cur)
            cur = hexAdd(cur, Dir)
    return ring


def getParrallagram(a, b):
    parr = []
    (q, r) = a
    (dx, dy, dz) = axial_to_cube(hexSub(b, a))
    if abs(dy) >= abs(dx) and abs(dy) >= abs(dz):
        for x in fullRange(0, dx):
            for z in fullRange(0, dz):
                parr.append((q + x, r + z))
    elif abs(dz) >= abs(dx):
        for x in fullRange(0, dx):
            for y in fullRange(0, dy):
                parr.append((q + x, r - x - y))
    else:
        for y in fullRange(0, dy):
            for z in fullRange(0, dz):
                parr.append((q - y - z, r + z))
    print(parr)
    return parr


def getParrCorners(a, b):
    (dx, dy, dz) = axial_to_cube(hexSub(b, a))
    if dx == 0 or dy == 0 or dz == 0:
        return [a, b]
    (q, r) = a
    if abs(dy) >= abs(dx) and abs(dy) >= abs(dz):
        return [a, (q + dx, r), b, (q, r + dz)]
    elif abs(dx) >= abs(dz):
        return [a, (q - dy, r), b, (q - dz, r + dz)]
    else:
        return [a, (q, r - dy), b, (q + dx, r - dx)]
    
    
def quickLine(a, b, source=True):
    (dx, dz) = hexSub(b, a)
    (q, r) = a
    line = []
    if dx == 0:
        if source:
            Range = fullRange(0, dz)
        else:
            Range = nonZeroRange(dz)
        for i in Range:
            line.append((q, r + i))
    else: 
        if source:
            Range = fullRange(0, dx)
        else:
            Range = nonZeroRange(dx)
        if dz == 0:
            for i in Range:
                line.append((q + i, r))
        else:
            for i in Range:
                line.append((q + i, r - i))
    return line

    
def getBox(a, b):
    if a == b:
        return [a]
    corners = getParrCorners(a, b)
    if len(corners) == 2:
        return quickLine(a, b)
    box = []
    for i in range(4):
        line = quickLine(corners[i], corners[(i + 1) % 4], source=False)
        box.extend(line)
    return box


def getPoly(corners):
    l = len(corners)
    if l == 2:
        return quickLine(corners[0], corners[1])
    poly = []
    for i in range(l):
        line = quickLine(corners[i - 1], corners[i], source=False)
        poly.extend(line)
    return poly


def getPolygram(a, b, corMethod):
    if a == b:
        return [a]
    return getPoly(corMethod(a, b))


def getTriCorners(a, b):
    corners = [a]
    d = triRound(hexSub(b, a))
    corners.append(hexAdd(a, d))
    corners.append(hexAdd(a, clockwise(d)))
    return corners


class HexGrid:
    
    def __init__(self, width, height):
        self.W = width
        self.H = height
        self.min = min(width, height) // 2
        self.max = width + height - self.min - 1
        self.grid = []
        self.entities = {}
        for q in range(self.W):
            self.grid.append([])
            app = self.grid[q].append
            for r in range(self.H):
                if self.inBounds(q, r, quick=True):
                    app(self.baseTile(q, r))
                else:
                    app(None)
    
    def hexBounds(self, a, quick=False):
        (q, r) = a
        return self.inBounds(q, r, quick=quick)
    
    def inBounds(self, q, r, quick=False):
        Sum = q + r
        return ((quick or (q >= 0 and r >= 0 and q < self.W and r < self.H)) 
                and Sum >= self.min and Sum < self.max)
    
    def baseTile(self, q, r):
        return 0  # (q, r)
    
    def setTile(self, q, r, tile):
        if self.inBounds(q, r):
            self.forceTile(q, r, tile)
            
    def forceTile(self, q, r, tile):
        self.grid[q][r] = tile
    
    # def forceHex(self, a, tile):
    #     (q,r) = a
    #     self.forceTile(q, r, tile)
    
    def getTile(self, q, r):
        return self.grid[q][r]
    
    # def getHex(self, a):
    #     (q,r) = a
    #     return self.getTile(q, r)
    
    def draw(self, Set, tile, force=True):
        if force:
            draw = self.forceTile
        else:
            draw = self.setTile
        for (q, r) in Set:
            draw(q, r, tile)
            
    def drawLine(self, a, b, tile):
        if self.hexBounds(a) and self.hexBounds(b):
            self.draw(getLine(a, b), tile)
            return True
        return False
            
    def drawParrallagram(self, a, b, tile, fill):
        if self.hexBounds(a) and self.hexBounds(b):
            if fill:
                self.draw(getParrallagram(a, b), tile)
            else:
                self.draw(getBox(a, b), tile)
            return True
        return False
    # def drawBox(self, a, b, tile):
    #     if self.hexBounds(a) and self.hexBounds(b):
    #         self.draw(getBox(a, b), tile)
    
    def drawCircle(self, center, radius, tile, fill):
        if fill:
            self.draw(getCirc(center, radius), tile, force=False)
        else:
            self.draw(getRing(center, radius), tile, force=False)
    
    # def drawRing(self, center, radius, tile):
    #     self.draw(getRing(center, radius), tile, force=False)
        
    def getColor(self, q, r, quick=False):
        if self.inBounds(q, r, quick):
            return self.getTile(q, r)
        return None
    
    def fill(self, a, tile):
        getClr = self.getColor
        (x, y) = a
        old = getClr(x, y)
        Next = [a]
        while Next:
            cur = Next.pop(0)
            (x, y) = cur
            if getClr(x, y) == old:
                Next.extend(neighbors(cur))
                self.forceTile(x, y, tile)
            
    def swapColor(self, old, new):
        getClr = self.getColor
        for q in range(self.W):
            for r in range(self.H):
                if getClr(q, r, quick=True) == old:
                    self.forceTile(q, r, new)
        
    def add(self, coords, entity):
        self.entities[coords] = entity
        
    def move(self, a, b):
        if self.hexBounds(b):
            self.entities[b] = self.entities[a]
            self.entities.pop(a)
            
    def swap(self, a, b):
        if self.hexBounds(b):
            temp = self.entities[b]
            self.entities[b] = self.entities[a]
            self.entities[a] = temp
    
    def remove(self, e):
        self.entities.pop(e)

# print(getCirc((0, 0), 1))
# print(getRing((0, 0), 2))
# hexGrid = HexGrid(5, 5)
# # hexGrid.drawLine((2,0), (4,2), tile)
# print(hexGrid.grid)
