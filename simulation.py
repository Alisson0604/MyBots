from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import constants as c
import numpy
import time

class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI

        if directOrGUI == "DIRECT":
            p.connect(p.DIRECT)
        else:
            p.connect(p.GUI)
            
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.world = WORLD()
        self.robot = ROBOT(solutionID)

    def Run(self):
        for i in range(c.steps):
            p.stepSimulation()
            if self.directOrGUI == "GUI":
                time.sleep(1/240)

            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)

    def Get_Fitness(self):
        self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()
