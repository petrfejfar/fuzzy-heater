import random

# from controllers.RPidriver import RPiDriver
from controllers.simulationdriver import SimulationDriver

from controllers.dummycontroller import DummyController
from controllers.PIDcontroller import PIDController
from controllers.fuzzycontroller import FuzzyController

if(__name__ == "__main__"):
    print("Simulation start.")
    try:
        driver = SimulationDriver()
        # driver = RPiDriver()
        # c = DummyController()
        c = PIDController()
        c.runController(driver)
    finally:
        driver.close()

    print("Simulation ends.")
