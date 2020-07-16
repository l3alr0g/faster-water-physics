# imports


class Surface:
    def __init__(self, id, res:tuple, format:str, pix_dist = 0.005): # pixdist is the real life distance between two pixels 
        self.id = id
        self.res = res
        self.pix_dist = pix_dist
        self.format = format
        self._children = []
    
    def bake(self, tl):
        '''
        bake the data for the provided timeline
        '''
        data = None
        return data
    
    def addChild(self, child):
        self._children.append(child)


