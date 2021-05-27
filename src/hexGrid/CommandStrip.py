'''
Created on May 12, 2021

@author: Liam
'''
from tkinter import Frame, Label, StringVar, Menu, GROOVE, Entry, IntVar, Checkbutton
from tkinter.ttk import Combobox
from util.math import toInt

colorInstr = 'choose a color from the list above or type it,\nif the color is not in the list then it will be transparent'


def twoClick(first='first coordinates, '):
    return 'first click will specify and show the ' + first + 'second click will '


def makeDrawMenu(strip, menu, rect):
        drawComands = Menu(menu, tearoff=0)
        drawComands.add_command(label='Brush', command=lambda:strip.setCommand('Brush',
            'Sets the color of one hex, ' + colorInstr + ', then click a hex'))  # spin, None))
        drawComands.add_command(label='Line', command=lambda:strip.setCommand('Line',
            'Draws a line between two points, ' + colorInstr + ',\n' + twoClick()
             +'draw the line', display='(0, 0)'))  # , dispLabel, None))
        drawComands.add_command(label=rect, command=lambda:strip.setCommand(rect,
            'Draws a parallelogram between two points, ' + colorInstr + ',\n' + twoClick()
             +'draw the parallelogram', display='(0, 0)', check=True))
        drawComands.add_command(label='Circle', command=lambda:strip.setCommand('Circle',
            'Draws a circle around a point, ' + colorInstr + ',\n'
            +'set the radius, and click a hex', entry=True, check=True))
        drawComands.add_command(label='Triangle', command=lambda:strip.setCommand('Triangle',
            '', display = '(0,0)', check = True))
            # 'Changes all matching hexes colors, ' + colorInstr 
            # +'and click a hex'))
        drawComands.add_command(label='Rhombus', command=lambda:strip.setCommand('Rhombus',
            '', display = '(0,0)', check = True))
        drawComands.add_command(label='Fill', command=lambda:strip.setCommand('Fill',
            'Changes matching neighbooring hexes colors, ' + colorInstr 
            +'and click a hex'))
        drawComands.add_command(label='SwapColor', command=lambda:strip.setCommand('SwapColor',
            'Changes all matching hexes colors, ' + colorInstr 
            +'and click a hex'))
        # drawComands.add_command(label='Swap', command=lambda:strip.setDraw('Swap'))#, None, None))
        menu.add_cascade(label='Draw', menu=drawComands)

        
def makeActorMenu(strip, menu):
        actorComands = Menu(menu, tearoff=0)
        actorComands.add_command(label='AddEntity', command=lambda:strip.setCommand('AddEntity',
            'Adds an unnumbered entity to the map, ' + colorInstr + 
            ', then type in a label and click an unoccupied hex', entry=True))
        actorComands.add_command(label='AddGeneric', command=lambda:strip.setCommand('AddGeneric',
            'Adds an numbered entity to the map, ' + colorInstr + 
            ', then type in a label and click an unoccupied hex,'
            +'\n remove all associated entities to reset counting', entry=True))
        actorComands.add_command(label='Move', command=lambda:strip.setCommand('Move',
            'Moves an entity to a new hex, ' + twoClick('the current coordinates of the clicked entity,\n')
            +'move it to an unoccupied hex, clicking a second entity will swap their positions', display='(0, 0)'))
        actorComands.add_command(label='Remove', command=lambda:strip.setCommand('Remove',
            'Removes an entity from the map, click on an entity to remove it'))
        menu.add_cascade(label='Actor', menu=actorComands)


allColors = ['white', 'black',
    # 'lavender',
    'dark slate gray',
    # 'dim gray', 'slate gray',
    'gray', 'navy',
    # 'royal blue',  
    'blue', 'dodger blue', 'deep sky blue',
    # 'sky blue', 
    # 'steel blue', 
    'turquoise', 'cyan',
    # 'aquamarine', 
    'dark green',
    # 'dark olive green',
    # 'dark sea green', 
    # 'sea green', 'medium sea green', 'light sea green', 
    'green',
    # 'spring green',
    'lawn green',
    # 'green yellow',
    'lime green',
    # 'yellow green',
    # 'forest green', 
    # 'khaki', 
    'yellow', 'gold',
    'goldenrod', 'dark goldenrod',
    'indian red', 'saddle brown', 'sandy brown',
    'tan', 'brown',
    # 'salmon', 
    'orange', 'dark orange',
    # 'coral', 
    # 'tomato', 
    'orange red', 'red',
    # 'hot pink', 
    'deep pink',
    # 'pink', 
    'magenta', 'maroon', 'orchid', 'purple' 
    # 'thistle'
    ]


class HexStrip():
    
    def __init__(self, root, font, colorWidth):
        self.font = font
        menu = Menu(root)
        root.config(menu=menu)
        makeDrawMenu(self, menu, 'Parallelogram')
        makeActorMenu(self, menu)
        strip = Frame(root)
        self.com = StringVar(strip, 'Command')
        comm = Label(strip, textvariable=self.com, relief=GROOVE, font=font)
        comm.grid(row=0, column=1)
        self.disp = StringVar(strip, 'Display')
        self.Disp = Label(strip, textvariable=self.disp, relief=GROOVE, font=font)
        self.Disp.grid(row=0, column=2)
        self.colors = Combobox(strip, values=allColors, font=font, width=colorWidth)
        self.colors.grid(row=0, column=3)
        self.entry = Entry(strip, font=font, width=colorWidth // 2)
        self.entry.grid(row=0, column=4)
        self.check = IntVar()
        self.checkBut = Checkbutton(strip, font=font, text="Fill", variable=self.check, relief=GROOVE)
        self.checkBut.grid(row=0, column=5)
        self.instr = StringVar(strip, 'Pick a command from the menu at the top left corner')
        Instr = Label(strip, textvariable=self.instr, relief=GROOVE)
        Instr.grid(row=1, column=0, columnspan=6)
        strip.pack()
        # print('colors', allColors.__len__())
        
    def setCommand(self, command, instr, display='', entry=False, check=False):
        if display == '':
            self.Disp.grid_forget()
        else:
            self.Disp.grid(row=0, column=2)
        if entry == False:
            self.entry.grid_forget()
        else:
            self.entry.grid(row=0, column=4)
        if check == False:
            self.checkBut.grid_forget()
        else:
            self.checkBut.grid(row=0, column=5)
        self.com.set(command)
        self.disp.set(display)
        self.instr.set(instr)
        # print(command)
    
    def getCommand(self):
        return self.com.get()
    
    def getDisplay(self):
        return self.disp.get()
    
    def setDisplay(self, Str):
        self.disp.set(Str)
        
    def getCords(self):
        return eval(self.getDisplay())
    
    def getColor(self):
        color = self.colors.get()
        if color in allColors:
            return color
        return None

    def getEntry(self):
        return self.entry.get()
    
    def getInt(self):
        return toInt(self.getEntry())
    
    def getCheck(self):
        return self.check.get()
