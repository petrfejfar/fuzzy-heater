import threading
import time
import datetime
import os
import glob
import RPi.GPIO as GPIO


class RPiDriver:
    DRIVER_BASE_DIR = '/sys/bus/w1/devices/'
    DEVICE_FOLDERS = glob.glob(DRIVER_BASE_DIR + '28*')
    device_file = [DEVICE_FOLDERS[0]+'/w1_slave'] # , DEVICE_FOLDERS[1]+'/w1_slave']

    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)

        self._pwm = GPIO.PWM(17, 5)
        self._pwm.start(0)

        return

    def read_temp_raw(self, index):
        f = open(self.device_file[index], 'rt')
        lines = f.readlines()

        f.close()

        return lines

    def read_temp(self, index):
        lines = self.read_temp_raw(index)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.1)
        lines = self.read_temp_raw(index)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0

        return temp_c

    # index is 0 or 1 (we have 2 thermometers), otherwise raise exception
    def temperature(self, index):
        if(index != 0 and index != 1):
            raise Exception("Invalid thermometer index.")

        return self.read_temp(index)

    # ratio is interval 0.0 to 1.0
    # 0.0 means turn off
    # 1.0 means turn on
    # <0.0; 1.0> is linear proportion
    def heat(self, ratio):
        self._pwm.start(ratio * 100.0)

        return

    def close(self):
        print("RPiDriver.close() called.")
        self._pwm.stop()
        GPIO.cleanup()
