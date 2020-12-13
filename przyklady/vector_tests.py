from math import sqrt
from random import seed, random
from itertools import starmap
from functools import reduce

# testy powinny być determinystyczne
seed(123)

# ważne: przy operacjach na floatach występują błedy
def close(a, b):
    EPSILON=0.001
    return abs(a-b)<EPSILON

def division_or_zero(divided, divider):
    if divider==0:
        return 0
    else:
        return divided/divider

class Vector:
    def __init__(self, x, y):
        self.x=x
        self.y=y
    
    @property
    def length(self):
        return sqrt(self.x*self.x+self.y*self.y)

    def normalized(self):
        length=self.length
        # celowy bład który będziemy próbować złapać
        # if length==0:
        #     return Vector(0, 0)
        return Vector(self.x/length, self.y/length)

    def __eq__(self, other):
        return close(self.x, other.x) and close(self.y, other.y)   

print("chosen points test:")
assert(close(Vector(3, 4).length, 5))
assert(close(Vector(1, 1).length, sqrt(2)))
assert(Vector(1, 0).normalized()==Vector(1, 0))
assert(close(Vector(100, 5).normalized().length, 1))
assert(close(Vector(2, 0).length, 2))

print("random tests:")
for i in range(1000):
    def random_coordinate():
        value=random()
        multiplier=1000
        # po zmianie na value<0.1 przypadek (0, 0) zostanie złapany
        if value<0.01:
            return 0
        return (value-0.5)*1000
    x=random_coordinate()
    y=random_coordinate()
    print(f"test x={x} \t y={y}")

    signs=[(1, 1), (-1, 1), (1, -1), (-1, -1)]
    
    def vector_length(sign_x, sign_y):
        return Vector(sign_x*x, sign_y*y).length

    def all_close(previous, current):
        # ważne, przy operacjach na floatach występują błedy
        assert(close(previous, current))
        return current

    # wektory o różnych znakach x, y powinny mieć tą samą długość
    reduce(all_close, starmap(vector_length, signs))
    
    for sign_x, sign_y in signs:
        original=Vector(sign_x*x, sign_y*y)
        normalized=original.normalized()
        # length of one
        assert(close(normalized.length, 1))
        # same direction
        assert(close(
            division_or_zero(original.x, original.y), 
            division_or_zero(normalized.x, normalized.y)))

print("characteristic points test:")
assert(Vector(0, 1).normalized().length==1)
assert(Vector(1, 0).normalized().length==1)
assert(Vector(0, 0).normalized().length==1)