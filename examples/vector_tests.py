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

class Vector:
    def __init__(self, x, y):
        self.x=x
        self.y=y
    
    def length(self):
        return sqrt(self.x*self.x+self.y*self.y)

    def unit(self):
        length=self.length()
        # oczywiście tutaj jest błąd - brak sprawdzenia length!=0
        # niestety testy tego nie złapały co tylko jeden rodzaj testów nie wystarcza
        return Vector(self.x/length, self.y/length)

    def __eq__(self, other):
        return close(self.x, other.x) and close(self.y, other.y)   

print("chosen points test:")
assert(close(Vector(3, 4).length(), 5))
assert(close(Vector(1, 1).length(), sqrt(2)))
assert(Vector(1, 0).unit()==Vector(1, 0))
assert(close(Vector(2, 0).length(), 2))

print("random tests:")
for i in range(1000):
    def random_coordinate():
        value=random()
        multiplier=1000
        # change this to value<0.1 to catch (0, 0)
        if value<0.01:
            return 0
        return (value-0.5)*1000
    x=random_coordinate()
    y=random_coordinate()
    print(f"test x={x} \t y={y}")
    
    def vector_length(sign_x, sign_y):
        return Vector(sign_x*x, sign_y*y).length()

    def unit_vector_length(sign_x, sign_y):
        return Vector(sign_x*x, sign_y*y).unit().length()

    signs=[(1, 1), (-1, 1), (1, -1), (-1, -1)]

    def all_close(previous, current):
        # ważne, przy operacjach na floatach występują błedy
        assert(close(previous, current))
        return current

    # wektory o różnych znakach x, y powinny mieć tą samą długość
    reduce(all_close, starmap(vector_length, signs))
    # wektor jednostkowy ma długość jeden
    # tutaj testujemy też przejście przez metody pomocnicze
    reduce(all_close, starmap(unit_vector_length, signs))

print("characteristic points test:")
assert(Vector(0, 1).unit().length()==1)
assert(Vector(1, 0).unit().length()==1)
assert(Vector(0, 0).unit().length()==1)