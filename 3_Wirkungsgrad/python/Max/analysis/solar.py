from labtool_ex2 import Project
from sympy import exp, pi, sqrt, Abs, pi

# from sympy.physics.units.systems.si import elementary_charge, boltzmann_constant
import numpy as np
from scipy.constants import elementary_charge, Boltzmann

# from numpy.typing import NDArray
import pandas as pd
import matplotlib.pyplot as plt  # noqa
import os
from uncertainties import ufloat

# pyright: reportUnboundVariable=false
# pyright: reportUndefinedVariable=false


def Voltmeter(V):
    return abs(V) * 0.0015 + 0.002


def Amperemeter(current):
    return abs(current) * 0.01 + 0.003


def KeithlyVolts(value):
    val = abs(value)
    if val < 0.02:
        return 0.1 / 100 * val + 200e-6
    if val < 0.2:
        return 0.015 / 100 * val + 200e-6
    if val < 2:
        return 0.020 / 100 * val + 300e-6

    return abs(value) * 0.00012


def KeithlyAmps(value):
    val = abs(value)
    if val < 0.00001:
        return 0.025 / 100 * val + 1.5e-9
    if val < 0.0001:
        return 0.020 / 100 * val + 15e-9
    if val < 0.001:
        return 0.020 / 100 * val + 150e-9
    if val < 0.01:
        return 0.020 / 100 * val + 1.5e-6
    if val < 0.1:
        return 0.025 / 100 * val + 15e-6
    if val < 1:
        return 0.067 / 100 * val + 900e-6
    return abs(value) * 0.00012


def createStromSpannungsKennlinie(P: Project, file: str):
    P.figure.clear()
    P.figure.set_size_inches((10, 4))
    P.data = pd.DataFrame(None)
    axs = P.figure.subplots(1, 2)
    ax = axs[0]

    filepath = os.path.join(os.path.dirname(__file__), file)
    P.load_data(filepath, loadnew=True)
    P.vload()
    P.data.loc[:, "dU"] = U.data.apply(Voltmeter)
    P.data.loc[:, "dI"] = I.data.apply(Amperemeter)

    P.vload()

    P.plot(
        ax,
        U,
        I,
        label="Gemessene Daten",
        style="#1cb2f5",
        errors=True,
        marker="o",
        markersize=4,
        markeredgecolor="#1cb2f5",
        markerfacecolor="#1cb2f5",
    )

    power = U * I
    P.resolve(power)
    maxpower = max(power.data)
    pmask = P.data["power"] == maxpower
    umask = P.data["U"] == 0
    imask = P.data["I"] == 0
    maxpower = P.data[pmask]
    kurzSchlussStrom = P.data[umask]
    leerLaufSpannung = P.data[imask]
    ax.plot(
        kurzSchlussStrom.U,
        kurzSchlussStrom.I,
        marker="o",
        markersize=4,
        markeredgecolor="orange",
        markerfacecolor="orange",
        label="Kurzschlussstrom",
        color="None",
    )
    ax.plot(
        leerLaufSpannung.U,
        leerLaufSpannung.I,
        marker="v",
        markersize=4,
        markeredgecolor="blue",
        markerfacecolor="blue",
        label="Leerlaufspannung",
        color="None",
    )
    ax.plot(
        maxpower.U,
        maxpower.I,
        marker="D",
        markersize=4,
        markeredgecolor="red",
        markerfacecolor="red",
        label="MPP",
        color="None",
    )
    ax.legend()
    ax.set_title("Strom-Spannungs-Kennlinie")
    ax = axs[1]
    P.plot(
        ax,
        U,
        power,
        label="Gemessene Daten",
        style="#1cb2f5",
        errors=True,
        marker="o",
        markersize=4,
        markeredgecolor="#1cb2f5",
        markerfacecolor="#1cb2f5",
    )
    ax.plot(
        maxpower.U,
        maxpower.power,
        marker="D",
        markersize=4,
        markeredgecolor="red",
        markerfacecolor="red",
        label="MPP",
        color="None",
    )
    P.data = P.data.u.com
    maxpower = P.data[pmask]
    kurzSchlussStrom = P.data[umask]
    leerLaufSpannung = P.data[imask]
    kv = {
        "pmax": maxpower.power.values[0],
        "umax": maxpower.U.values[0],
        "imax": maxpower.I.values[0],
        "UL": leerLaufSpannung.U.values[0],
        "Ik": kurzSchlussStrom.I.values[0],
        "FF": maxpower.power.values[0]
        / (leerLaufSpannung.U.values[0] * kurzSchlussStrom.I.values[0]),
    }
    print(kv)
    P.add_text(ax, keyvalue=kv, offset=[25, -10], color="#F5560C")
    ax.legend()
    ax.set_title("Leistungkennlinie")
    return ax


