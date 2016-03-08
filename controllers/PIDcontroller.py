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

from time import time, sleep


class PIDController:
    MAX_INTEGRATION_SUM = 150.0

    def __init__(self, desired_temp):
        ultimate_gain = 1.0
        oscillation_period = 240.0
        self.kP = 0.6*ultimate_gain
        self.kI = 2.0*self.kP/oscillation_period
        self.kD = self.kP*oscillation_period/8.0

        self._desired_temp = desired_temp

        self.last_e = 0.0
        self.d_e = 0.0
        self.sum_e = 0.0
        self.e = 0.0

    def __repr__(self):
        return "p=%.4f, i=%.4f, d=%.4f, e=%.4f, e_d=%.4f, s=%.4f, last_e=%.4f " % (
            self.kP, self.kI, self.kD, self.e, self.d_e, self.sum_e, self.last_e
        )

    def setConstants(self, p, i, d):
        self.kP = p
        self.kI = i
        self.kD = d

    def getTemp(self, driver):
        temp0 = driver.temperature(0)
        # temp1 = driver.temperature(1)
        temp1 = temp0
        avg_temp = (temp0 + temp1) / 2.0

        print("Temperature of system is [0]", temp0, " [1]", temp1, "°C")

        return avg_temp

    def runController(self, driver, period):
        last_timestamp = time()
        if(self.getTemp(driver) > self._desired_temp):
            driver.heat(0.0)
        else:
            driver.heat(1.0)

        while True:
            avg_temp = self.getTemp(driver)

            curr_timestamp = time()
            delta = curr_timestamp - last_timestamp
            if(delta < period):
                sleep(period - delta)
                curr_timestamp = time()
            delta = curr_timestamp - last_timestamp
            last_timestamp = curr_timestamp

            power = self.update(avg_temp, delta)
            print(self)
            print("power=", power, " delta=", delta)
            power = min(1.0, max(0.0, power))
            driver.heat(power)

            print("Controller is set to ", power)

        return

    def update(self, value, timespan):
        self.e = self._desired_temp - value
        self.d_e = (self.e - self.last_e) / timespan
        self.sum_e += self.e
        self.sum_e = min(self.MAX_INTEGRATION_SUM, max(-self.MAX_INTEGRATION_SUM, self.sum_e))
        self.last_e = self.e

        return self.__getValue()

    def __getValue(self):
        return self.kP*self.e + self.kI*self.sum_e + self.kD*self.d_e
