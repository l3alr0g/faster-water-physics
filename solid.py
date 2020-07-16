# imports
from surface import Surface
from pert import Kelvin

class SolidObject:
    def __init__(self, id:str, parent:Surface = None, timeline = None):
        self.id = id
        self.perts = []
        if parent != None: self.reparentTo(parent)

    def reparentTo(self, parent:Surface):
        parent.addChild(self)
        return
    
    def link(self, new_pert):
        self.perts.append(new_pert)
        new_pert.link(self)
    
    def getPos(self, t):
        return
    
    def getSpeed(self, t):
        return

class Floater(SolidObject): # automatically linked to Kelvin pert
    def __init__(self, id:str, parent:Surface = None, o_ls = 15, i_ls = 4, duration = 1):
        SolidObject.__init__(self, id, parent = parent)
        kpert = Kelvin(id+"_pert", o_ls, i_ls, duration, parent)
