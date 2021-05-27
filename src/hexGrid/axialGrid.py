'''
Created on May 5, 2021

@author: Liam
'''
from util.math import fullRange, roundUp, nonZeroRange, sumRange


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


def dirRound(a, b, unit=True):
    if a == b:
        return (0, 0)
    d = hexSub(b, a)
    l = quickDist(d)
    u = cube_round(axial_to_cube(hexScale(d, 1 / l)), ax=True)
    if unit:
        return u
    return hexScale(u, l)


def triRound(a, b):
    # d = hexSub(b, a)
    # (x, z) = d
    (x, y, z) = axial_to_cube(hexSub(b, a))
    if x == 0 or z == 0 or y == 0:
        return (x, z)
    # y = -x - z
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


def getCirc(center, radius):
    if radius <= 0:
        return [center]
    (x, y, z) = axial_to_cube(center)
    return getFill(x - radius, x + radius, y - radius, y + radius,
                       z - radius, z + radius, Sorted=True)
    # (cq, cr) = center
#     circ = []
#     for q in range(-radius, radius + 1):
#         for r in range(max(-radius, -q - radius), min(radius, -q + radius) + 1):
# #         var z = -x-y
#             circ.append((cq + q, cr + r))
#     return circ


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
    (ax, ay, az) = axial_to_cube(a)
    (bx, by, bz) = axial_to_cube(b)
    return getFill(ax, bx, ay, by, az, bz)
    # (dx, dz) = hexSub(b, a)
    # dy = -dx - dz
    # xRange = fullRange(0, dx)
    # zRange = fullRange(0, dz)
    # yMin = min(0, dy)
    # yMax = max(0, dy)
    # return getFill(a, xRange, zRange, yMin, yMax)
    # parr = []
    # (q, r) = a
    # (dx, dy, dz) = axial_to_cube(hexSub(b, a))
    # if abs(dy) >= abs(dx) and abs(dy) >= abs(dz):
    #     for x in fullRange(0, dx):
    #         for z in fullRange(0, dz):
    #             parr.append((q + x, r + z))
    # elif abs(dz) >= abs(dx):
    #     for x in fullRange(0, dx):
    #         for y in fullRange(0, dy):
    #             parr.append((q + x, r - x - y))
    # else:
    #     for y in fullRange(0, dy):
    #         for z in fullRange(0, dz):
    #             parr.append((q - y - z, r + z))
    # print(parr)
    # return parr

    
def getTriangle(a, b):
    (ax, ay, az) = axial_to_cube(a)
    # (dx, dy, dz) = axial_to_cube(hexAdd(a, triRound(a, b)))
    (dx, dy, dz) = axial_to_cube(triRound(a, b))
    if dx == 0:
        # xRange = fullRange(0, dy)
        bx = ax + dy
    else:
        # xRange = fullRange(0, dx)
        bx = ax + dx
    if dz == 0:
        # zRange = fullRange(0, dx)
        bz = az + dx
    else:
        # zRange = fullRange(0, dz)
        bz = az + dz
    if dy == 0:
    #     dy = dz
        by = ay + dz
    else:
        by = ay + dy
    return getFill(ax, bx, ay, by, az, bz)
    # yMin = min(0, dy)
    # yMax = max(0, dy)
    # return getFill(a, xRange, zRange, yMin, yMax)

    
# def getFill(a, xRange, zRange, yMin, yMax):
#     (q, r) = a
#     fill = []
#     for x in xRange:
#         for z in zRange:
#             y = -x - z
#             if y >= yMin and y <= yMax:
#                 fill.append((q + x, r + z))
#     return fill


def getFill(x1, x2, y1, y2, z1, z2, Sorted=False):
    if Sorted:
        # zMin = z1
        # zMax = z2
        # sMin = -y2
        # sMax = -y1
        xRange = range(x1, x2 + 1)
        zRange = z1, z2, -y2, -y1
    else:
        # zMin = min(z1, z2)
        # zMax = max(z1, z2)
        # sMin = -max(y1, y2)
        # sMax = -min(y1, y2)
        xRange = fullRange(x1, x2)
        zRange = min(z1, z2), max(z1, z2), -max(y1, y2), -min(y1, y2)
        # zRange = zMin,zMax,sMin,sMax
    fill = []
    for x in xRange:
        for z in sumRange(x, *zRange, Sorted=True):
            fill.append((x, z))
    return fill
# def getBox(a, b):
#     if a == b:
#         return [a]
#     corners = getParrCorners(a, b)
#     if len(corners) == 2:
#         return quickLine(a, b)
#     box = []
#     for i in range(4):
#         line = quickLine(corners[i], corners[(i + 1) % 4], source=False)
#         box.extend(line)
#     return box


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


def parrCorners(a, b):
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

    
def triCorners(a, b):
    d = triRound(a, b)
    corners = [a]
    corners.append(hexAdd(a, d))
    corners.append(hexAdd(a, clockwise(d)))
    return corners


def rhomCorners(a, b):
    d = dirRound(a, b, unit=False)
    corners = [a]
    corners.append(hexAdd(a, counterClockwise(d)))
    corners.append(hexAdd(a, d))
    corners.append(hexAdd(a, clockwise(d)))
    return corners
    

def circCorners(center, radius):
    corners = []
    for Dir in axial_directions:
        corners.append(hexAdd(center, hexScale(Dir, radius)))
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
        
    def setBounds(self, Set, indexes=None, quick=False):
        if indexes == None:
            indexes = range(len(Set))
        for i in indexes:
            (q, r) = Set[i]
            if not self.inBounds(q, r, quick=quick):
                return False
        return True
    
    def baseTile(self, q, r):
        return 0  # (q, r)
    
    def setTile(self, q, r, tile):
        if self.inBounds(q, r):
            self.forceTile(q, r, tile)
            return True
        return False
            
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
                self.draw(getPolygram(a, b, parrCorners), tile)
            return True
        return False
    # def drawBox(self, a, b, tile):
    #     if self.hexBounds(a) and self.hexBounds(b):
    #         self.draw(getBox(a, b), tile)
    
    def drawTriangle(self, a, b, tile, fill):
        if self.hexBounds(a) and self.hexBounds(b):
            if a == b:
                (q, r) = a
                return self.setTile(q, r, tile)
            corners = triCorners(a, b)
            force = self.setBounds(corners, indexes=[1, 2])
            if fill:
                self.draw(getTriangle(a, b), tile, force=force)
            else:
                self.draw(getPoly(corners), tile, force=force)
            return True
        return False
    
    def drawRhombus(self, a, b, tile, fill):
        if self.hexBounds(a) and self.hexBounds(b):
            if a == b:
                (q, r) = a
                return self.setTile(q, r, tile)
            corners = rhomCorners(a, b)
            force = self.setBounds(corners, indexes=[1, 3])
            if fill:
                c, d = corners[1::2]
                self.draw(getParrallagram(c, d), tile, force=force)
            else:
                self.draw(getPoly(corners), tile, force=force)
            return True
        return False
    
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
