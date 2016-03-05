import time


class PIDController:
    kP = 1.0
    kI = 1.0
    kD = 1.0

    last_temp = 0
    diff_temp = 0
    sum_temp = 0
    curr_temp = 0

    def setConstants(self, p, i, d):
        self.kP = p
        self.kI = i
        self.kD = d

    def update(self, value, timespan):
        self.diff_temp = (value - self.last_temp) / timespan
        self.sum_temp += self.diff_temp
        self.last_temp = self.curr_temp
        self.curr_temp = value

        return self.__getValue()

    def __getValue(self):
        return self.kP * (self.curr_temp - self.last_temp) + self.kI * self.sum_temp + self.kD * self.diff_temp