def fitPlots(P: Project, file: str, p0, dunkel=False):
    P.figure.clear()
    P.figure.set_size_inches((10, 4))
    P.data = pd.DataFrame(None)
    axs = P.figure.subplots(1, 2)

    filepath = os.path.join(os.path.dirname(__file__), file)
    P.load_data(filepath, loadnew=True)
    P.data.drop(["t", "s"], axis=1, inplace=True)
    P.vload()
    P.data.loc[:, "dU"] = U.data.apply(KeithlyVolts)
    P.data.loc[:, "dI"] = I.data.apply(KeithlyAmps)
    P.data.loc[:, "d_I"] = I.data.apply(KeithlyAmps)
    P.data.loc[:, "_I"] = I.data
    P.data = P.data[P.data["I"] < 0.3998]

    power = U * I
    P.resolve(power)
    maxpower = min(power.data)
    pmask = P.data["power"] == maxpower
    umask = P.data["U"] == 0
    imask = P.data["I"] == 0
    maxpower = P.data[pmask]
    P.vload()

    ax = axs[1]
    P.plot(
        ax,
        U,
        power,
        label="Gemessene Daten",
        style="#1cb2f5",
        errors=True,
        marker="o",
        markersize=4,
        markeredgecolor="#1cb2f5",
        markerfacecolor="#1cb2f5",
    )
    ax.plot(
        maxpower.U,
        maxpower.power,
        marker="D",
        markersize=4,
        markeredgecolor="red",
        markerfacecolor="red",
        label="MPP",
        color="None",
    )
    P.data = P.data.u.com
    maxpower = P.data[pmask]
    kv = {
        "pmax": maxpower.power.values[0],
        "umax": maxpower.U.values[0],
        "imax": maxpower.I.values[0],
        "P0": p0,
        "eta": abs(maxpower.power.values[0]) / p0,
    }
    print(kv)
    P.add_text(ax, keyvalue=kv, offset=[0, 35], color="#F5560C")
    ax.legend()
    ax.set_title("Leistungkennlinie")
    print(P.data)
    P.data = P.data.u.sep
    P.vload()

    ax = axs[0]
    P.plot(
        ax,
        U,
        I,
        label="Gemessene Daten",
        style="#1cb2f5",
        errors=True,
        marker="o",
        markersize=4,
        markeredgecolor="#1cb2f5",
        markerfacecolor="#1cb2f5",
    )

    maxpower = P.data[pmask]
    ax.plot(
        maxpower.U,
        maxpower.I,
        marker="D",
        markersize=4,
        markeredgecolor="red",
        markerfacecolor="red",
        label="MPP",
        color="None",
    )
    P.vload()
    if dunkel:
        P.data = P.data[P.data["U"] > 0.14]
    I = IS1 * (exp(elementary_charge * U / (f1 * Boltzmann * 293.15)) - 1) - Iph
    P.plot_fit(
        axes=ax,
        x=U,
        y=I,
        eqn=I,
        style=r"#0cf574",
        label="Diodenkennlinie",
        offset=[0, 10],
        use_all_known=False,
        guess={
            "f1": 2.0,
            # "T": 300,
            # "f2": 2.0,
            "IS1": 2e-6,
            # "IS2": 5e-6,
            "Iph": 80e-3,
        },
        bounds=[
            {"name": "f1", "min": 0, "max": 4},
            # {"name": "f2", "min": 0, "max": 4},
            # {"name": "T", "min": 293, "max": 400},
            {"name": "IS1", "min": 0, "max": 1},
            {"name": "Iph", "min": -2e-1, "max": 1},
            # {"name": "IS2", "min": 0, "max": 1},
        ],
        add_fit_params=True,
        granularity=10000,
        # gof=True,
        scale_covar=True,
    )
    ax.legend()
    ax.set_title("Strom-Spannungs-Kennlinie")
    return ax


