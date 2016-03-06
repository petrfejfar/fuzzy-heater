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


        low_member =
