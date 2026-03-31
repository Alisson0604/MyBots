from solution import SOLUTION
import os
import copy
import constants as c

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")

        self.parents = {}
        self.nextAvailableID = 0

        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evaluate(self, solutions):
        for i in solutions:
            solutions[i].Start_Simulation("DIRECT")

        for i in solutions:
            solutions[i].Wait_For_Simulation_To_End()

    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Spawn(self):
        self.children = {}

        for i in self.parents:
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for i in self.children:
            self.children[i].Mutate()

    def Select(self):
        for i in self.parents:
            if self.children[i].fitness < self.parents[i].fitness:
                self.parents[i] = self.children[i]

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()
    
    def Print(self):
        print("") 
        for i in self.parents:
            print(f"Parent: {self.parents[i].fitness} | Child: {self.children[i].fitness}")
        print("")

    def Show_Best(self):
        best_key = 0
        for i in self.parents:
            if self.parents[i].fitness < self.parents[best_key].fitness:
                best_key = i
        
        self.parents[best_key].Start_Simulation("GUI")

   