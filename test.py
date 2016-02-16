#!python3
import random
import threading
import controller
import time;
import matplotlib.pyplot as plt
import datetime

class SimulatedHeater:    
    # enviroment constants
    water_volume = 0.25; # liters
    water_ther_capacity = 4185.5; # J/(kg*K)
    heater_power = 25; # Watt
    enviroment_temp = 23.0; # Celsius
    
    # model
    actual_temp = 23.0; # Celsius
    power_ratio = 0.0; # ratio

    # tuples (date, heat set)
    heat_log = [];

    lock = threading.Lock();
    
    def __init__(self):
        self.__run();
        
        return;
    
    # index is 0 or 1 (we have 2 thermometers), otherwise raise exception
    def temperature(self, index):
        with self.lock:
            if(index != 0 and index != 1):
                raise Exception("Invalid thermometer index.");
        
        return self.actual_temp + random.random() - 0.5;
        
    # ratio is interval 0.0 to 1.0 
    # 0.0 means turn off
    # 1.0 means turn on
    # <0.0; 1.0> is linear proportion
    def heat(self, ratio):
        with self.lock:
            self.power_ratio = ratio;
            self.heat_log.append((datetime.datetime.now(), ratio));        
                
            if(ratio < 0.0 or ratio > 1.0):
                raise Exception("Argument ratio out of range.");
        
        return;
        
    # 
    def __run(self):
        # update inner state of model       
        def update_state():
            while True:
                with self.lock:
                    time_span = 0.02; # sec
                    
                    # simulate heat from heater 
                    energy_emitted = self.power_ratio * self.heater_power * time_span; # J
                    therm_delta = energy_emitted / (self.water_ther_capacity * self.water_volume); # Celsius
                    self.actual_temp += therm_delta;
                    
                    # simulate enviroment cooling (magic aproximation)
                    energy_emitted = 0.5 * self.heater_power * time_span; # J
                    therm_delta = energy_emitted / (self.water_ther_capacity * self.water_volume); # Celsius
                    self.actual_temp -= therm_delta;
                    
                time.sleep(time_span);
            return;
            
        # draw plot with historical data about model
        def make_plot():
            temp1_log = [];           
            temp2_log = [];           
            while True:
                    
                temp1_log.append((datetime.datetime.now(), self.temperature(0)));                
                temp2_log.append((datetime.datetime.now(), self.temperature(1)));                
                
                # draw
                plt.clf();    
                plt.title('Temperature on sensors');
                [val, date] = zip(*temp1_log);
                plt.subplot(211);
                plt.plot(val, date, color = "red", aa = True, label = "temp1");
                [val, date] = zip(*temp2_log);
                plt.plot(val, date, color = "green", aa = True, label = "temp2");
                if self.heat_log:
                    with self.lock:
                        plt.title('Heat commands');
                        [val, date] = zip(*self.heat_log);
                        plt.subplot(212)
                        plt.plot(val, date, color = "blue", aa = True, label = "heat");
                plt.savefig("history.png");
                
                time.sleep(2);
           
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