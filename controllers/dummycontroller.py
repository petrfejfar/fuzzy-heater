import time


class DummyController:
    # driver is class of
    def runController(self, driver):
        # do very basic work
        power = 0.0  # ratio
        desired_temp = 33.0  # Celsius
        while True:
            temp0 = driver.temperature(0)
            # temp1 = driver.temperature(1)
            temp1 = temp0
            avg_temp = (temp0 + temp1) / 2.0

            if(avg_temp < desired_temp):
                power = min(1.0, power + 0.02)
            else:
                power = max(0.0, power - 0.02)
            # if(avg_temp < desired_temp):
            #     power = 1.0
            # else:
            #     power = 0.0
            driver.heat(power)

            print("Temperature of system is [0]", temp0, " [1]", temp1, "°C and controller is set to ", power)

        return
