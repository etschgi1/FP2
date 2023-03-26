import labtool as lt
import numpy as np
abstand = lt.unp.uarray([0, 5, 10, 15, 20, 25, 30, 35], 0.5) * 1e-3  # m


def uncertainty_amperage(amperage):
    if amperage < 0.004:
        return 0.001 * amperage + 4 * 1e-7
    elif amperage < 0.4:
        return 0.001 * amperage + 4 * 1e-5


data_18_1 = np.array([0.5, 40, 75, 100, 131, 164, 195, 228]) * 1e-3  # A
data_18_2 = np.array([0.5, 49, 78, 108, 149, 180, 208, 240]) * 1e-3  # A

data_18_1 = lt.unp.uarray(
    data_18_1, [uncertainty_amperage(x) for x in data_18_1])
data_18_2 = lt.unp.uarray(
    data_18_2, [uncertainty_amperage(x) for x in data_18_2])

data_40_1 = np.array([0.5, 76, 122, 165, 216, 261, 314, 360]) * 1e-3  # A
data_40_2 = np.array([0.5, 60, 100, 139, 190, 245, 290, 340]) * 1e-3  # A

data_40_1 = lt.unp.uarray(
    data_40_1, [uncertainty_amperage(x) for x in data_40_1])
data_40_2 = lt.unp.uarray(
    data_40_2, [uncertainty_amperage(x) for x in data_40_2])

data_18 = np.mean([data_18_1, data_18_2], axis=0)
data_40 = np.mean([data_40_1, data_40_2], axis=0)


def calc_radius(auslenkung, kolbendurchmesser=0.135):
    alpha = np.arcsin(auslenkung / kolbendurchmesser)
    l = np.sqrt(kolbendurchmesser**2 - auslenkung**2)
    # ????
