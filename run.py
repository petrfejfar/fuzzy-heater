# The MIT License (MIT)
#
# Copyright (c) 2016 Petr Fejfar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
        # c = PIDController(33.0)
        c = FuzzyController(33.0)
        c.runController(driver, 5.0)
    finally:
        driver.close()

    print("Simulation ends.")
