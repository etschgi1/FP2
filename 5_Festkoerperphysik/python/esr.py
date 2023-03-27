import labtool as lt
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.optimize as opt

B_FELD_ABSCHWÄCHUNG = 0.89
# Auftrag 1: Bestimmung des Resonanzmagnetfeldes B0 in Abhängigkeit von der gewählten Resonanzfrequenz
# Auftrag 2: Bestimmung des Landé-Faktors von DPPH

# DATA
# Spule;f/MHz;I=/mA;
# klein;120.0;1133;
# klein;110;1031;
# klein;100;951;
# klein;90;845;
# klein;80.1;757;
# klein;70;666;
# klein;60;567;
# mittel;50.1;485;
# mittel;40.1;386;
# mittel;35.1;338;
# mittel;30;290;
# groß;25;242;
# groß;20;168;

data = pd.read_csv("5_Festkoerperphysik/data/esr.csv", sep=";")
mu_0 = 4 * np.pi * 1e-7


def calc_B(I, n=320, r=6.8e-2):  # 7.6e-2): # info mit 7.6e-2 kommt ma hin
    # r = lt.u.ufloat(r, 0.1e-2)
    return I * mu_0 * (4 / 5) ** (3 / 2) * n / r


amp = data["I=/mA"].to_numpy()
# amp = lt.unp.uarray(amp, [0.01] * len(amp))
data["B/mT"] = calc_B(amp / 1e3) * 1e3
b_field = data["B/mT"].to_numpy()
freq = data["f/MHz"].to_numpy()
b_field = b_field * B_FELD_ABSCHWÄCHUNG
# print(b_field)
# exit()
mpl.use("agg")
mpl.rcParams.update(
    {
        "text.latex.preamble": r"\usepackage{lmodern}\usepackage[locale=DE,uncertainty-mode=separate]{siunitx}\usepackage{nicefrac}"
    }
)


def lin_func(x, k):
    return k * x


# regression
x = np.linspace(0, max(b_field), 100)
res, var = opt.curve_fit(lin_func, b_field, freq)
res = lt.u.ufloat(res, np.sqrt(np.diag(var)))
print(res)
lt.plt_latex()
lt.plt.plot(b_field, freq, "x", label="Messwerte")
y = lin_func(x, res)
lt.plt_uplot(x, y, label="Regression")

lt.plt.xlabel(r"$f\:/\: \si{\mega\hertz}$")
lt.plt.ylabel(r"$B\:/\: \si{\milli\tesla}$")
lt.plt.tight_layout()
lt.plt.grid()
lt.plt.title("Resonsanzfrequenz in Abhängigkeit des Magnetfelds (DPPH)")
lt.plt.text(0.66 * max(x), 0.5 * max(freq), (r"Fit: $f = " + f"{res:S}" + " \cdot B$"))
# lt.plt.show()
# calc g
h = 6.62607015e-34  # J*s
mu_b = 9.274009994e-24  # J/T


def g(fit_param):
    return h / mu_b * fit_param * 1e9


g_ = g(res)
print(f"g = {g_:S}")

if g_ > 1.95:
    print("B-mod:")
    print(b_field)
    lt.plt.savefig("5_Festkoerperphysik/python/plots/esr_red_magnetic_field.pdf")
    lt.plt.savefig("5_Festkoerperphysik/python/plots/esr_red_magnetic_field.png")
else:
    lt.plt.savefig("5_Festkoerperphysik/python/plots/esr.pdf")
    lt.plt.savefig("5_Festkoerperphysik/python/plots/esr.png")
print(data.to_latex())
