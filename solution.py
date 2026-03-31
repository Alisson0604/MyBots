import pyrosim.pyrosim as pyrosim
import random
import numpy as np
import os
import time

class SOLUTION:
    def __init__(self, id):
        self.myID = id
        self.weights = np.random.rand(3,2) * 2 - 1
        self.fitness = 0
    
    def Set_ID(self, id):
        self.myID = id

    def Mutate(self):
        randomRow = random.randint(0, 2)
        randomColumn = random.randint(0, 1)

        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()

        brain_file = "brain" + str(self.myID) + ".nndf"
        while not os.path.exists(brain_file):
            time.sleep(0.01)

        os.system("start /B python simulate.py " + directOrGUI + " " + str(self.myID))
    
    def Wait_For_Simulation_To_End(self):

        fitnessFileName = "fitness" + str(self.myID) + ".txt"

        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        with open(fitnessFileName, "r") as f:
            self.fitness = float(f.read())

        os.system("del " + fitnessFileName)

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(
            name="WorldCube",
            pos=[5,0,0.5],
            size=[1,1,1]
        )
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(
            name="Torso",
            pos=[0,0,1.5],
            size=[1,1,1]
        )

        # BACK LEG
        pyrosim.Send_Joint(
            name="Torso_BackLeg",
            parent="Torso",
            child="BackLeg",
            type="revolute",
            position=[-0.5,0,1]
        )

        pyrosim.Send_Cube(
            name="BackLeg",
            pos=[-0.5,0,-0.5],
            size=[1,1,1]
        )

        # FRONT LEG
        pyrosim.Send_Joint(
            name="Torso_FrontLeg",
            parent="Torso",
            child="FrontLeg",
            type="revolute",
            position=[0.5,0,1]
        )

        pyrosim.Send_Cube(
            name="FrontLeg",
            pos=[0.5,0,-0.5],
            size=[1,1,1]
        )
        pyrosim.End()

    def Generate_Brain(self):

        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

        for currentRow in range(3):    
            for currentColumn in range(2): 
                weight = self.weights[currentRow][currentColumn]
                pyrosim.Send_Synapse(
                    sourceNeuronName=currentRow,
                    targetNeuronName=currentColumn + 3,
                    weight=weight
                )
        pyrosim.End()