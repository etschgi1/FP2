import labtool as lt
import numpy as np

diameter = lt.u.ufloat(17.0e-3, 2e-4)  # m


def area(d):
    return np.pi * d**2 / 4


goal = 1000  # W/m²
factor = 0.1

print(goal * area(diameter))
print(goal * area(diameter) / factor)
