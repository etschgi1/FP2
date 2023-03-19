from numpy import *
import numpy as np
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
import math as m

lam = 532 * 10 ** (-9)
z = 260.5 * 10 ** (-2)
dz = 0.5 * 10 ** (-2)
dx = 0.01 * 10 ** (-2)
spalta = [
    0.25 * 10 ** (-3),
    0.25 * 10 ** (-3),
    0.5 * 10 ** (-3),
    1.00 * 10 ** (-3),
]  # Spaltabstand d
spaltb = [
    0.2 * 10 ** (-3),
    0.1 * 10 ** (-3),
    0.1 * 10 ** (-3),
    0.1 * 10 ** (-3),
]  # Spaltbreite D

# Formel anlegen für theoretische Berechnung von Interferenz und Beugung
def calcint(x, d):
    return 0.5 * (1 + cos((2 * pi * x * d) / (lam * z)))


def calcbeug(x, D):
    return sin(pi * x * D / (lam * z)) ** 2 / (pi * x * D / (lam * z)) ** 2


# Maximum der Intensitätsverteilung finden
def findmax(graustufe):
    gmax = graustufe[600]
    for i in range(600, 650):
        if graustufe[i] > gmax:
            gmax = graustufe[i]
    return gmax


# Normierung der I n t e n s i t t auf 1
def scaledgrau(graustufe):
    scaledg = []
    faktor = 1 / findmax(graustufe)
    for i in range(len(graustufe)):
        scaledg.append(graustufe[i] * faktor)
    return scaledg


def main() -> None:
    i = 3
    xtheo = np.linspace(-4e-2, 4e-2, 1000)
    interferenz = calcint(xtheo, spalta[i])
    beugung = calcbeug(xtheo, spaltb[i])
    intbeug = beugung * interferenz
    plt.plot(xtheo, intbeug, color="green", label="Theoretischer Verlauf")
    plt.show()


if __name__ == "__main__":
    main()
