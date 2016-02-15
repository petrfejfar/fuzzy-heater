#!python3
import random
import threading
import controller
import time;

class SimulatedHeater:
    lock = threading.Lock();
    actual_temp = 25;

    def __init__(self):
        self.__run();
        
        return;
    
    # index is 0 or 1 (we have 2 thermometers), otherwise raise exception
    def temperature(self, index):
        with self.lock:
            if(index != 0 and index != 1):
                raise Exception("Invalid thermometer index.");
        
        return self.actual_temp;
        
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
        # update inner state of model       
        def update_state():
            while True:
                self.actual_temp += random.random() - 0.5;
                time.sleep(0.02);
            return;
            
        # draw plot with historical data about model
        def make_plot():
            # TODO
            return;            
        
        thread = threading.Thread(target=update_state);
        # thread dies on program exit
        thread.daemon = True;  
        thread.start();
    
        thread = threading.Thread(target=make_plot);
        # thread dies on program exit
        thread.daemon = True;  
        thread.start();
        
        return;
        

if(__name__ == "__main__"):
    print("Simulation start.");
    driver = SimulatedHeater();
    c = controller.Controller()
    c.runController(driver);
    print("Simulation ends.");