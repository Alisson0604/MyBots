import pyrosim.pyrosim as pyrosim
import pybullet as p
import pybullet_data

class WORLD:
    def __init__(self):
        p.loadSDF("world.sdf")
        p.loadURDF("plane.urdf")
	