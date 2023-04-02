import labtool as lt
import matplotlib as mpl
import numpy as np

# elementary charge
q_e = 1.602176634e-19  # C

# electron mass
m_e = lt.u.ufloat_fromstr("9.1093837015(28)e-31")  # kg


def calc_radius(s, d=0.135):
    one_over_sin_alpha = d / s
    l = lt.unp.sqrt(d**2 - s**2)  # type: ignore
    return 0.5 * l * one_over_sin_alpha


def get_magnetic_field(I, a, n=320, R=8.8e-2):
    # equation 10
    mu_0 = 4 * np.pi * 1e-7  # H/m
    return mu_0 * n * R**2 * I * (R**2 + a**2) ** -1.5


def plot_r_inverse(inverse_radius, B_18, B_40, fit_18, fit_40):
    mpl.use("agg")
    lt.plt_latex()
    lt.plt_uplot(B_18 * 1000, inverse_radius, label=r"$\SI{1.8}{\kilo\volt}$")
    lt.plt_uplot(B_40 * 1000, inverse_radius, label=r"$\SI{4.0}{\kilo\volt}$")
    lt.plt.plot(fit_18.x_out * 1000, fit_18.y_out, label=r"lineare Regression $\SI{1.8}{\kilo\volt}$")
    lt.plt.plot(fit_40.x_out * 1000, fit_40.y_out, label=r"lineare Regression $\SI{4.0}{\kilo\volt}$")
    ax = lt.plt.gca()
    ax.text(
        x=0.98,
        y=0.05,
        s=r"$q_{\text{spez},\SI{1.8}{\kilo\volt}} = \SI{" + f"{fit_18.pu[0]:S}" + r"}{\coulomb\per\kilo\gram}$"
        "\n"
        r"$q_{\text{spez},\SI{4.0}{\kilo\volt}} = \SI{" + f"{fit_40.pu[0]:S}" + r"}{\coulomb\per\kilo\gram}$",
        transform=ax.transAxes,
        horizontalalignment="right",
        verticalalignment="bottom",
        bbox=dict(alpha=0.5, facecolor="white"),
    )
    lt.plt.ylabel(r"$\frac{1}{r}$ / $\si{\per\meter}$")
    lt.plt.xlabel(r"$B$ / $\si{\milli\tesla}$")
    lt.plt.title("Inverser Krümmungsradius des abgelenkten Elektronenstrahls\nin Abhängigkeit des Magnetfeldes")
    lt.plt.legend()
    lt.plt.grid()
    lt.plt.tight_layout()
    lt.plt.savefig("5_Festkoerperphysik/python/plots/kruemmungsradius.pdf")
    print("saved kruemmungsradius.pdf")
    lt.plt.close()


def plot_B(inverse_radius, B_18, B_40, fit_18, fit_40):
    mpl.use("agg")
    lt.plt_latex()
    lt.plt_uplot(inverse_radius, B_18 * 1000, label=r"$\SI{1.8}{\kilo\volt}$")
    lt.plt_uplot(inverse_radius, B_40 * 1000, label=r"$\SI{4.0}{\kilo\volt}$")
    lt.plt.plot(fit_18.x_out, fit_18.y_out * 1000, label=r"lineare Regression $\SI{1.8}{\kilo\volt}$")
    lt.plt.plot(fit_40.x_out, fit_40.y_out * 1000, label=r"lineare Regression $\SI{4.0}{\kilo\volt}$")
    ax = lt.plt.gca()
    ax.text(
        x=0.98,
        y=0.05,
        s=r"$q_{\text{spez},\SI{1.8}{\kilo\volt}} = \SI{" + f"{fit_18.pu[0]:S}" + r"}{\coulomb\per\kilo\gram}$"
        "\n"
        r"$q_{\text{spez},\SI{4.0}{\kilo\volt}} = \SI{" + f"{fit_40.pu[0]:S}" + r"}{\coulomb\per\kilo\gram}$",
        transform=ax.transAxes,
        horizontalalignment="right",
        verticalalignment="bottom",
        bbox=dict(alpha=0.5, facecolor="white"),
    )
    lt.plt.xlabel(r"$\frac{1}{r}$ / $\si{\per\meter}$")
    lt.plt.ylabel(r"$B$ / $\si{\milli\tesla}$")
    lt.plt.title("Inverser Krümmungsradius des abgelenkten Elektronenstrahls\nals Abhängigkeit des Magnetfeldes")
    lt.plt.legend()
    lt.plt.grid()
    lt.plt.tight_layout()
    lt.plt.savefig("5_Festkoerperphysik/python/plots/kruemmungsradius_B.pdf")
    print("saved kruemmungsradius_B.pdf")
    lt.plt.close()


def print_latex(B_18, B_40):
    concat = np.concatenate((B_18, B_40)) * 1e3
    for b in concat:
        print(f"{b:S}")


def main() -> None:
    displacement_s = lt.unp.uarray([5, 10, 15, 20, 25, 30, 35], 2.0) * 1e-3  # m

    data_18_1 = np.array([40, 75, 100, 131, 164, 195, 228]) * 1e-3  # A
    data_18_2 = np.array([49, 78, 108, 149, 180, 208, 240]) * 1e-3  # A
    data_18 = lt.StudentArray([data_18_1, data_18_2])

    data_40_1 = np.array([76, 122, 165, 216, 261, 314, 360]) * 1e-3  # A
    data_40_2 = np.array([60, 100, 139, 190, 245, 290, 340]) * 1e-3  # A
    data_40 = lt.StudentArray([data_40_1, data_40_2])

    # calc radius
    radius = calc_radius(displacement_s)
    inverse_radius = 1 / radius  # 1/m
    print(inverse_radius)

    # calc B
    half_coil_distance_a = (lt.u.ufloat(73, 4) + lt.u.ufloat(22, 1)) * 1e-3 / 2  # m # type: ignore
    B_18 = get_magnetic_field(data_18.array, half_coil_distance_a)  # T
    B_40 = get_magnetic_field(data_40.array, half_coil_distance_a)  # T
    print_latex(B_18, B_40)

    # calc things for plot
    inverse_radius_n, _ = lt.separate_uarray(inverse_radius)
    B_18_n, _ = lt.separate_uarray(B_18)
    B_40_n, _ = lt.separate_uarray(B_40)

    # fit
    def lin_fit_func_r_inverse(U):
        return lambda B, q: lt.np.sqrt(q / (2 * U)) * B

    def lin_fit_func_B(U):
        return lambda r_inverse, q: lt.np.sqrt(2 * U / q) * r_inverse

    fit_18_r_inverse = lt.CurveFit(lin_fit_func_r_inverse(1.8e3), B_18_n, inverse_radius_n)
    fit_40_r_inverse = lt.CurveFit(lin_fit_func_r_inverse(4.0e3), B_40_n, inverse_radius_n)

    fit_18_B = lt.CurveFit(lin_fit_func_B(1.8e3), inverse_radius_n, B_18_n)
    fit_40_B = lt.CurveFit(lin_fit_func_B(4.0e3), inverse_radius_n, B_40_n)

    # plot
    plot_r_inverse(inverse_radius, B_18, B_40, fit_18_r_inverse, fit_40_r_inverse)
    plot_B(inverse_radius, B_18, B_40, fit_18_B, fit_40_B)

    # print calculated values
    print(f"q_sp_18:  {fit_18_r_inverse.pu[0]:e}")
    print(f"q_sp_40:  {fit_40_r_inverse.pu[0]:e}")
    print(f"q_sp_lit: {q_e/m_e:S}")  # type: ignore


if __name__ == "__main__":
    main()
