#!python3
import time

class Controller:
    # driver is class of
    def runController(self, driver):
        # do very basic work
        while(True):
            print("Temperature on thermometer 0 is ", driver.temperature(0), "°C");
            time.sleep(2);
        return;