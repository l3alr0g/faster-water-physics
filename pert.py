# imports
from panda3d.core import Vec2
from PIL import Image
from math import cos, sin, acos, asin, pi
from surface import Surface
import os

DIR = os.getcwd()

'''
relation de dispersion pour un sillage de kelvin: w**2 = gk => w = g/c avec c = v(solide) soit w = g/v(solide)
'''
class Pert:
    def __init__(self, id:str, o_ls:float, i_ls:float, duration:float, parent = None):
        self.outer_lifespan = o_ls
        self.inner_lifespan = i_ls
        self.id = id
        self.duration = duration
        self.linked_to = None
        self.reparentTo(parent)
    
    def reparentTo(self, parent):
        self.parent = parent
        self.parent.addChild(self)
    
    def link(self, s_o):
        self.linked_to = s_o
        return

class Circular(Pert):
    def __init__(self, id:str, o_ls:float, i_ls:float, duration:float, parent:Surface, w, c = 0.5, A = 1, t_init = 0):
        '''
        id - associated name
        o_ls - outer lifespan (time before the perturbation dies)
        i_ls - inner lifespan (same thing but inside the circle)
        duration - explicit
        parent - class Surface
        w, c, A, t_init - sim parameters
        '''
        g = 9.81
        w = g/c
        Pert.__init__(self, id, o_ls, i_ls, duration, parent)
        self._attrib = (w, w/c, c, A) # w, c, k, amp, phi temporel
        self.phi = t_init
        return None

    def _expr(self, r, t):
        r = abs(r)
        w, k, A = self._attrib[:2] + self._attrib[3:]
        amp = self.amplitude(r, t)
        ans = amp*cos(w*(t - self.phi) - k*r + pi/2)
        ans += 1
        ans /= 2 # heightmap format
        return (ans-0.5)*A + 0.5
    
    def amplitude(self, r, t):
        c = self._attrib[2]
        a, b = c*(t-self.duration), min(c*t, c*self.outer_lifespan)

        if math_in(r, [a, b]) and a < b:
            amp = (1 - r/(c*self.outer_lifespan))
            return amp    
        elif math_in(r, [c*(t-self.duration-self.inner_lifespan),a], exclude=(a)):
            if (1 - r/(c*self.outer_lifespan)) >= 0: amp = (1 - r/(c*self.outer_lifespan))
            else: amp = 0
            amp *= (r/(c*self.inner_lifespan) + (self.duration + self.inner_lifespan - t)/self.inner_lifespan)
            return amp
        else: return 0
    
    def getData(self, res, startingpoint:Vec2, t):
        data = []
        for i in range(res[0]):
            line = []
            for j in range(res[1]):
                r = dist(Vec2(i,j), startingpoint)*self.parent.pix_dist
                shade = self._expr(r, t)
                line.append(shade)
            data.append(line)
        return data

class Kelvin(Pert):
    def __init__(self, id:str, o_ls:float, i_ls:float, duration:float, parent:Surface, w = 2.5, c = 0.5, A = 1):
        Pert.__init__(self, id, o_ls, i_ls, duration, parent)
        self._attrib = (w, w/c, c, A)
        return None
    
    def getData(self, res, t):
        data = []
        

'''
class Wind(Pert):
    def __init__(self):
        raise NotImplementedError("this class isn't ready to use (yet)")
'''

# utility functions

def dist(p1:Vec2, p2:Vec2):
    vect = p1 - p2
    return vect.length()

def math_in(x, interval:list, exclude:list = []):
    '''
    math version of the 'in' keyword: math_in(x, [a,b]) 
    exclude (non-default) should contain the borders of the interval you want to ignore
    '''
    interval.sort()
    if type(exclude) in (float, int): # single-value tuples get converted to ints/floats
        exclude = [exclude]
    try:
        if interval[0] in exclude: out0 = interval[0] < x
        else: out0 = interval[0] <= x
        if interval[1] in exclude: out1 = x < interval[1]
        else: out1 = x <= interval[1]
        return out0 and out1  
    except: raise TypeError


def format(data, name):
    output = ()
    for x in data:
        temp = []
        for y in x:
            u = y*255
            u = int(u)
            temp.append((u,u,u))
        output += tuple(temp)
    im = Image.new('RGB', (len(data), len(data)))
    
    im.putdata(output)
    im.save(DIR+"\\output\\"+name+'.png')
    print('saved as %s.png' % name)
    return


if __name__=='__main__': # testing
    from surface import Surface
    mesh = Surface("water", (400, 400), 'RGB', pix_dist = 0.03)
    new_pert = Circular('drop1', 5, 1, 1.5, mesh, 25, c = 2, A = 0.1, t_init = 0)
    for i in range(45, 50):
        data = new_pert.getData(mesh.res, Vec2(200, 200), i*0.1)
        format(data ,'output%ss'%i)
    