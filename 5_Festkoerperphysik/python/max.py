from labtool_ex2 import Project
from sympy import exp, pi, sqrt, Abs, pi

# from sympy.physics.units.systems.si import elementary_charge, boltzmann_constant
from scipy.constants import elementary_charge, Boltzmann, h, m_e
import numpy as np

# from numpy.typing import NDArray
import pandas as pd
import matplotlib.pyplot as plt  # noqa
import os
from uncertainties import ufloat

# distanzspulen_esp = ufloat(67.3, 0.2)
#
#
# 1.84kV =<F6><F6><F6><F6><F6><F6>

# pyright: reportUnboundVariable=false
# pyright: reportUndefinedVariable=false


def error(U):
    return U * 0.05 + 0.0010


def freqUnsicherheit(f):
    return 0.1


def AmpereLD(x):
    return 0.002


def distanzUnsicherheit(s):
    return 0.0010


def AnodenSpannung(U):
    return 5000 * 0.03


def AmpereTTI(x):
    if x < 0.004:
        return x * 0.001 + 4e-7
    if x < 0.4:
        return x * 0.001 + 4e-5
    if x < 1:
        return x * 0.003 + 1e-3


def test_festkoerper_protokoll():
    gm = {
        "U": r"U",
        "I": r"I",
        "D": r"d",
        "bigD": r"d_\text{Gross}",
        "smallD": r"d_\text{Klein}",
        "nu": r"\nu",
        "s": r"s",
        "g1": r"g_1",
        "g2": r"g_2",
        "lmbd": r"\lambda",
        "H": r"H",
        "B": r"B",
        "repr": r"\frac{1}{r}",
        "espz": r"e_\text{spez}",
        "c": r"c",
        "k": r"k",
    }
    gv = {
        "U": r"\si{\volt}",
        "I": r"\si{\milli\ampere}",
        "s": r"\si{\meter}",
        "nu": r"\si{\mega\hertz}",
        "H": r"\si{\ampere\per\meter}",
        "B": r"\si{\tesla}",
        "bigD": r"\si{\meter}",
        "g1": r"\si{\per\meter}",
        "g2": r"\si{\per\meter}",
        "lmbd": r"\si{\per\meter}",
        "smallD": r"\si{\meter}",
        "repr": r"\si{\per\meter}",
        "espz": r"\si{\coulomb\per\kg}",
        "c": r"\si{\volt\second\per\meter\squared}",
        "k": r"\si{\mega\hertz\per\milli\tesla}",
    }

    pd.set_option("display.max_columns", None)
    plt.rcParams["axes.axisbelow"] = True
    P = Project("Festkoerper", global_variables=gv, global_mapping=gm, font=13)
    P.output_dir = str(os.path.dirname(__file__)) + "/"
    P.figure.set_size_inches((10, 4))
    ax: plt.Axes = P.figure.add_subplot()

    # # Aufgabe 1
    # file = "../data/graphit.csv"
    # filepath = os.path.join(os.path.dirname(__file__), file)
    # P.load_data(filepath, loadnew=True)
    # mask = P.data["D"] > 40.9
    # mask[0] = False
    # bigD = P.data[mask] / 1000
    # smallD = P.data[~mask] / 1000

    # # print(bigD.groupby(["U"]).mean())
    # # print(bigD.groupby(["U"]).sem())
    # # print(smallD.groupby(["U"]).mean())
    # # print(smallD.groupby(["U"]).sem())
    # # print(smallD.groupby(["U"]).sem().index.values)
    # P.data = pd.DataFrame()
    # P.data["bigD"] = bigD.groupby(["U"]).mean()
    # P.data["dbigD"] = bigD.groupby(["U"]).sem()
    # P.data["smallD"] = smallD.groupby(["U"]).mean()
    # P.data["dsmallD"] = smallD.groupby(["U"]).sem()
    # P.data["dsmallD"] = smallD.groupby(["U"]).sem()
    # P.data["U"] = smallD.groupby(["U"]).sem().index.values * 1e6
    # P.data["dU"] = P.data["U"].apply(AnodenSpannung)
    # P.data = P.data.reset_index(drop=True)
    # P.vload()
    # print(P.data)

    # lmbda = h / sqrt(2 * m_e * elementary_charge * U)

    # P.resolve(lmbda)

    # g1 = 4 * 0.0675 / bigD * lmbda
    # g2 = 4 * 0.0675 / smallD * lmbda

    # P.resolve(g1)
    # P.resolve(g2)

    # print(P.data)
    # print(g1.data.mean())
    # print(g1.data.sem())
    # print(g2.data.mean())
    # print(g2.data.sem())

    # Aufgabe 2
    # file = "../data/kruemmung.csv"
    file = "../data/kruemmung_our.csv"
    filepath = os.path.join(os.path.dirname(__file__), file)
    P.load_data(filepath, loadnew=True)
    P.data.loc[:, "s"] = s.data / 1000
    P.data.loc[:, "U"] = U.data * 1000
    P.data.loc[:, "dU"] = U.data.apply(AnodenSpannung)
    P.data.loc[:, "dI"] = I.data.apply(AmpereTTI)
    P.data.loc[:, "ds"] = s.data.apply(distanzUnsicherheit)
    two_a = ufloat(0.09331, 0.004)
    # !!!!!!!!! Abstand mitte zu mitte war falsch eingestellt
    R = ufloat(0.068, 0.001)
    f = 320 * R**2 * (R**2 + (two_a / 2) ** 2) ** (-3 / 2)
    d = ufloat(0.135, 0.0005)

    P.data = P.data.u.com
    P.data["B"] = f * I.data * 1.25663706212e-06
    P.data["repr"] = 2 * s.data / (d * (d**2 - s.data**2) ** (0.5))
    print(P.data)
    P.data = P.data.u.sep

    P.plot_data(
        ax,
        repr,
        B,
        label="Gemessene Daten",
        style="#ad0afd",
        errors=True,
    )

    B = sqrt(2 * U.data.values[0] / espz) * repr

    P.plot_fit(
        axes=ax,
        x=repr,
        y=B,
        eqn=B,
        style=r"#ad0afd",
        label=r"$U_A  @\SI{4.01(15)}{\kilo\volt}$",
        offset=[0, 40],
        use_all_known=False,
        guess={
            "espz": 1e10,
        },
        bounds=[
            {"name": "espz", "min": 0.01, "max": 1e13},
        ],
        add_fit_params=True,
        granularity=10000,
        # gof=True,
        scale_covar=True,
    )
    P.vload()

    file = "../data/kruemmung2.csv"
    filepath = os.path.join(os.path.dirname(__file__), file)
    P.load_data(filepath, loadnew=True)
    P.data.loc[:, "s"] = s.data / 1000
    P.data.loc[:, "U"] = U.data * 1000
    P.data.loc[:, "dU"] = U.data.apply(AnodenSpannung)
    P.data.loc[:, "dI"] = I.data.apply(AmpereTTI)
    P.data.loc[:, "ds"] = s.data.apply(distanzUnsicherheit)
    two_a = ufloat(0.09331, 0.004)
    R = ufloat(0.068, 0.001)
    f = 320 * R**2 * (R**2 + (two_a / 2) ** 2) ** (-3 / 2)
    d = ufloat(0.135, 0.0005)

    P.data = P.data.u.com
    P.data["B"] = f * I.data * 1.25663706212e-06
    P.data["repr"] = 2 * s.data / (d * (d**2 - s.data**2) ** (0.5))
    print(P.data)
    P.data = P.data.u.sep

    P.plot_data(
        ax,
        repr,
        B,
        label="Gemessene Daten",
        style="#f49004",
        errors=True,
    )

    B = sqrt(2 * U.data.values[0] / espz) * repr

    P.plot_fit(
        axes=ax,
        x=repr,
        y=B,
        eqn=B,
        style=r"#f49004",
        label=r"$U_A @\SI{3.00(15)}{\kilo\volt}$",
        offset=[0, 60],
        use_all_known=False,
        guess={
            "espz": 1e10,
        },
        bounds=[
            {"name": "espz", "min": 0.01, "max": 1e13},
        ],
        add_fit_params=True,
        granularity=10000,
        # gof=True,
        scale_covar=True,
    )
    P.figure.suptitle("Fit Spezifischer Elektronenmasse")
    P.figure.tight_layout()
    P.ax_legend_all(loc=4)
    ax = P.savefig("spezifischeElektronenMasseFit.pdf")
    #
    # # Aufgabe 3
    # P.vload()
    #
    # file = "../data/esr.csv"
    # filepath = os.path.join(os.path.dirname(__file__), file)
    # P.load_data(filepath, loadnew=True)
    # P.data.loc[:, "dI"] = I.data.apply(AmpereLD)
    # P.data.loc[:, "dnu"] = nu.data.apply(freqUnsicherheit)
    #
    # P.gv["B"] = r"\si{\milli\tesla}"
    # P.data = P.data.u.com
    # P.data["B"] = 4.23 * I.data * 0.068 / ufloat(0.087, 0.003)
    # print(P.data)
    # P.data = P.data.u.sep
    #
    # P.plot_data(
    #     ax,
    #     B,
    #     nu,
    #     label="Gemessene Daten",
    #     style="#ad0afd",
    #     errors=True,
    # )
    #
    # nu = k * B
    #
    # vals = P.plot_fit(
    #     axes=ax,
    #     x=B,
    #     y=nu,
    #     eqn=nu,
    #     style=r"#ad0afd",
    #     label=r"Landé Faktor",
    #     offset=[0, 40],
    #     use_all_known=False,
    #     guess={
    #         "k": 2.9e1,
    #     },
    #     bounds=[
    #         {"name": "k", "min": 1e1, "max": 1e3},
    #     ],
    #     add_fit_params=True,
    #     granularity=10000,
    #     # gof=True,
    #     scale_covar=True,
    # )
    # g = ufloat(vals["k"].value, vals["k"].stderr) * 1e9 * h / (9.273e-24)
    # print(f"Landé Faktro: {g=}")
    #
    # P.figure.suptitle(
    #     "Bestimmung des Landé Faktor von DPPH \n mittels der Frequenzabhängigkeit des Resonanzmagnetfeldes"
    # )
    # P.figure.tight_layout()
    # P.ax_legend_all(loc=4)
    # ax = P.savefig("esr.pdf")


if __name__ == "__main__":
    test_festkoerper_protokoll()
