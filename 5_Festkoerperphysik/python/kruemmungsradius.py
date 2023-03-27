import labtool as lt
import matplotlib as mpl
import numpy as np

PLOT = True

# elementary charge
q_e = 1.602176634e-19  # C
# electron mass
m_e = 9.1093837015e-31  # kg

abstand = lt.unp.uarray([5, 10, 15, 20, 25, 30, 35], 2.0) * 1e-3  # m


# def uncertainty_amperage(amperage):
#     if amperage < 0.004:
#         return 0.001 * amperage + 4 * 1e-7
#     elif amperage < 0.4:
#         return 0.001 * amperage + 4 * 1e-5


data_18_1 = np.array([40, 75, 100, 131, 164, 195, 228]) * 1e-3  # A
data_18_2 = np.array([49, 78, 108, 149, 180, 208, 240]) * 1e-3  # A
data_18 = lt.StudentArray([data_18_1, data_18_2])

data_40_1 = np.array([76, 122, 165, 216, 261, 314, 360]) * 1e-3  # A
data_40_2 = np.array([60, 100, 139, 190, 245, 290, 340]) * 1e-3  # A
data_40 = lt.StudentArray([data_40_1, data_40_2])


def calc_radius(auslenkung_s, kolbendurchmesser_d=0.135):
    sin_alpha = auslenkung_s / kolbendurchmesser_d
    l = lt.unp.sqrt(kolbendurchmesser_d**2 - auslenkung_s**2)
    return l / (2 * sin_alpha)


# calc radius
radius = calc_radius(abstand)
for r in radius:
    print(f"{r*100:S}")

# 3.5mm laut Angabe - 4.5mm ca laut bild
# R = 6.8mm laut Angabe
def get_magnetic_field(I, n=320, R=6.8e-2, a=4.5e-2):
    # equation 10
    mu_0 = 4 * np.pi * 1e-7  # H/m
    return mu_0 * n * R**2 * I / (R**2 + a**2) ** (3 / 2)


# calc B
B_18 = get_magnetic_field(data_18.array)  # T
B_40 = get_magnetic_field(data_40.array)  # T

# print like a latex table
print("\nI / mA & B_18 / mT")
for i, b in zip(data_18.array, B_18):
    print(rf"{i*1000:S} & {b*1e3:S} \\")
print("\nI / mA & B_40 / mT")
for i, b in zip(data_18.array, B_40):
    print(rf"{i*1000:S} & {b*1e3:S} \\")


inverse_radius = 1 / radius


def lin_func(x, k):
    return k * x


inverse_radius_n, _ = lt.separate_uarray(inverse_radius)
B_18_n, _ = lt.separate_uarray(B_18)
B_40_n, _ = lt.separate_uarray(B_40)

fit_18 = lt.CurveFit(lin_func, B_18_n, inverse_radius_n)
fit_40 = lt.CurveFit(lin_func, B_40_n, inverse_radius_n)
print(f"Fit 18: {fit_18.p[0]}")
print(f"Fit 40: {fit_40.p[0]}")


def calc_q_spez_from_slope(k, U):
    return 2 * U * k**2


q_sp_18 = calc_q_spez_from_slope(fit_18.p[0], 1.8e3)
q_sp_40 = calc_q_spez_from_slope(fit_40.p[0], 4.0e3)
print(f"q_sp_18:  {q_sp_18:e}")
print(f"q_sp_40:  {q_sp_40:e}")
print(f"q_sp_lit: {q_e/m_e:e}")


if PLOT:
    # plot
    mpl.use("agg")
    mpl.rcParams.update(
        {
            "text.latex.preamble": r"\usepackage{lmodern}\usepackage[locale=DE,uncertainty-mode=separate]{siunitx}\usepackage{nicefrac}"
        }
    )
    lt.plt_latex()
    lt.plt_uplot(B_18 * 1000, inverse_radius, label=r"$\SI{1.8}{\kilo\volt}$")
    lt.plt_uplot(B_40 * 1000, inverse_radius, label=r"$\SI{4.0}{\kilo\volt}$")
    lt.plt.plot(fit_18.x_out * 1000, fit_18.y_out, label=r"$\SI{1.8}{\kilo\volt}$: lineare Regression")
    lt.plt.plot(fit_40.x_out * 1000, fit_40.y_out, label=r"$\SI{1.8}{\kilo\volt}$: lineare Regression")
    lt.plt.ylabel(r"$\frac{1}{r}$ / $\si{\per\meter}$")
    lt.plt.xlabel(r"$B$ / $\si{\milli\tesla}$")
    lt.plt.title("Inverser Krümmungsradius des abgelenkten Elektronenstrahls\nin Abhängigkeit des Magnetfeldes")
    lt.plt.legend()
    lt.plt.grid()
    lt.plt.tight_layout()
    lt.plt.savefig("5_Festkoerperphysik/python/plots/kruemmungsradius.pdf")
