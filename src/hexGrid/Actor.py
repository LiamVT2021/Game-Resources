'''
Created on May 14, 2021

@author: Liam
'''
from tkinter import Label, GROOVE, Entry
from tkinter.ttk import Combobox


class Entity:
    
    def __init__(self, color, label):
        self.color = color
        self.label = label
    
    def getColor(self):
        return self.color
        
    def getLabel(self):
        return self.label
        
    def toTuple(self):
        return (self.color, self.getLabel())
    
    def toKey(self):
        return (self.color, self.label)
    

class Template:

    def __init__(self, group, name, maxHp, AC, initative, reach=1, movement=6):
        self.group = group
        self.name = name
        self.maxHp = maxHp
        self.reach = reach
        self.moveRange = movement
        self.initMod = initative
        self.AC = AC


class GridActor(Entity):

    def __init__(self, color, label, temp):
        super().__init__(color, label)
        self.temp = temp
        self.curHp = temp.maxHp
        
    def damage(self, dmg):
        self.curHp -= dmg
        
    def heal(self, heal):
        self.curHp += heal
        temp = self.temp
        if self.curHp > temp.maxHp:
            self.curHp = temp.maxHp


class GenericGridActor(GridActor):
    
    def __init__(self, color, label, temp, count):
        super().__init__(color, label, temp)
        self.count = count      
        
    def getLabel(self):
        return self.label + str(self.count)
    
    def __str__(self):
        return str(self.toTuple())
    
    
class ActorManager:
    
    def __init__(self):
        self.Dict = {}
        
    def makeGeneric(self, color, label, temp):
        generic = (temp, 0, [])
        self.Dict[(color, label)] = generic
        return generic
    
    def addGeneric(self, color, label):
        match = self.Dict.get((color, label))
        if isinstance(match, tuple):
            (temp, count, List) = match
        elif match == None:
            (temp, count, List) = self.makeGeneric(color, label, None)
        else:
            return None    
        count += 1
        actor = GenericGridActor(color, label, temp, count)
        List.append(actor)
        self.Dict[(color, label)] = (temp, count, List)
        return actor
    
    def remove(self, actor):
        key = actor.toKey()
        match = self.Dict.get(key)
        if isinstance(match, tuple):
            (_temp, _count, List) = match
            List.remove(actor)
            # for gen in List:
            #     print(gen)
            if not List:
                self.Dict.pop(key)
        else:
            self.Dict.pop(key)
            

groups = {'Party': 'green', 'Enemies': 'red', 'Allies': 'blue', 'Other': 'yellow'}


class ActorWindow(ActorManager):
        
    def __init__(self, root, font, baseWidth):
        self.window = root
        root.title("Dungeon Master Screen")
        root.protocol("WM_DELETE_WINDOW", lambda:0)
        super().__init__()
        # print(list(groups.keys()))
        self.Group = Combobox(root, values=list(groups.keys()), font=font, width=baseWidth // 2)
        self.Label = Entry(root, font=font, width=baseWidth // 4)
        self.Name = Entry(root, font=font, width=baseWidth)
        self.HP = Entry(root, font=font, width=baseWidth // 4)
        self.AC = Entry(root, font=font, width=baseWidth // 4)
        self.Init = Entry(root, font=font, width=baseWidth // 4)
        self.Move = Entry(root, font=font, width=baseWidth // 4)
        self.Reach = Entry(root, font=font, width=baseWidth // 4)
        group = Label(root, text="Group", relief=GROOVE, font=font)
        icon = Label(root, text="Icon", relief=GROOVE, font=font)
        name = Label(root, text="Name", relief=GROOVE, font=font)
        hp = Label(root, text="HP", relief=GROOVE, font=font)
        ac = Label(root, text="AC", relief=GROOVE, font=font)
        init = Label(root, text="Init", relief=GROOVE, font=font)
        move = Label(root, text="Move", relief=GROOVE, font=font)
        reach = Label(root, text="Reach", relief=GROOVE, font=font)
        i = 0
        for label in [self.Group, self.Label, self.Name, self.HP, self.AC, self.Init, self.Move, self.Reach]:
            label.grid(row=0, column=i)
            i += 1
        i = 0
        for label in [group, icon, name, hp, ac, init, move, reach]:
            label.grid(row=1, column=i)
            i += 1
                
    # def make(self, ):
        
# man = ActorManager()
# man.makeGeneric('blue', 'T', 'test')
# man.addGeneric('red', 'T')

# class EntityManager:
#
#     def __init__(self):
#         self.Dict = {}
#
#     def makeEntity(self, color, name):
#         matches = self.Dict[(color, name)] 
#         if matches == None:
#             self.Dict[(color, name)] = Entity(color,name,0)
#         elif isinstance(matches, list):
#             if matches.isEmpty():
#                 self.Dict[(color, name)] = Entity(color,name,0)
#             else:
#                 count = matches[-1].getCount()+1
#                 matches.append(Entity(color, name, count))
#         else:
#             matches.setCount(1)
#             self.Dict[(color, name)] = [matches, Entity(color, name, 2)]
#
#     def removeEntity(self, entity):
#         (color, name, _count) = entity.toTuple()
#         matches = self.Dict[(color, name)] 
#         if matches == None:
#             return False
#         elif isinstance(matches, list):
#             if not matches.isEmpty():
#                 self.Dict[(color, name)].pop(entity)
#                 return True
#             return False
#         else:
#             self.Dict.pop((color,name))
#             return True
    
