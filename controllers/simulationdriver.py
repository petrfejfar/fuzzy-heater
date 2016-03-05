from random import random
import threading
from time import sleep
import matplotlib.pyplot as plt
import datetime


class SimulationDriver:
    # enviroment constants
    water_volume = 0.25  # liters
    water_ther_capacity = 4185.5  # J/(kg*K)
    heater_power = 25  # Watt
    enviroment_temp = 23.0  # Celsius

    # model
    actual_temp = 23.0  # Celsius
    power_ratio = 0.0  # ratio

    def __init__(self):
        # tuples (date, heat set)
        self.heat_log = []

        self.lock = threading.Lock()

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

        sleep(1)
        return self.actual_temp + random() - 0.5

    # ratio is interval 0.0 to 1.0
    # 0.0 means turn off
    # 1.0 means turn on
    # <0.0; 1.0> is linear proportion
    def heat(self, ratio):
        with self.lock:
            self.power_ratio = ratio
            self.heat_log.append((datetime.datetime.now(), ratio))

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

            temp1_log.append((datetime.datetime.now(), self.temperature(0)))
            temp2_log.append((datetime.datetime.now(), self.temperature(1)))

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

            sleep(2)

    def close(self):
        pass
