from hillclimber import HILL_CLIMBER
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import os

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()

#for i in range(5):
#    os.system("python generate.py")
#    os.system("python simulate.py")

