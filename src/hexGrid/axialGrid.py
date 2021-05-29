'''
Created on May 5, 2021

@author: Liam
'''
from util.math import fullRange, roundUp, nonZeroRange, sumRange, even


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
        self.setBounds(width, height)
        self.grid = []
        self.entities = {}
        for q in range(self.W):
            self.grid.append(self.makeRow(q))
            # app = self.grid[q].append
            # for r in range(self.H):
            #     if self.inBounds(q, r, quick=True):
            #         app(self.baseTile(q, r))
            #     else:
            #         app(None)

    def setBounds(self, width, height):
        self.W = width
        self.H = height
        self.min = min(width, height) // 2
        self.max = width + height - self.min - 1
        
    def makeRow(self, q):
        row = []
        app = row.append
        for r in range(self.H):
            app(self.baseTile(q, r))
        return row

    def makeTile(self, q, r):
        if self.getTile(q, r) == None:
            self.grid[q][r] = self.baseTile(q, r)
            
    def helpBounds(self, width, height, left, up, expand):
        w = abs(width)
        h = abs(even(height))
        if expand:
            if up != None:
                h = min(h, w * 2)
            if self.W + w < self.H + h:
                h = self.W + w - self.H
                if h % 2 == 1:
                    h -= 1
        else:
            if self.W - w < 5:
                w = 0
            if self.H - h < 3:
                h = 0
            if up != None:
                h = min(h, w * 2)
            if self.W - w < self.H - h:
                if h < w*2:
                    w = h*2
                #     w = self.H
                else:
                    h = self.H - self.W + w  
                    if h % 2 == 1:
                        h -= 1
        if left == None:
            lw = w // 2
        elif left:
            lw = w
        else:
            lw = 0
        # if up == False:
        #     lw += h // 2
        if up == None:
            uh = h // 2
        elif up:
            uh = h
        else:
            uh = 0
            lw += h // 2
        return (w, h, lw, uh)
    
    def expand(self, width, height, left, up):
        # w = abs(width)
        # h = abs(even(height))
        # if up != None:
        #     h = min(h, w * 2)
        # if self.W + w < self.H + h:
        #     h = self.W + w - self.H
        #     if h % 2 == 1:
        #         h -= 1
        # if (w == 0 and h == 0) or (left != None and up != None):
        #     return
        # oldW, oldH = self.W, self.H
        # left = w < 0
        (w, h, lw, uh) = self.helpBounds(width, height, left, up, True)
        grid = self.grid
        if w != 0:
            oldW = self.W
            check = self.getOutBounds(left)
            # print(check)
            self.setBounds(oldW + w, self.H)
            # if left == None:
            #     lw = w // 2
            # elif left:
            #     lw = w
            # else:
            #     lw = 0
            # if up == False:
            #     lw += h // 2
            for q in range(0, lw):
                grid.insert(q, self.makeRow(q))
            for q in range(oldW + lw, self.W):
                grid.append(self.makeRow(q))
            for (q, r) in check:
                q += lw
                if self.inBounds(q, r, quick=True):
                    self.makeTile(q, r)
        if h != 0:
            # check = self.getOutBounds(up)
            oldH = self.H
            if up is not None:
                check1 = self.getOutBounds(up)
            self.setBounds(self.W, oldH + h)
            # if up == None:
            #     uh = h // 2
            # elif up:
            #     uh = h
            # else:
            #     uh = 0
            for q in range(0, self.W):
                row = grid[q]
                ins = row.insert
                app = row.append
                for r in range (0, uh):
                    ins(r, self.baseTile(q, r))
                for r in range (oldH + uh, self.H):
                    app(self.baseTile(q, r))
            if up is not None:
                # print(grid)
                for (q, r) in check1:
                    r += uh
                    if self.inBounds(q, r, quick=True):
                        self.makeTile(q, r)
                # print(grid)
                for (q, r)in self.getOutBounds(not up):
                    # print(q, r)
                    # r += uh
                    self.deleteTile(q, r)
        self.shiftEntitys((lw, uh))
        
    def shrink(self, width, height, left, up):
        # w = abs(width)
        # h = abs(even(height))
        # if up != None:
        #     h = min(h, w * 2)
        # grid = self.grid
        (w, h, lw, uh) = self.helpBounds(width, height, left, up, False)
        if w != 0:
            oldW = self.W
            # check = self.getOutBounds(left)
            # print(check)
            self.setBounds(oldW - w, self.H)
            # if left == None:
            #     lw = w // 2
            # elif left:
            #     lw = w
            # else:
            #     lw = 0
            # if up == False:
            #     lw += h // 2
            # print(lw)
            self.deleteRow(self.W + lw, oldW)
            self.deleteRow(0, lw)
            # print(self.grid)
            # for q in range(0, lw):
            #     grid.insert(q, self.makeRow(q))
            # for q in range(oldW + lw, self.W):
            #     grid.append(self.makeRow(q))
            for (q, r) in self.getOutBounds(left):
                self.deleteTile(q, r)
                # q += lw
                # if self.inBounds(q, r, quick=True):
                #     self.makeTile(q, r)
        if h != 0:
            # check = self.getOutBounds(up)
            oldH = self.H
            # if up is not None:
            #     check1 = self.getOutBounds(up)
            self.setBounds(self.W, oldH - h)
            # if up == None:
            #     uh = h // 2
            # elif up:
            #     uh = h
            # else:
            #     uh = 0
            for q in range(0, self.W):
                self.deleteCol(q, self.H + uh, oldH)
                self.deleteCol(q, 0, uh)
            
                # row = grid[q]
                # ins = row.insert
                # app = row.append
                # for r in range (0, uh):
                #     ins(r, self.baseTile(q, r))
                # for r in range (oldH + uh, self.H):
                #     app(self.baseTile(q, r))
            
            # if up is not None:
            for (q, r) in self.getOutBounds(up):
                self.deleteTile(q, r)

            #     print(grid)
            #     for (q, r) in check1:
            #         r += uh
            #         if self.inBounds(q, r, quick=True):
            #             self.makeTile(q, r)
            #     print(grid)
            #     for (q, r)in self.getOutBounds(not up):
            #         print(q, r)
            #         # r += uh
            #         self.deleteTile(q, r)
        self.shiftEntitys((-lw, -uh))
    def deleteTile(self, q, r):
        self.grid[q][r] = None
    
    def deleteRow(self, q1, q2):
        del self.grid[q1:q2]
    
    def deleteCol(self, q, r1, r2):
        del self.grid[q][r1:r2]
    # def hexBounds(self, a, quick=False):
    #     (q, r) = a
    #     return self.inBounds(q, r, quick=quick)
    
    def inBounds(self, q, r, quick=False):
        Sum = q + r
        return ((quick or (q >= 0 and r >= 0 and q < self.W and r < self.H)) 
                and Sum >= self.min and Sum < self.max)
        
    def cornBounds(self, Set, indexes=None, quick=False):
        if indexes == None:
            indexes = range(len(Set))
        for i in indexes:
            # (q, r) = Set[i]
            if not self.inBounds(*Set[i], quick=quick):
                return False
        return True
    
    def getOutBounds(self, topLeft):
        if topLeft == None:
            return self.getOutBounds(True) + self.getOutBounds(False)
        if topLeft:
            Min = self.min - 1
            return getFill(0, Min, -Min, 0, 0, Min, Sorted=True)
        w = self.W - 1
        h = self.H - 1
        drop = self.min - 1
        Max = -self.max  # -1
        Min = Max - drop
        # bound = w - drop, w, Min, Max, h - drop, h
        # print(bound)
        return getFill(w - drop, w, Min, Max, h - drop, h, Sorted=True)
    
    def baseTile(self, q, r):
        if self.inBounds(q, r, quick=True):
            return 0  # (q, r)
        return None
    
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
        if self.inBounds(*a) and self.inBounds(*b):
            self.draw(getLine(a, b), tile)
            return True
        return False
            
    def drawParrallagram(self, a, b, tile, fill):
        if self.inBounds(*a) and self.inBounds(*b):
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
        if self.inBounds(*a) and self.inBounds(*b):
            if a == b:
                (q, r) = a
                return self.setTile(q, r, tile)
            corners = triCorners(a, b)
            force = self.cornBounds(corners, indexes=[1, 2])
            if fill:
                self.draw(getTriangle(a, b), tile, force=force)
            else:
                self.draw(getPoly(corners), tile, force=force)
            return True
        return False
    
    def drawRhombus(self, a, b, tile, fill):
        if self.inBounds(*a) and self.inBounds(*b):
            if a == b:
                return self.setTile(*a, tile)
            corners = rhomCorners(a, b)
            force = self.cornBounds(corners, indexes=[1, 3])
            if fill:
                c, d = corners[1::2]
                self.draw(getParrallagram(c, d), tile, force=force)
            else:
                self.draw(getPoly(corners), tile, force=force)
            return True
        return False
    
    def drawCircle(self, center, radius, tile, fill):
        # if radius == 0:
        #     self.setTile(*center, tile)
        force = self.cornBounds(circCorners(center, radius))
        if fill:
            self.draw(getCirc(center, radius), tile, force=force)
        else:
            self.draw(getRing(center, radius), tile, force=force)
    
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
        if self.inBounds(*b):
            self.entities[b] = self.entities[a]
            self.entities.pop(a)
            
    def swap(self, a, b):
        if self.inBounds(*b):
            temp = self.entities[b]
            self.entities[b] = self.entities[a]
            self.entities[a] = temp
    
    def remove(self, e):
        self.entities.pop(e)
    
    def shiftEntitys(self, offset):
        if offset == (0, 0):
            return
        newEnt = {}
        oldEnt = self.entities
        rem = []
        # offset = (q, r)
        bounds = self.inBounds
        for coords in oldEnt:
            ent = oldEnt[coords]
            print(coords, ent)
            newCoords = hexAdd(coords, offset)
            if bounds(*newCoords):
                newEnt[newCoords] = ent
            else: 
                rem.append(coords)
        for e in rem:
            self.remove(e)
        self.entities = newEnt
    # def printCSV(self):
    #     for 

# template = HexGrid(3, 3)
# hexGrid = HexGrid(5, 5)
# hexGrid.drawCircle((2, 2), 1, 1, True)
# print(hexGrid.grid)
# hexGrid.shrink(2, 2, None, None)
# print(hexGrid.grid)
# print(template.grid)
