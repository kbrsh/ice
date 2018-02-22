import math
from ..random import random, randomConstant, randomNoise, randomNoise2D, maximumSlopePixel

# Operations
class VariableXOperator(object):
    def compute(self, x, y):
        return x

class VariableYOperator(object):
    def compute(self, x, y):
        return y

class ConstantOperator(object):
    def __init__(self):
        self.constant = (maximumSlopePixel * float(random())) - 1.0

    def compute(self, x, y):
        return self.constant

class AdditionOperator(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, x, y):
        return (self.a.compute(x, y) + self.b.compute(x, y)) / 2.0

class SubtractionOperator(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, x, y):
        return (self.a.compute(x, y) - self.b.compute(x, y)) / 2.0

class MultiplicationOperator(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, x, y):
        return self.a.compute(x, y) * self.b.compute(x, y)

class ReciprocalOperator(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        ac = self.a.compute(x, y)
        if ac == 0.0:
            return ac
        else:
            return (1.0 / self.a.compute(x, y)) % 1.0

class ExponentOperator(object):
    def __init__(self, a):
        self.a = a
        self.exponent = abs(randomConstant())

    def compute(self, x, y):
        ac = self.a.compute(x, y)

        if ac < 0.0:
            return -(abs(ac) ** self.exponent)
        else:
            return ac ** self.exponent

class NegationOperator(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        return -self.a.compute(x, y)

class LeftShiftOperator(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        return (self.a.compute(x, y) * 10.0) % 1.0

class RightShiftOperator(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        return self.a.compute(x, y) / 10.0

class SineOperator(object):
    def __init__(self, a):
        self.a = a
        self.frequency = randomConstant() * math.pi
        self.phase = randomConstant()

    def compute(self, x, y):
        return math.sin((self.frequency * self.a.compute(x, y)) + self.phase)

class CosineOperator(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        return math.cos(self.a.compute(x, y) * math.pi)

class HyperbolicTangentOperator(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        return math.tanh(self.a.compute(x, y))

class SquashOperator(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        ac = self.a.compute(x, y)
        return ac / (abs(ac) + 1.0)

class ArrowOperator(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        return -abs(2.0 * self.a.compute(x, y)) + 1.0

class NoiseOperator(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        return 2.0 * randomNoise((self.a.compute(x, y) + 1.0) / 2.0) - 1.0

class Noise2DOperator(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, x, y):
        return 2.0 * randomNoise2D((self.a.compute(x, y) + 1.0) / 2.0, (self.b.compute(x, y) + 1.0) / 2.0) - 1.0

operationsEnd = [VariableXOperator, VariableYOperator, ConstantOperator]
operations = [AdditionOperator, SubtractionOperator, MultiplicationOperator, ReciprocalOperator, ExponentOperator, NegationOperator, LeftShiftOperator, RightShiftOperator, SineOperator, CosineOperator, HyperbolicTangentOperator, SquashOperator, ArrowOperator, NoiseOperator, Noise2DOperator]

operationsEndLength = len(operationsEnd)
operationsLength = len(operations)

# Generate Operation
def operation(current):
    if current == 0:
        return operationsEnd[random() % operationsEndLength]()
    else:
        nextLevel = current - 1
        currentOperation = operations[random() % operationsLength]

        params = []
        paramsLength = currentOperation.__init__.__code__.co_argcount

        for param in range(paramsLength - 1):
            params.append(operation(nextLevel))

        return currentOperation(*params)
