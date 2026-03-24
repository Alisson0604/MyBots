from world import WORLD
from robot import ROBOT

import pybullet as p
import pybullet_data
import constants as c
import numpy
import time

class SIMULATION:
    def __init__(self):
        p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        for i in range(c.steps):
            p.stepSimulation()
            time.sleep(1/60)

            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)

    def __del__(self):
        p.disconnect()