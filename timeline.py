# imports
from surface import Surface
from solid import SolidObject

class Timeline:
    def __init__(self, parent:Surface, duration:float = 1, dt:float = 0.04):
        assert duration > 0
        self.duration = duration
        self.data = []
        self.reparentTo(parent)
        
    
    def reparentTo(self, parent):
        parent.addChild(self)
        return
    
    def addActor(self, actor):
        return
    
    def addEvent(self, actor, event, t):
        return
    
    def getState(self, actor, t):
        return

