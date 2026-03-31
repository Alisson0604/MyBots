from pyrosim.neuralNetwork import NEURAL_NETWORK
import pyrosim.pyrosim as pyrosim
import constants as c
import pybullet as p
import pybullet_data
import os

from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self, solutionID): 
        self.solutionID = solutionID
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)

        self.sensors = {}
        self.motors = {}
        
        brain_file = "brain" + str(self.solutionID) + ".nndf"
        self.nn = NEURAL_NETWORK(brain_file)
        
        if os.name == 'nt':
            os.system("del " + brain_file)
        else:
            os.system("rm " + brain_file)

        self.Prepare_To_Sense()
        self.Prepare_To_Act()
    
    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
       
    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                jointName = jointName.encode("utf-8")
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self, desiredAngle)

    def Think(self):
        self.nn.Update()
        #self.nn.Print()

    def Get_Fitness(self):
        tmpFile = "tmp" + str(self.solutionID) + ".txt"
        fitnessFile = "fitness" + str(self.solutionID) + ".txt"

        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        
        f = open(tmpFile, "w")
        f.write(str(xCoordinateOfLinkZero))
        f.close()

        if os.name == 'nt':
            # En Windows, os.rename falla si el destino existe. 'replace' es más seguro.
            if os.path.exists(fitnessFile):
                os.remove(fitnessFile)
            os.rename(tmpFile, fitnessFile)
        else:
            # En Linux/Mac mv sobreescribe por defecto
            os.system("mv " + tmpFile + " " + fitnessFile)