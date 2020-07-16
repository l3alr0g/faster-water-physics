from panda3d.core import Vec2,Vec4
from math import cos, pi
from PIL import Image



class ShapeBox:
    def __init__(self):
        self.available_shapes = {
            "circular":self.c_mat
        }
    def create(self, name, *kwargs):
        if len(kwargs): data = self.available_shapes[name](kwargs)
        else: data = self.available_shapes[name]()
        return data
    
    def c_mat(self, 
            res = 1080,
            smoothness_rad = 40,
            radius = 500,
            center = Vec2(540, 540),
            Hsat = 1, 
            Lsat = 0): 
        
        def interpol_func(r, smoothness, centval): # we'll use the cos function
            if -pi < pi*(r - centval)/smoothness < pi: shade = (cos(pi*(r - centval)/smoothness)+1)/2
            else:
                shade = 0
            if shade > Hsat: shade = Hsat
            elif shade < Lsat: shade = Lsat
            return shade

        data = [[Vec4(1,1,1,0) for i in range(res)] for j in range(res)] # initialize raw data 
        for i in range(res):
            for j in range(res):
                r = dist(Vec2(i,j), center)
                shade = interpol_func(r, smoothness_rad, radius)
                data[i][j] = Vec4(shade, shade, shade, 1)
        return data
    
    def format(self, data):
        output = ()
        for x in data:
            temp = []
            for y in x:
                u = list(y)
                for a in range(4):
                    u[a]*=255
                    u[a] = int(u[a])
                temp.append(tuple(u)[0:3])
            output+=tuple(temp)
        im = Image.new('RGB', (len(data), len(data)))
        
        im.putdata(output)
        im.save('output.png')
        print('saved as output.png')
        return

def dist(p1:Vec2, p2:Vec2):
    vect = p1 - p2
    return vect.length()


if __name__=="__main__":
    S = ShapeBox()
    output = S.create("circular")
    S.format(output)
