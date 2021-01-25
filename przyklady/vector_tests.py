"""
Contains Vector class and it's tests.
"""

from math import sqrt
from random import seed, random
from termcolor import cprint

# IMPORTANT: tests determinism
seed(123)

def print_test_name(name):
    cprint(f"\n{name}:", attrs=["underline"])

def end_test():
    """
    Prints a message at the end of a test.
    """
    cprint("test passed", "green")

def close(a, b):
    """
    Correct way of comparing two floats.

    Returns:
        True if two float values are close to each other.
    """
    EPSILON=0.001
    return abs(a-b)<EPSILON

def division_or_zero(divided, divider):
    """
    Returns:
        divided/divider if divider is not zero, else zero
    """
    if divider!=0:
        return divided/divider
    else:
        return 0
        
class Vector:
    """Represents geometric structure of vector.

    Attributes:
        x: x coordinate
        y: y coordinate
    """
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

def chosen_points_tests():
    """
    Uses points picked by the class author to test it.
    """
    print_test_name("chosen points test")
    assert(close(Vector(3, 4).length, 5))
    assert(close(Vector(1, 1).length, sqrt(2)))
    assert(Vector(1, 0).normalized()==Vector(1, 0))
    assert(close(Vector(100, 5).normalized().length, 1))
    assert(close(Vector(2, 0).length, 2))
    end_test()

TESTED_COUNT=500

def random_coordinates():
    """
    Returns: 
        iterator over random coordinates in range <0, 1000>.
    """
    for _ in range(TESTED_COUNT):
        def random_coordinate():
            """
            Returns:
                Random coordinate used for testing, in range <0, 1000>.
            """
            value=random()
            multiplier=1000
            # after changing to value<0.1 (0, 0) case will be catched
            if value<0.01:
                return 0
            return (value-0.5)*multiplier
        yield (random_coordinate(), random_coordinate())

def apply_signs_combinations(x, y):
    """
    Returns:
        Iterator over x and y combined with all possible signs
    """
    # all possible signs of coordinate
    signs=[(1, 1), (-1, 1), (1, -1), (-1, -1)]
    for sign_x, sign_y in signs:
        yield (sign_x*x, sign_y*y)

def random_length_tests():
    """
    Tests vector.length property over random coordinates.
    """
    print_test_name("random length tests")
    for x, y in random_coordinates():
        print(f"test x={x} \t y={y}")
        # check if vectors with different coordinate signs
        # have the same length
        previous=None
        for x, y in apply_signs_combinations(x, y):
            current=Vector(x, y).length
            if previous!=None:
                assert(close(current, previous))
            previous=current

def random_normalized_tests():
    """
    Tests vector.normalized() method over random coordinates.
    """
    print_test_name("random normalized tests")
    for x, y in random_coordinates():
        # check if normalized vector has length of one
        # and same direction
        for x, y in apply_signs_combinations(x, y):
            original=Vector(x, y)
            normalized=original.normalized()
            # length of one
            assert(close(normalized.length, 1))
            # same direction
            assert(close(
                division_or_zero(original.x, original.y), 
                division_or_zero(normalized.x, normalized.y)))
    end_test()

def characteristic_points_test():
    """
    Uses coordinates containing zeros to check if the class handles them correctly.
    """
    print_test_name("characteristic points test")
    assert(Vector(0, 1).normalized().length==1)
    assert(Vector(1, 0).normalized().length==1)
    assert(Vector(0, 0).normalized().length==1)
    end_test()

# if module is executed as a script run the tests
if __name__ == '__main__':
    chosen_points_tests()
    random_length_tests()
    random_normalized_tests()
    characteristic_points_test()