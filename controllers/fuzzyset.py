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


class InfiniteFuzzySet:

    def __init__(self, values):
        """
            values = [-10, -5, 0, 5, 10]
        """
        self._values = values

    def fuzzificate(self, value):
        # create empty membership
        result = dict((x, 0) for x in self._values)

        if(value <= self._values[0]):
                result[self._values[0]] = 1
                return result

        if(value >= self._values[-1]):
                result[self._values[-1]] = 1
                return result

        left_index = 0
        right_index = 1

        while (self._values[right_index] < value):
            left_index += 1
            right_index += 1

        left_val = self._values[left_index]
        right_val = self._values[right_index]

        print(left_val, ", ", right_val)

        result[right_val] = float(value-left_val)/(right_val-left_val)
        result[left_val] = float(right_val-value)/(right_val-left_val)

        return result


class ValueFuzzySet:

    def __init__(self, values, interval_width):
        """
            values = [-10, -5, 0, 5, 10]
        """
        self._values = values
        self._interval_width = interval_width

    def defuccificate(self, weights):
        """
            weights = [0, 0.3, 0.2, 0, 1]
        """

        strengths = list(map(lambda w: w*self._interval_width*(2-w)/2.0, weights))
        center_of_gravity = sum(map(lambda x: x[0]*x[1], zip(strengths, self._values)))/sum(strengths)

        return center_of_gravity

class GainFuzzySet:

    def __init__(self, low, high):
        self._low = low
        self._high = high

    def fuzzificate(self, value):
        pass
