from fuzzyset import InfiniteFuzzySet, ValueFuzzySet


class FuzzyController:
    def __init__(self):
        self.last_temp = 0
        self.diff_temp = 0
        self.curr_temp = 0

        self._error_interval = [-5, 0, 5]
        self._error_set = InfiniteFuzzySet(self._error_interval)
        self._diff_error_interval = [-5, 0, 5]
        self._diff_error_set = InfiniteFuzzySet(self._diff_error_interval)
        self._value_set = ValueFuzzySet([0, 1])

        self._rules = [
            [1, 1, 1],
            [1, 0, 0],
            [0, 0, 0]
            ]

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
            self.update(avg_temp, 0.02)

            value = avg_temp
            e_mem = self._error_set.fuzzificate(self.curr_temp)
            e_diff_mem = self._diff_error_set.fuzzificate(self.curr_temp)

            turn_off = 0.0
            turn_on = 0.0
            for row_index in range(len(self._rules)):
                row = self._rules[row_index]
                for col_index in range(len(row)):
                    rule = row[row_index]
                    rule_strength = e_mem[self._error_interval[row_index]] * e_diff_mem[self._diff_error_interval[col_index]]

                    if(rule == 1):
                        turn_on += rule_strength
                    else:
                        turn_off += rule_strength

            strength_sum = turn_on + turn_off
            turn_on /= strength_sum
            turn_off /= strength_sum

            power = self._value_set.defuccificate([turn_off, turn_on])

            driver.heat(power)

            print("Temperature of system is [0]", temp0, " [1]", temp1, "°C and controller is set to ", power)

        return

    def update(self, value, timespan):
        self.diff_temp = (value - self.last_temp) / timespan
        self.last_temp = self.curr_temp
        self.curr_temp = value

        return self.__getValue()
