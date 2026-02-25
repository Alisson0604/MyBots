from simulation import SIMULATION

# numpy.save("data/backLegSensorValues.npy", backLegSensorValues)
# numpy.save("data/frontLegSensorValues.npy", frontLegSensorValues)

simulation = SIMULATION()
simulation.Run()