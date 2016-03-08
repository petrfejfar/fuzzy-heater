# The MIT License (MIT)
#
# Copyright (c) 2016 Petr Fejfar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from controllers.fuzzyset import InfiniteFuzzySet, ValueFuzzySet
from time import time


class FuzzyController:
    def __init__(self, desired_temp):
        self.last_e = 0.0
        self.d_e = 0.0

        self._desired_temp = desired_temp

        self._error_interval = [-1, 0, 1]
        self._error_set = InfiniteFuzzySet(self._error_interval)
        self._diff_error_interval = [-0.5, 0, 0.5]
        self._diff_error_set = InfiniteFuzzySet(self._diff_error_interval)
        self._value_set = ValueFuzzySet([0, 1], 1)

        self._rules = [
            [0, 0, 0.5],
            [0, 0.5, 1],
            [0.5, 1, 1]
            ]

    # driver is class of
    def runController(self, driver, period):
        last_timestamp = time()
        while True:
            temp0 = driver.temperature(0)
            # temp1 = driver.temperature(1)
            temp1 = temp0
            avg_temp = (temp0 + temp1) / 2.0
            self.update(avg_temp, 0.02)

            curr_timestamp = time()
            delta = curr_timestamp - last_timestamp
            last_timestamp = curr_timestamp

            e = self._desired_temp - avg_temp
            d_e = (e - self.last_e) / delta
            self.last_e = e

            value = avg_temp
            e_mem = self._error_set.fuzzificate(e)
            print("e_mem is ", e , "###", e_mem)
            e_diff_mem = self._diff_error_set.fuzzificate(d_e)
            print("e_diff_mem=",d_e, "###", e_diff_mem)

            turn_off = 0.0
            turn_on = 0.0
            for row_index in range(len(self._rules)):
                row = self._rules[row_index]
                a = []
                for col_index in range(len(row)):
                    rule = row[col_index]
                    rule_strength = e_mem[self._error_interval[row_index]] * e_diff_mem[self._diff_error_interval[col_index]]
                    a.append(rule_strength)

                    print(rule, self._error_interval[row_index], self._diff_error_interval[col_index])
                    turn_on += rule_strength * rule
                print(a)
            print(turn_on, turn_off)

            #strength_sum = turn_on + turn_off
            #turn_on /= strength_sum
            #turn_off /= strength_sum

            #power = self._value_set.defuccificate([turn_off, turn_on])
            power = turn_on
            driver.heat(power)

            print("Temperature of system is [0]", temp0, " [1]", temp1, "°C and controller is set to ", power)

        return

    def update(self, value, timespan):
        pass
