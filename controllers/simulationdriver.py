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

from random import random
import threading
from time import sleep, time
import matplotlib.pyplot as plt


class SimulationDriver:
    # enviroment constants
    water_volume = 0.25  # liters
    water_ther_capacity = 4185.5  # J/(kg*K)
    heater_power = 25  # Watt
    enviroment_temp = 23.0  # Celsius

    def __init__(self):
        # tuples (date, heat set)
        self.heat_log = []

        self.lock = threading.Lock()

        # model
        self.actual_temp = 23.0  # Celsius
        self.power_ratio = 0.0  # ratio

        self.start_time = time()

        # run background simulation
        self.model_thread = threading.Thread(target=self.update_state)
        # thread dies on program exit
        self.model_thread.daemon = True
        self.model_thread.start()

        thread = threading.Thread(target=self.make_plot)
        # thread dies on program exit
        thread.daemon = True
        thread.start()

        return

    # index is 0 or 1 (we have 2 thermometers), otherwise raise exception
    def temperature(self, index):
        with self.lock:
            if(index != 0 and index != 1):
                raise Exception("Invalid thermometer index.")

        sleep(0.5)
        return self.actual_temp  # + random() - 0.5

    # ratio is interval 0.0 to 1.0
    # 0.0 means turn off
    # 1.0 means turn on
    # <0.0; 1.0> is linear proportion
    def heat(self, ratio):
        with self.lock:
            self.power_ratio = ratio
            t = time() - self.start_time
            self.heat_log.append((t, ratio))

            if(ratio < 0.0 or ratio > 1.0):
                raise Exception("Argument ratio out of range.")

        return

    def update_state(self):
        while True:
            with self.lock:
                time_span = 0.02  # sec

                # simulate heat from heater
                energy_emitted = self.power_ratio * self.heater_power * time_span  # J
                therm_delta = energy_emitted / (self.water_ther_capacity * self.water_volume)  # Celsius
                self.actual_temp += therm_delta

                # simulate enviroment cooling (magic aproximation)
                energy_emitted = 0.5 * self.heater_power * time_span  # J
                therm_delta = energy_emitted / (self.water_ther_capacity * self.water_volume)  # Celsius
                self.actual_temp -= therm_delta

            sleep(time_span/1000000)
        return

    # draw plot with historical data about model
    def make_plot(self):
        temp1_log = []
        temp2_log = []
        while True:
            t = time() - self.start_time
            temp1_log.append((t, self.temperature(0)))
            temp2_log.append((t, self.temperature(1)))

            # draw
            plt.clf()
            plt.title('Temperature on sensors')
            [val, date] = zip(*temp1_log)
            plt.subplot(211)
            plt.plot(val, date, color="red", aa=True, label="temp1")
            [val, date] = zip(*temp2_log)
            plt.plot(val, date, color="green", aa=True, label="temp2")
            if self.heat_log:
                with self.lock:
                    plt.title('Heat commands')
                    [val, date] = zip(*self.heat_log)
                    plt.subplot(212)
                    plt.plot(val, date, color="blue", aa=True, label="heat")
            plt.savefig("history.png")

            sleep(0.1)

    def close(self):
        pass
