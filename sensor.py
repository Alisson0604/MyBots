import pyrosim.pyrosim as pyrosim
import constants as c
import numpy

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName

        # Create zero vectors
        self.values = numpy.zeros(c.steps)
    
    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
