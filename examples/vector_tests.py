from math import sqrt
from random import random
from itertools import starmap
from functools import reduce

EPSILON=0.001

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
        return self.x==other.x and self.y==other.y

for i in range(1000):
    def random_coordinate():
        value=random()
        multiplier=1000
        # if value<0.1:
        #     return 0
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
        assert(abs(previous-current)<EPSILON)
        return current

    # wektory o różnych znakach x, y powinny mieć tą samą długość
    reduce(all_close, starmap(vector_length, signs))
    # wektor jednostkowy ma długość jeden
    # tutaj testujemy też przejście przez metody pomocnicze
    reduce(all_close, starmap(unit_vector_length, signs))

print("data tests finished")
# print("characteristic points test:")

# błąd wyszedł dopiero na teście punktów charakterystycznych dziedziny
# assert(Vector(0, 1).unit().length()==1)
# assert(Vector(1, 0).unit().length()==1)
# assert(Vector(0, 0).unit().length()==1)