import labtool as lt
import matplotlib as mpl
from scipy.signal import savgol_filter

mpl.use("agg")
lt.plt_latex()


def plot_verlauf(data: lt.pd.DataFrame) -> None:
    fig, ax = lt.plt.subplots()
    ax.plot(data["t"], data["T1"], "C0", label="$T_1$")
    ax.plot(data["t"], data["T2"], "r", label="$T_2$")
    ax.set_xlabel("$t$ / s")
    ax.set_ylabel("$T$ / °C")
    ax.set_title("Temperaturverläufe der beiden Wärmereservoires")
    ax.grid()
    ax.legend()

    fig.savefig("./3_Wirkungsgrad/latex/fig/plots/T_Verlauf.pdf")


def plot_leistungszahl(data: lt.pd.DataFrame) -> None:
    c = 4.184e3  # J / (kg * K)
    rho = 997  # kg / m^3
    V = 4e-3  # m^3
    m = rho * V  # kg
    P = 120  # W

    data["T1"] = savgol_filter(data["T1"] + 273.15, 501, 5)  # °C -> K
    data["T2"] = savgol_filter(data["T2"] + 273.15, 501, 5)  # °C -> K

    fig, ax = lt.plt.subplots()
    ax.plot(data["t"], data["T1"], "C0", label="$T_1$")
    ax.plot(data["t"], data["T2"], "r", label="$T_2$")
    fig.savefig("./3_Wirkungsgrad/latex/fig/plots/T_Verlauf_Test.pdf")
    exit()

    dotT2 = lt.np.gradient(data["T2"], data["t"])
    dotQ = m * c * dotT2
    epsilon = dotQ / P

    delta_T = lt.np.diff(data["T2"])

    fig, ax = lt.plt.subplots()
    ax.plot(delta_T, epsilon[:-1])
    ax.set_xlabel(r"$\Delta T$ / K")
    ax.set_ylabel(r"$\epsilon$ / 1")
    ax.set_title("Leistungszahl der Wärmepumpe")
    ax.grid()

    fig.savefig("./3_Wirkungsgrad/latex/fig/plots/leistungszahl.pdf")


def main() -> None:
    data = lt.pd.read_csv(
        "./3_Wirkungsgrad/data/Versuch 3/pumpe.csv",
        sep=";",
        decimal=",",
        header=0,
        names=["t", "T1", "T2"],
    )
    # plot_verlauf(data)
    plot_leistungszahl(data)


if __name__ == "__main__":
    main()