def test_solar_protokoll():
    gm = {
        "U": r"U",
        "UL": r"U_L",
        "I": r"I",
        "_I": r"I",
        "Ik": r"I_k",
        "DT": r"\Delta T",
        "IS1": r"I_{S1}",
        "IS2": r"I_{S2}",
        "Iph": r"I_{ph}",
        "Rs": r"R_{s}",
        "Rp": r"R_{p}",
        "P0": r"P_{0}",
        "T": r"T",
        "f1": r"f_1",
        "f2": r"f_2",
        "t": r"t",
        "power": r"P",
        "pmax": r"P_\text{MPP}",
        "umax": r"U_\text{MPP}",
        "imax": r"I_\text{MPP}",
        "eta": r"\eta",
        "FF": r"FF",
        "eps": r"\epsilon",
    }
    gv = {
        "U": r"\si{\volt}",
        "UL": r"\si{\volt}",
        "I": r"\si{\milli\ampere}",
        "_I": r"\si{\ampere}",
        "Ik": r"\si{\milli\ampere}",
        "t": r"\si{\second}",
        "T": r"\si{\kelvin}",
        "IS1": r"\si{\ampere}",
        "IS2": r"\si{\ampere}",
        "Iph": r"\si{\ampere}",
        "Rs": r"\si{\ohm}",
        "Rp": r"\si{\ohm}",
        "f1": r"1",
        "f2": r"1",
        "P0": r"\si{\watt}",
        "power": r"\si{\milli\watt}",
        "pmax": r"\si{\milli\watt}",
        "umax": r"\si{\volt}",
        "imax": r"\si{\milli\ampere}",
        "DT": r"\si{\kelvin}",
        "FF": r"1",
        "eta": r"1",
        "eps": r"1",
    }

    pd.set_option("display.max_columns", None)
    plt.rcParams["axes.axisbelow"] = True
    P = Project("Solar", global_variables=gv, global_mapping=gm, font=13)
    P.output_dir = "./"
    P.figure.set_size_inches((10, 1))
    ax: plt.Axes = P.figure.add_subplot()
    schieflagedersolarzellen = ufloat(5, 1)  # grad
    quellenAbstand = ufloat(284, 2)  # mm ist Abstand bis Lampenglas
    flaechesolarzelle = ufloat(10 * 8, 1)
    bagedeagtflaechesolarzelle = ufloat(10 * 7, 1)
    # Aufgabe 1
    ax = createStromSpannungsKennlinie(P, "../data/solarSerieOhneAbdeckung.csv")
    P.figure.suptitle("Serienschaltung von Solarzellen")
    P.figure.tight_layout()
    P.print_table(
        U,
        I,
        name="werte_serienschaltung",
        options=r"cells={font=\footnotesize},rowsep=0pt,",
        inline_units=True,
    )
    # P.ax_legend_all(loc=0)
    ax = P.savefig("serienschaltung.pdf")

    # Aufgabe 2
    ax = createStromSpannungsKennlinie(P, "../data/solarParallelOhneAbdeckung.csv")
    P.figure.suptitle("Parallelschaltung von Solarzellen")
    P.figure.tight_layout()
    P.print_table(
        U,
        I,
        name="werte_parallelschaltung",
        options=r"cells={font=\footnotesize},rowsep=0pt,",
        inline_units=True,
    )
    # P.ax_legend_all(loc=0)
    ax = P.savefig("parallelschaltung.pdf")

    # Aufgabe 3
    ax = createStromSpannungsKennlinie(P, "../data/solarSerieMitAbdeckung.csv")
    P.figure.suptitle("Serienschaltung von Solarzellen abgedeckt")
    P.figure.tight_layout()
    # P.ax_legend_all(loc=0)
    P.print_table(
        U,
        I,
        name="werte_abgedeckt",
        options=r"cells={font=\footnotesize},",
        inline_units=True,
    )
    ax = P.savefig("serienschaltungAbgedeckt.pdf")

    P.gv["power"] = r"\si{\watt}"
    P.gv["I"] = r"\si{\ampere}"
    P.gv["imax"] = r"\si{\ampere}"
    P.gv["pmax"] = r"\si{\watt}"
    # Aufgabe 4
    l1 = ufloat(1.7, 0.1) / 100
    l2 = ufloat(3.9, 0.1) / 100
    cellArea = l1 * l2
    print(cellArea)
    durchmesserPower = ufloat(1.8, 0.1) / 100  # hersteller
    powerArea = np.pi * durchmesserPower**2 / 4
    print(powerArea)

    ax = fitPlots(P, "../data/dunkel.csv", p0=0.01 * cellArea, dunkel=True)
    P.figure.suptitle("Dunkelkennlinie")
    P.figure.tight_layout()
    ax = P.savefig("dunkelkennlinie.pdf")

    # Aufgabe 5
    # hellwattlampe = ufloat(0.63, 0.02)
    # hellwattlampe2 = ufloat(3.4, 0.2)

    hellwattlampe = ufloat(0.63, 0.02) / 10
    hellwattlampe2 = ufloat(3.4, 0.2) / 32
    # hellwattlampe = ufloat(0.63, 0.02) / 10
    # # hellwattlampe2 = ufloat(3.4, 0.2) / 10
    # hellwattlampe2 = ufloat(1.2, 0.2) / 10
    hellwattled = ufloat(0.264, 0.003)
    Intensity1 = hellwattlampe / powerArea
    Intensity2 = hellwattlampe2 / powerArea
    Intensity3 = hellwattled / powerArea

    ax = fitPlots(P, "../data/helllampe.csv", p0=Intensity1 * cellArea)
    P.figure.suptitle(
        r"Hellkennlinie @ \SI{"
        + Intensity1.__format__("S")
        + r"}{\watt\per\square\meter}"
    )
    P.figure.tight_layout()
    ax = P.savefig("helllampe.pdf")

    ax = fitPlots(P, "../data/helllampe2.csv", p0=Intensity2 * cellArea)
    P.figure.suptitle(
        r"Hellkennlinie @ \SI{"
        + Intensity2.__format__("S")
        + r"}{\watt\per\square\meter}"
    )
    P.figure.tight_layout()
    ax = P.savefig("helllampe2.pdf")

    ax = fitPlots(P, "../data/hellled.csv", p0=Intensity3 * cellArea)
    P.figure.suptitle(
        r"Hellkennlinie @ \SI{"
        + Intensity3.__format__("S")
        + r"}{\watt\per\square\meter}"
    )
    P.figure.tight_layout()
    ax = P.savefig("hellled.pdf")
    # I = (
    #     IS1 * exp(elementary_charge * (U - _I * RS) / (f1 * boltzmann_constant * T))
    #     + IS2 * exp(elementary_charge * (U - _I * RS) / (f2 * boltzmann_constant * T))
    #     - Iph
    #     + (U - _I * Rs) / Rp
    # )

    # Thomas Monet


if __name__ == "__main__":
    test_solar_protokoll()
