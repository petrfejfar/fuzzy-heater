import random

# from controllers.RPidriver import RPiDriver
from controllers.simulationdriver import SimulationDriver
from controllers.controller import Controller

if(__name__ == "__main__"):
    print("Simulation start.")
    try:
        driver = SimulationDriver()
        # driver = RPiDriver()
        c = Controller()
        c.runController(driver)
    finally:
        driver.close()

    print("Simulation ends.")
