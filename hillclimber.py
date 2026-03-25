from solution import SOLUTION
import copy
import constants as c

class HILL_CLIMBER:
    def __init__(self):
        self.parent = SOLUTION()
        self.child = None

    def Evolve(self):
        self.parent.Evaluate("GUI")

        for currentGeneration in range(1, c.numberOfGenerations + 1):
            self.Evolve_For_One_Generation()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.child.fitness < self.parent.fitness:
            self.parent = self.child

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()

    def Print(self):
        print(f"Parent fitness: {self.parent.fitness}, Child fitness: {self.child.fitness}")

    def Show_Best(self):
        self.parent.Evaluate("GUI")