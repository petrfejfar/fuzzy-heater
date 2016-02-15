#!python3

import threading
import controller

class SimulatedHeater:
    lock = threading.Lock();
    
    # index is 0 or 1 (we have 2 thermometers), otherwise raise exception
    def temperature(self, index):
        with self.lock:
            if(index != 0 and index != 1):
                raise Exception("Invalid thermometer index.");
        
        return 25.0;
        
    # ratio is interval 0.0 to 1.0 
    # 0.0 means turn off
    # 1.0 means turn on
    # <0.0; 1.0> is linear proportion
    def power(self, ratio):
        with self.lock:
            if(ratio < 0.0 or ratio > 1.0):
                raise Exception("Argument ratio out of range.");
        
        return;
        
    # 
    def __run(self):
        def fnc():
            return;
        
        thread = threading.Thread(target=fnc);
        # thread dies on program exit
        thread.daemon = True;  
        thread.start();
        
        return;
        

if(__name__ == "__main__"):
    print("Simulation start.");
    driver = SimulatedHeater();
    controller.controller.runController(driver);
    print("Simulation ends.");