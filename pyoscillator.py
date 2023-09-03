import math
import random


class Oscillator:
    def sin(t):
        return math.sin(t)

    def saw(t):
        if t < math.pi:
            return t / math.pi
        else:
            return -1 + ((t - math.pi) / math.pi)

    def square(t):
        if t < math.pi:
            return 0.999999
        else:
            return -0.999999

    def triangle(t):
        return (math.acos(math.cos(t)) / math.pi - 0.5) * 2

    def noise():
        return random.uniform(-1, 1)
