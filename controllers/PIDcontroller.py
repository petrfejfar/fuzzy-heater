class PIDController:

    def __init__(self):
        self.kP = 1.0
        self.kI = 1.0
        self.kD = 1.0

        self.last_temp = 0
        self.diff_temp = 0
        self.sum_temp = 0
        self.curr_temp = 0

    def setConstants(self, p, i, d):
        self.kP = p
        self.kI = i
        self.kD = d

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

            driver.heat(self.update(avg_temp, 0.02))

            print("Temperature of system is [0]", temp0, " [1]", temp1, "°C and controller is set to ", power)

        return

    def update(self, value, timespan):
        self.diff_temp = (value - self.last_temp) / timespan
        self.sum_temp += self.diff_temp
        self.last_temp = self.curr_temp
        self.curr_temp = value

        return self.__getValue()

    def __getValue(self):
        return self.kP * (self.curr_temp - self.last_temp) + self.kI * self.sum_temp + self.kD * self.diff_temp
