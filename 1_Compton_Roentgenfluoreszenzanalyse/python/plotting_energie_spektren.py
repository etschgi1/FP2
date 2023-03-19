import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
from matplotlib import rcParams


def plt_latex() -> None:
    """Use LaTeX as text processor for matplotlib, set figsize for a textwidth of 15 cm"""
    cm = 1 / 2.54  # conversion factor inch to cm
    rcParams.update(
        {
            "text.usetex": True,
            "text.latex.preamble": r"\usepackage{lmodern}\usepackage[locale=DE,uncertainty-mode=separate]{siunitx}",
            "font.family": "Latin Modern Roman",
            "figure.figsize": (15 * cm, 9 * cm),  # 15:9 relation
            "figure.autolayout": True,  # auto tight_layout()
        }
    )
    return None


plt_latex()

ROOT_FOLDER = "1_Compton_Roentgenfluoreszenzanalyse/data/csv"
ARMOFFSET = -1.6
MESSUNGEN = pd.DataFrame(
    {"deg_target": [20] * 9, "deg_arm": [30 + ARMOFFSET + 15 * x for x in range(9)]})


# !TODO maybe change if we really want to find the middle
def find_peak_energy(Ereignisse, Energie):
    # find peak energy
    # find 5 highest peaks
    peaks, _ = sp.signal.find_peaks(Ereignisse, height=150)
    # interpolated peak index
    center = np.sum(peaks * Energie[peaks]) / np.sum(Energie[peaks])
    lower_index, higher_index = int(np.floor(center)), int(np.ceil(center))
    # interpolate peak energy
    peak_energy_init = (Energie[lower_index] + (Energie[higher_index] -
                        Energie[lower_index]) * (center - lower_index))
    counts_at_peak = (Ereignisse[lower_index] + (Ereignisse[higher_index] -
                      Ereignisse[lower_index]) * (center - lower_index))
    # simple:
    # return Energie[Ereignisse.idxmax()], Ereignisse.max()
    # "besser"
    return peak_energy_init, counts_at_peak


def plot_energie_spektren():
    MESSUNGEN["name"] = ["Plexi_20_" + str(x) for x in MESSUNGEN["deg_arm"]]
    print("Plot following data: ")
    print(MESSUNGEN)
    peak_energies = []
    fig, ax = plt.subplots(3, 3)
    for index, row in MESSUNGEN.iterrows():
        data = pd.read_csv(ROOT_FOLDER + "/" + row["name"] + ".csv", sep=";")
        data.replace(",", ".", regex=True, inplace=True)
        Ereignisse = data["Ereignisse N_A"].astype(float)
        Energie = data["Energie E_A / keV"].astype(float)
        pos = ax[index // 3, index % 3]
        pos.plot(Energie, Ereignisse)
        pos.set_title("Arm angle: " + str(row["deg_arm"]) + "°")
        pos.set_xlabel("Energy / keV")
        pos.set_ylabel("Counts")
        pos.grid()
        # mark highest peak
        peak_energie_idx, peak_energy_counts = find_peak_energy(
            Ereignisse, Energie)
        # pos.plot(peak_energie_idx, peak_energy_counts, "rx")
        pos.axvline(peak_energie_idx, color="r", linestyle="--")
        peak_energies.append((peak_energie_idx, peak_energy_counts))
        # display peak energy
        pos.text(peak_energie_idx * 1.05, max(Ereignisse) * 0.9,
                 str(round(peak_energie_idx, 2)) + " keV")
    print("Peak energies: {}".format(peak_energies))
    fig.set_size_inches(18.5, 10.5)
    plt.tight_layout()
    plt.savefig(
        "1_Compton_Roentgenfluoreszenzanalyse/plots/energie_spektren.pdf")
    plt.savefig(
        "1_Compton_Roentgenfluoreszenzanalyse/plots/energie_spektren.png")
    # plt.show()
    plt.close()
    return peak_energies, np.array(list(MESSUNGEN["deg_arm"]))


#### Constants ####
ev_to_joule = 1.602176634e-19
E_0_Mo_kalpha = 17374.29 * ev_to_joule  # joule
# joule #source: http://hyperphysics.phy-astr.gsu.edu/hbase/Tables/kxray.html
E_0_Mo_kalpha_uncertainty = 0.03 * ev_to_joule
c = 299792458  # m/s
e_mass_theory = 9.1093837015e-31  # kg


def energy(phi, m_elec, E_0_Mo_kalpha=E_0_Mo_kalpha):
    return E_0_Mo_kalpha / (1 + ((E_0_Mo_kalpha / (m_elec * c**2))) * (1 - np.cos(phi)))


def eval_compton(peak_energies, angles):
    # plot energies over angles
    print("Plot energies over angles")
    fig, ax = plt.subplots()
    peak_energies = np.array(
        [x[0] for x in peak_energies]) * 1000 * ev_to_joule  # to joule
    angles = np.deg2rad(angles)  # to rad
    ax.plot(angles, peak_energies / (1000 * ev_to_joule),
            "rx", label="Data")  # plot in keV
    ax.set_title("Peak energies over arm angle")
    ax.set_xlabel("Arm angle / rad")
    ax.set_ylabel("Peak energy / keV")
    ax.grid()
    # fit energy
    popt, pcov = sp.optimize.curve_fit(
        energy, angles, peak_energies, p0=[e_mass_theory])
    print(
        f"Got electron mass of {popt[0]} kg, uncertainty for mass {np.sqrt(pcov[0, 0])}")
    # plot fit
    x = np.linspace(min(angles), max(angles), 1000)
    y = energy(x, popt[0]) / (1000 * ev_to_joule)  # back to keV
    ax.plot(x, y, label="Fit")
    ax.legend()
    # plot uncertainty band
    sigma = 2
    y_one = energy(x, popt[0] + sigma *
                   np.sqrt(pcov[0, 0]), E_0_Mo_kalpha=E_0_Mo_kalpha + E_0_Mo_kalpha_uncertainty) / (1000 * ev_to_joule)
    y_two = energy(x, popt[0] - sigma *
                   np.sqrt(pcov[0, 0]), E_0_Mo_kalpha=E_0_Mo_kalpha - E_0_Mo_kalpha_uncertainty) / (1000 * ev_to_joule)
    lab = r"$2 \sigma$ uncertainty band"
    ax.fill_between(x, y_one, y_two, alpha=0.2, label=lab)

    plt.savefig("1_Compton_Roentgenfluoreszenzanalyse/plots/energie_winkel.pdf")
    plt.savefig("1_Compton_Roentgenfluoreszenzanalyse/plots/energie_winkel.png")
    plt.show()


def main():
    ret = plot_energie_spektren()
    print("Got following results: ")
    print(ret)
    eval_compton(ret[0], ret[1])


if __name__ == "__main__":
    main()
