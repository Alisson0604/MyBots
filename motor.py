import pyrosim.pyrosim as pyrosim
import pybullet as p
import constants as c
import numpy

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):

        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.offset = c.offset

        if self.jointName == b'Torso_FrontLeg':
            self.frequency = c.frequency
        else:
            self.frequency = c.frequency / 4

        self.motorValues = numpy.zeros(c.steps)

        for t in range(c.steps):
            self.motorValues[t] = self.amplitude * numpy.sin(
                self.frequency * t + self.offset
            )

    def Set_Value(self, robot, t):
        targetLocation = self.motorValues[t]

        pyrosim.Set_Motor_For_Joint(
        bodyIndex=robot.robotId,
        jointName=self.jointName,
        controlMode=p.POSITION_CONTROL,
        targetPosition=targetLocation,
        maxForce=c.maxForce
        )