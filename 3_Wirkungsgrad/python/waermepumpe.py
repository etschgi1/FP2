import labtool as lt
import matplotlib as mpl
from scipy.signal import savgol_filter
from numpy.typing import NDArray

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


def test_filter(data: lt.pd.DataFrame) -> None:
    data["T1"] += 273.15
    data["T2"] += 273.15
    T1_smoothed = savgol_filter(data["T1"], 101, 7)
    T2_smoothed = savgol_filter(data["T2"], 401, 5)

    dotT2 = lt.np.gradient(T2_smoothed, data["t"])
    dotT2_savgol = savgol_filter(data["T2"], 301, 4, deriv=1)
    dotQ = 4190 * 4 * dotT2
    epsilon = dotQ / 120

    T_diff = savgol_filter(data["T2"] - data["T1"], 201, 3)
    T_diff_pre_smoothed = T2_smoothed - T1_smoothed  # type: ignore

    fig, ax = lt.plt.subplots()
    # ax.plot(data["t"], data["T2"], label="T2")
    # ax.plot(data["t"], dotT2_gradient_unsmoothed, label="dotT2_gradient_unsmoothed")
    # ax.plot(data["t"], dotT2, label="dotT2_gradient")
    # ax.plot(data["t"], dotT2_savgol, label="dotT2_savgol")
    # ax.plot(data["t"], data["T1"], label="T1")
    # ax.plot(data["t"], T2_smoothed, label="T2 smoothed")
    # ax.plot(data["t"], T1_smoothed, label="T1 smoothed")
    ax.plot(data["t"], data["T2"] - data["T1"], label="actual T_diff")
    ax.plot(data["t"], T_diff, label="T_diff")
    # ax.plot(data["t"], T_diff_pre_smoothed, label="T_diff pre-smoothed")
    ax.set_xlabel(r"$\Delta T$ / °C")
    ax.set_ylabel(r"$\epsilon$ / 1")
    ax.legend()
    ax.grid()
    fig.savefig("./3_Wirkungsgrad/latex/fig/plots/T_Verlauf_Test.pdf")


def test_filter2(data: lt.pd.DataFrame, epsilon: NDArray) -> None:
    data["T1"] += 273.15
    data["T2"] += 273.15
    T_diff = savgol_filter(data["T2"] - data["T1"], 201, 3)

    T1_smoothed = savgol_filter(data["T1"], 101, 7)
    T2_smoothed = savgol_filter(data["T2"], 401, 5)

    epsilon_pre_smoothed = T2_smoothed / (T2_smoothed - T1_smoothed)  # type: ignore
    epsilon_actual = data["T2"] / (data["T2"] - data["T1"])
    epsilon_smoothed = savgol_filter(data["T2"] / (data["T2"] - data["T1"]), 101, 3)

    fig, ax = lt.plt.subplots()
    ax.plot(T_diff, epsilon, label="epsilon")
    # ax.plot(T_diff, epsilon_pre_smoothed, label="epsilon pre-smoothed")
    ax.plot(T_diff, epsilon_smoothed, label="epsilon smoothed")
    ax.set_xlabel(r"$\Delta T$ / °C")
    ax.set_ylabel(r"$\epsilon$ / 1")
    ax.legend()
    ax.grid()
    fig.savefig("./3_Wirkungsgrad/latex/fig/plots/epsilon_test.pdf")


def plot_leistungszahl(data: lt.pd.DataFrame) -> tuple[NDArray, NDArray]:
    c = 4184  # J / (kg * K)
    rho = 997  # kg / m^3
    V = 4e-3  # m^3
    m = rho * V  # kg
    P = 120  # W

    data["T1"] += 273.15  # °C -> K
    data["T2"] += 273.15  # °C -> K
    T_diff = savgol_filter(data["T2"] - data["T1"], 201, 3)

    dotT2 = savgol_filter(data["T2"], 301, 4, deriv=1)
    dotQ = c * m * dotT2  # type: ignore
    epsilon = dotQ / P

    fig, ax = lt.plt.subplots()
    ax.plot(T_diff, epsilon)
    ax.set_xlabel(r"$\Delta T$ / °C")
    ax.set_ylabel(r"$\epsilon$ / 1")
    ax.set_title("Leistungszahl der Wärmepumpe")
    ax.grid()

    fig.savefig("./3_Wirkungsgrad/latex/fig/plots/leistungszahl.pdf")

    return T_diff, epsilon


def plot_guetegrad(data: lt.pd.DataFrame, T_diff: NDArray, epsilon: NDArray) -> None:
    data["T1"] += 273.15
    data["T2"] += 273.15

    epsilon_carnot = savgol_filter(data["T2"] / (data["T2"] - data["T1"]), 101, 3)
    eta = epsilon / epsilon_carnot

    fig, ax = lt.plt.subplots()
    ax.plot(T_diff, eta)
    ax.set_xlabel(r"$\Delta T$ / °C")
    ax.set_ylabel(r"$\eta$ / 1")
    ax.set_title("Gütegrad der Wärmepumpe")
    ax.grid()

    fig.savefig("./3_Wirkungsgrad/latex/fig/plots/guetegrad.pdf")


def main() -> None:
    data = lt.pd.read_csv(
        "./3_Wirkungsgrad/data/Versuch 3/pumpe.csv",
        sep=";",
        decimal=",",
        header=0,
        names=["t", "T1", "T2"],
    )
    # plot_verlauf(data)
    T_diff, epsilon = plot_leistungszahl(data)
    plot_guetegrad(data, T_diff, epsilon)
    # test_filter2(data, epsilon)


if __name__ == "__main__":
    main()
