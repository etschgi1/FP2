from labtool_ex2 import Project
from sympy import exp, pi, sqrt, Abs, conjugate, pi, acos, asin, atan
import numpy as np
from numpy.typing import NDArray
import pandas as pd
import matplotlib.pyplot as plt  # noqa
import os
from uncertainties import ufloat

# pyright: reportUnboundVariable=false
# pyright: reportUndefinedVariable=false


def Thermometer(T):
    return T * 0 + 0.10


def MachoMeter(T):
    return T * 0 + 0.10


def ChronometerHand(t):
    return t * 0 + 2


def Chronometer(t):
    return t * 0 + 0.002


def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial

    try:
        window_size = np.abs(int(window_size))
        order = np.abs(int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order + 1)
    half_window = (window_size - 1) // 2
    # precompute coefficients
    b = np.mat(
        [[k**i for i in order_range] for k in range(-half_window, half_window + 1)]
    )
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs(y[1 : half_window + 1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window - 1 : -1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve(m[::-1], y, mode="valid")


# Eisbildung fehler isolation


def test_waermepumpe_protokoll():
    gm = {
        "pk": r"p_k",
        "pw": r"p_w",
        "Tw": r"T_k",
        "Tk": r"T_w",
        "DT": r"\Delta T",
        "t": r"t",
        "eta": r"\eta",
        "eps": r"\epsilon",
        "epsMax": r"\epsilon_\text{max}",
    }
    gv = {
        "pk": r"\si{\bar}",
        "pw": r"\si{\bar}",
        "Tw": r"\si{\degreeCelsius}",
        "Tk": r"\si{\degreeCelsius}",
        "t": r"\si{\second}",
        "DT": r"\si{\kelvin}",
        "eta": r"1",
        "eps": r"1",
        "epsMax": r"1",
    }

    pd.set_option("display.max_columns", None)
    plt.rcParams["axes.axisbelow"] = True
    P = Project("Waermepumpe", global_variables=gv, global_mapping=gm, font=13)
    P.output_dir = "./"
    P.figure.set_size_inches((8, 6))
    ax: plt.Axes = P.figure.add_subplot()

    # Aufgabe 3
    filepath = os.path.join(os.path.dirname(__file__), "../data/waermeDruck.csv")
    P.load_data(filepath, loadnew=True)

    P.data["dpk"] = P.data["pk"].apply(MachoMeter)
    P.data["dpw"] = P.data["pw"].apply(MachoMeter)
    P.data["dt"] = P.data["t"].apply(ChronometerHand)

    P.plot(
        ax,
        t,
        pk,
        label="Gemessene Daten",
        style="#1cb2f5",
        errors=True,
        marker="o",
        markersize=4,
        markeredgecolor="#1cb2f5",
        markerfacecolor="#1cb2f5",
    )
    P.plot(
        ax,
        t,
        pw,
        label="Gemessene Daten",
        style="#F5460C",
        errors=True,
        marker="o",
        markersize=4,
        markeredgecolor="#F5460C",
        markerfacecolor="#F5460C",
    )

    P.print_table(
        t,
        pk,
        pw,
        name="werte_druck",
        options=r"cells={font=\footnotesize},rowsep=0pt,",
        inline_units=True,
    )
    P.figure.suptitle(r"Druckverlauf")
    P.figure.tight_layout()
    P.ax_legend_all(loc=7)
    ax = P.savefig("pressureProfile.pdf")

    filepath = os.path.join(os.path.dirname(__file__), "../data/waerme.csv")

    P.load_data(filepath, loadnew=True)

    P.data["dTk"] = P.data["Tk"].apply(Thermometer)
    P.data["dTw"] = P.data["Tw"].apply(Thermometer)
    P.data["dDT"] = P.data["DT"].apply(Thermometer)
    P.data["DT"] = -1 * savitzky_golay(P.data["DT"].values, 551, 3)
    P.data["dt"] = P.data["t"].apply(Chronometer)

    P.plot(
        ax,
        t,
        Tk,
        label="Gemessene Daten",
        style="#1cb2f5",
        errors=True,
        marker="o",
        markersize=4,
        markeredgecolor="#1cb2f5",
        markerfacecolor="#1cb2f5",
    )
    P.plot(
        ax,
        t,
        Tw,
        label="Gemessene Daten",
        style="#F5460C",
        errors=True,
        marker="None",
    )

    P.figure.suptitle(r"Temperaturverlauf")
    P.figure.tight_layout()
    P.ax_legend_all(loc=7)
    ax = P.savefig("temperatureProfile.pdf")
    P.figure.set_size_inches((11, 4))
    # ax: plt.Axes = P.figure.add_subplot()

    kuebelvolumen = ufloat(4, 0.020)
    leistungKompressor = ufloat(118, 2)

    eps_ = (
        4190
        * kuebelvolumen
        / leistungKompressor
        * np.gradient(savitzky_golay(P.data["Tw"].values, 501, 3), P.data["t"].values)
    )
    P.data = P.data.u.com
    print(eps_)
    P.data.drop(["T_3", "T_4"], axis=1, inplace=True)
    P.data = P.data.u.sep
    print(P.data)
    # print(eps_.nominal_value)
    P.data["eps"] = eps_
    print(P.data)
    # P.data = P.data.u.com
    P.data = P.data.u.sep

    P.plot(
        ax,
        DT,
        eps,
        label="Gemessene Daten",
        style="#F5459C",
        errors=True,
        marker="None",
    )
    P.figure.suptitle(r"Leistungszahl der Wärmepumpe")
    P.figure.tight_layout()
    ax = P.savefig("leistungszahlVerlauf.pdf")
    P.data = P.data.u.com
    param = {
        "epsMax": 1
        / (1 - (min(Tk.data.values) + 273.15) / (max(Tw.data.values) + 273.15))
    }
    print(1 / (1 - (min(Tk.data.values) + 273.15) / (max(Tw.data.values) + 273.15)))

    P.data["eta"] = eps.data * (
        1 - (min(Tk.data.values) + 273.15) / (max(Tw.data.values) + 273.15)
    )
    P.data = P.data.u.sep

    P.plot(
        ax,
        DT,
        eta,
        label="Gemessene Daten",
        style="#A5459C",
        errors=True,
        marker="None",
    )
    P.add_text(ax, keyvalue=param, offset=[75, 60], color="#A5459C")
    P.figure.suptitle(r"Wirkungsgrad der Wärmepumpe")
    P.figure.tight_layout()
    ax = P.savefig("wirkungsgradVerlauf.pdf")

    # print(np.gradient(savitzky_golay(P.data["Tw"].values.nomi, 251, 3), P.data["t"].values))


if __name__ == "__main__":
    test_waermepumpe_protokoll()
