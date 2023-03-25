import labtool as lt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Beschleunigungsspannung/kV;1.Maxima/mm;1.Maxima/mm;2.Maxima/mm;2.Maxima/mm
# 2;17;17;31;30;
# 2.5;15;15;27;26;
# 3;13;13;24;24;
# 3.5;12;13;21;24;
# 4;11;12;20;22;
# info die unsicherheit ist mal geschätzt :)
Us = lt.unp.uarray([2, 2.5, 3, 3.5, 4], 0.02) * 1000  # V
data = np.array([[17, 17, 31, 30], [15, 15, 27, 26], [
    13, 13, 24, 24], [12, 13, 21, 24], [11, 12, 20, 22]]) * 1e-3  # m
data = lt.unp.uarray(data, 1e-3)  # m
means = [(sum(sublist[:2]) / 2, sum(sublist[-2:]) / 2) for sublist in data]
diffs = [abs(sublist[0] - sublist[1]) for sublist in means]
print(diffs)

m_elec = 9.10938356e-31  # kg
q_elec = 1.60217662e-19  # C
h = 6.62607015e-34  # J*s


def wavelength(U, m_e=m_elec, q_e=q_elec):
    return h / (2 * m_e * q_e * U)**0.5


wavelengths = []
print("Wellenlängen für verschiedene Spannungen LATEX")
print(r"$U_B$ / kV & $\lambda$ / m \\\\")
for u in Us:
    wl = wavelength(u)
    wavelengths.append(wl)
    print(f"{u} & {wl} \\\\")

print("Graphit Gitterabstand")
d_lat_lit = 2.46e-10  # m
d_vert_lit = 6.88e-10  # m

# Näherungsformel


def d_graph(r, lambda_, R=67.5e-3, n=1):
    # r ist der gemessene Abstand zwischen den beiden Maxima
    return 2 * R / r * n * lambda_


d1_res, d2_res = [], []
for wl in wavelengths:
    d1_res += [d_graph(r[0], wl) for r in means]
    d2_res += [d_graph(r[1], wl) for r in means]
d1_res = np.array(d1_res)
d2_res = np.array(d2_res)
stat_d1 = lt.Student([x.n for x in d1_res], sigma=2)
stat_d2 = lt.Student([x.n for x in d2_res], sigma=2)
print("\n\n+++++++++++++++++++++++++++++++\nGitterabstände 2-sigma Intervall - Student T-Verteilung")
print(stat_d1)
print(stat_d2)
