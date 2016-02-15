#!python3
import time

class controller:
    # driver is class of
    def runController(driver):
        # do very basic work
        while(True):
            print("Temperature on thermometer 0 is ", driver.temperature(0), "°C");
            time.sleep(2000);
        return;