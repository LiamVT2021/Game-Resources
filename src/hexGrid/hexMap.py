'''
Created on May 3, 2021

@author: Liam
'''
from tkinter import Tk, Canvas
from tkinter.font import Font
from math import sqrt
from hexGrid.axialGrid import HexGrid, cube_round, axial_to_cube, parrCorners, \
                            circCorners, triCorners, rhomCorners
from hexGrid.CommandStrip import HexStrip
from hexGrid.Actor import Entity, ActorManager


def lineCorners(a, b):
    return [a, b]


def makeHex(canvas, x, y, a, color='white'):
    sq3 = int(sqrt(3) / 2 * a)
    cords = x, y + a, x + sq3, y + a / 2, x + sq3, y - a / 2, x, y - a, x - sq3, y - a / 2, x - sq3, y + a / 2
    inner = canvas.create_polygon(cords, fill=color, tag='inner')
    outer = canvas.create_polygon(cords, outline='black', fill='',
                width=1, activewidth=3, tag='outer')
    return (inner, outer)
    # hexagon.bind('<Button>',click(hexagon))

    
def makeCircle(canvas, x, y, r, color, label, font):
    circle = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color)
    text = canvas.create_text(x, y, text=label, font=font)
    return(circle, text)


def moveCircle(canvas, shape, x, y, r):
    (circ, text) = shape
    canvas.coords(circ, x - r, y - r, x + r, y + r)
    canvas.coords(text, x, y)
    # print('moved to')
    # print(x, y)


