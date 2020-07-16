from surface import Surface
from timeline import Timeline
from pert import Circular, Kelvin
from solid import SolidObject, Floater

mainFrame = Surface("water", (1080, 1080), 'RGB')
tl = Timeline(mainFrame, duration = 10, dt = 0.1)
boat = Floater("boat1", parent = mainFrame)

data = mainFrame.bake(tl)