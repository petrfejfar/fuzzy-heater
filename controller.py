#!python3
import time
import random

class Controller:
    # driver is class of
    def runController(self, driver):
        # do very basic work
        power = 0.0; # ratio 
        desired_temp = 33.0; # Celsius
        while(True):
            temp1 = driver.temperature(0);
            temp2 = driver.temperature(1);
            avg_temp = (temp1 + temp2) / 2.0;
            
            if(avg_temp < desired_temp):
                power = min(1.0, power + 0.02);
            else:
                power = max(0.0, power - 0.02);                
            driver.heat(power);
                    
            print("Temperature of system is ", avg_temp, "°C and controller is set to ", power);
            time.sleep(2);
        return;