class HexMap(HexGrid):

    def __init__(self, A, B, hexSize=35,):
        root = Tk()
        self.window = root
        self.window.title("Hex Map V" + version)
        self.font = Font(size=hexSize // 2)
        self.strip = HexStrip(root, self.font, hexSize // 3)
        # print(self.strip.getCommand())
#         if width < 5:
#             width = 5 
#         elif width % 2 == 0:
#             width += 1
#         if height < 5:
#             height = 5 
#         elif height % 2 == 0:
#             height += 1
#         self.X = self.W = width
#         self.Y = self.H = height
#         self.X = width-(height-1)//2
        self.S = hexSize
        self.WS = int(sqrt(3) * (self.S))
        self.HS = 1.5 * (self.S)
        
        if A < 3:
            A = 3
        elif A % 2 == 0:
            A += 1
        if B < 3:
            B = 3
        elif B % 2 == 0:
            B += 1  
        W = max(A, B)
        H = min(A, B)
        Map = Canvas(root, bg="white", height=(H + 1) * self.HS, width=(W + 1) * self.WS)
        self.map = Map
        super().__init__(W, H)
#         self.grid = []
#         self.entities = {}
#         for x in range(self.X):
#             self.grid.append([])
#             app = self.grid[x].append
#             for y in range(self.Y):
#                 if self.inBounds(x, y):
#                     app(self.makeHex(x, y))
#                 else:
#                     app(None)
#         hex1 = makeHex(self.map, 30, 35, self.S)
#         makeHex(self.map, self.WS + 30, 35, self.S)
#         makeHex(self.map, 2 * self.WS + 30, 35, self.S)
#         makeHex(self.map, self.WS / 2 + 30, 35 + self.HS, self.S)
#         makeHex(self.map, 3 / 2 * self.WS + 30, 35 + self.HS, self.S)
#         hex1 = self.makeHex(0, 0)
#         self.makeHex(1, 0)
#         self.makeHex(1, 1)
#         self.makeHex(0, 1)
        Map.tag_raise('outer')
        Map.pack()
        Map.bind('<Button-1>', self.click)
        Map.bind('<Motion>', self.hover)
#         self.map.itemconfig(hex1, fill='blue')
        self.actors = ActorManager()  # ActorWindow(Toplevel(), self.font, hexSize // 2)
        
    def addEntity(self, coords, color, label):
        entity = Entity(color, label)
        self.add(coords, self.makeEntity(coords, entity))
        
    def addGeneric(self, coords, color, label):
        generic = self.actors.addGeneric(color, label)
        self.add(coords, self.makeEntity(coords, generic))
        
    def move(self, a, b):
        get = self.entities.get(a)
        if get != None:
            (shape, _entity) = get
            self.moveCircle(shape, b)
            super().move(a, b)

    def swap(self, a, b):
        A = self.entities.get(a)
        B = self.entities.get(b)
        if A != None and B != None:
            (shapeA, _entityA) = A
            (shapeB, _entityB) = B
            self.moveCircle(shapeA, b)
            self.moveCircle(shapeB, a)
            super().swap(a, b)
            
    def moveCircle(self, shape, coords):
        (X, Y) = self.hexCenter(coords)
        moveCircle(self.map, shape, X, Y, self.S * .6)
    
    def remove(self, e):
        get = self.entities.get(e)
        if get != None:
            (shape, entity) = get
            if entity.isActor():
                self.actors.remove(entity)
            (circ, text) = shape
            self.map.delete(circ, text)
            super().remove(e)
        
    def baseTile(self, x, y):
        return self.makeHex(x, y)
    
    def makeHex(self, x, y, color=None):
        (X, Y) = self.getCenter(x, y)
        if color == None:
            return makeHex(self.map, X, Y, self.S)
        return makeHex(self.map, X, Y, self.S, color)
    
    def hexCenter(self, Hex):
        (x, y) = Hex
        return self.getCenter(x, y)
    
    def getCenter(self, x, y):
        return ((x + 1 + (y - self.min) / 2) * self.WS,
                (y + 1) * self.HS)
        
    def makeEntity(self, coords, entity):
        (X, Y) = self.hexCenter(coords)
        (color, label) = entity.toTuple()
        return (makeCircle(self.map, X, Y, self.S * .6, color, label, self.font), entity)
        
    def getClicked(self, ex, ey):
        py = ey / self.HS - 1
        ap = (ex / self.WS - 1 - (py - self.min) / 2, py)
        # print(ap)
        return cube_round(axial_to_cube(ap), True)

    def start(self):
        self.window.mainloop()
        
    def forceTile(self, x, y, tile):
        (inner, _outer) = self.getTile(x, y)
        self.map.itemconfig(inner, fill=tile)
    
    def getColor(self, x, y, quick=False):
        if self.inBounds(x, y, quick=quick):
            (inner, _outer) = self.getTile(x, y)
            return self.map.itemcget(inner, 'fill')
        return None
    
#     def highlight(self, x, y):
#         (_inner, outer) = self.getHex(x, y)
#         self.map.itemconfig(outer, outline='red', width=2, activewidth=4)
#         self.map.tag_raise(outer)
#
#     def highlightSet(self, Set):
#         for (x, y) in Set:
#             self.highlight(x, y)
#
#     def delight(self):
#         self.map.itemconfig('outer', outline='black', width=1, activewidth=3)
# #         self.map.tag_raise('outer')
#
#     def highlightRing(self, x, y, d):
#         self.highlightSet(self.getRing(x, y, d))
        
    def click(self, event):
        # print("clicked: (%s %s)" % (event.x, event.y))
        E = self.getClicked(event.x, event.y)
        if not self.hexBounds(E):
            return
        strip = self.strip
        comm = strip.getCommand()
        clr = strip.getColor()
        write = str(E)
        if comm == 'Brush':
            (x, y) = E
            self.setTile(x, y, clr)
        elif comm == 'Line':
            if self.drawLine(strip.getCords(), E, clr):
                write = '(0, 0)'
        elif comm == 'Parallelogram':
            # A = strip.getCords()
            if self.drawParrallagram(strip.getCords(), E, clr, strip.getCheck()):
                write = '(0, 0)'
            # if not self.hexBounds(A):
            #     strip.setDisplay(str(E))
            # else:#elif self.hexBounds(E):
            #     if strip.getCheck():
            #         self.drawParrallagram(A, E, clr)
            #     else:
            #         self.drawBox(A, E, clr)
            #     strip.setDisplay('(0, 0)')
        elif comm == 'Circle':
            # if self.hexBounds(E):
            # if strip.getCheck():
            self.drawCircle(E, strip.getInt(), clr, strip.getCheck())
            # else:
            #     self.drawRing(E, strip.getInt(), clr)
        elif comm == 'Triangle':
            if self.drawTriangle(strip.getCords(), E, clr, strip.getCheck()):
                write = '(0, 0)'
            # A = strip.getCords()
            # if not self.hexBounds(A):
            #     strip.setDisplay(str(E))
            # else:#elif self.hexBounds(E):
                # if strip.getCheck():
                #     self.drawParrallagram(A, E, clr)
                # else:
                #     self.drawBox(A, E, clr)
                # strip.setDisplay('(0, 0)')
        elif comm == 'Rhombus':
            if self.drawRhombus(strip.getCords(), E, clr, strip.getCheck()):
                write = '(0, 0)'
        elif comm == 'Fill':
            # if self.hexBounds(E):
            self.fill(E, clr)
        elif comm == 'SwapColor':
            (x, y) = E
            old = self.getColor(x, y)
            if old != None:
                self.swapColor(old, clr)
        elif comm == 'AddEntity':
            if self.entities.get(E) == None:
                self.addEntity(E, clr, strip.getEntry())
        elif comm == 'AddGeneric':
            if self.entities.get(E) == None:
                self.addGeneric(E, clr, strip.getEntry())
        elif comm == 'Move':
            A = strip.getCords()
            if not self.hexBounds(A):
                if self.entities.get(E) == None:
                    return  # strip.setDisplay(str(E))
            else:  # elif self.hexBounds(E):
                if A == E:
                    pass
                elif self.entities.get(E) == None:
                    self.move(A, E)
                else:
                    self.swap(A, E)
                write = '(0, 0)'
        elif comm == 'Remove':
            self.remove(E)
        strip.setDisplay(write)

    def pathCoords(self, hexList):
        coords = []
        for Hex in hexList:
            coords.extend(self.hexCenter(Hex))
        return coords
        
    def hover(self, event):
        E = self.getClicked(event.x, event.y)
        if not self.hexBounds(E):
            self.map.delete('hover')
            return
        strip = self.strip
        comm = strip.getCommand()
        if comm == 'Line':
            self.makeHover(strip.getCords(), E, lineCorners)
            # A = strip.getCords()
            # if self.hexBounds(A):  # and self.hexBounds(E):
            #     coords = self.pathCoords([A, E])
            #     self.map.delete('hover')
            #     self.map.create_line(coords, width=2, tags='hover')
            # else:
            #     self.map.delete('hover')
        if comm == 'Parallelogram':
            self.makeHover(strip.getCords(), E, parrCorners)
            # A = strip.getCords()
            # if self.hexBounds(A):  # and self.hexBounds(E):
            #     corners = parrCorners(A, E)
            #     coords = self.pathCoords(corners)
            #     self.map.delete('hover')
            #     if len(corners) == 2:
            #         self.map.create_line(coords, width=2, tags='hover')
            #     else:
            #         self.map.create_polygon(coords, fill='', outline='black', width=2, tags='hover')
            # else:
            #     self.map.delete('hover')
        if comm == 'Circle':
            self.makeHover(E, strip.getInt(), circCorners)
            # if self.hexBounds(E):
            # radius = strip.getInt()
            # corners = circCorners(E, radius)
            # coords = self.pathCoords(corners)
            # self.map.delete('hover')
            # if radius > 0:
            #     self.map.create_polygon(coords, fill='', outline='black', width=2, tags='hover')
            # else:
            #     self.map.delete('hover')
        if comm == 'Triangle':
            self.makeHover(strip.getCords(), E, triCorners)
            # A = strip.getCords()
            # if self.hexBounds(A):  # and self.hexBounds(E):
            #     corners = triCorners(A, E)
            #     coords = self.pathCoords(corners)
            #     self.map.delete('hover')
            #     self.map.create_polygon(coords, fill='', outline='black', width=2, tags='hover')
            # else:
            #     self.map.delete('hover')
        if comm == 'Rhombus':
            self.makeHover(strip.getCords(), E, rhomCorners)
            # A = strip.getCords()
            # if self.hexBounds(A):  # and self.hexBounds(E):
            #     corners = rhomCorners(A, E)
            #     coords = self.pathCoords(corners)
            #     self.map.delete('hover')
            #     self.map.create_polygon(coords, fill='', outline='black', width=2, tags='hover')
            # else:
            #     self.map.delete('hover')
                
    def makeHover(self, a, b, cornMethod):
            if self.hexBounds(a):  # and self.hexBounds(E):
                corners = cornMethod(a, b)
                coords = self.pathCoords(corners)                    
                self.map.delete('hover')
                if len(corners) == 2:
                    self.map.create_line(coords, width=2, tags='hover')
                else:
                    self.map.create_polygon(coords, fill='', outline='black',
                                             width=2, tags='hover')
            else:
                self.map.delete('hover')

                    
version = '1.2'
map2 = HexMap(9, 15)
map2.start()
