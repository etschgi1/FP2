import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np

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
    return Energie[Ereignisse.idxmax()], Ereignisse.max()
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
        pos.plot(peak_energie_idx, peak_energy_counts, "rx")
        peak_energies.append((peak_energie_idx, peak_energy_counts))
        # display peak energy
        pos.text(peak_energie_idx * 1.02, peak_energy_counts,
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
    return peak_energies, MESSUNGEN["deg_arm"]


def eV_to_joule(eV):
    return eV * 1.602176634e-19


def joule_to_eV(joule):
    return joule / 1.602176634e-19


def deg_to_rad(deg):
    return deg * np.pi / 180


E_0_Mo_kalpha = eV_to_joule(17.44e3)
c = 299792458  # m/s


def energy(phi, m_elec):
    return E_0_Mo_kalpha / (1 + ((E_0_Mo_kalpha / (m_elec * c**2))) * (1 - np.cos(phi)))


def eval_compton(peak_energies, angles):
    # plot energies over angles
    fig, ax = plt.subplots()
    peak_energies = [(x[0] * 1000) for x in peak_energies]
    angles = deg_to_rad(angles)
    ax.plot(angles, peak_energies, "rx", label="Data")
    ax.set_title("Peak energies over arm angles")
    ax.set_xlabel("Arm angle / rad")
    ax.set_ylabel("Peak energy / eV")
    ax.grid()
    # fit energy
    peak_energies_joule = [eV_to_joule(x) for x in peak_energies]
    popt, pcov = sp.optimize.curve_fit(
        energy, angles, peak_energies_joule)
    print(popt)
    print(f"Got electron mass of {popt[0]} kg")
    # plot fit
    x = np.linspace(min(angles), max(angles), 1000)
    y = energy(x, popt[0])
    ax.plot(x, y, label="Fit")

    plt.savefig("1_Compton_Roentgenfluoreszenzanalyse/plots/energie_winkel.pdf")
    plt.savefig("1_Compton_Roentgenfluoreszenzanalyse/plots/energie_winkel.png")
    plt.show()


def main():
    ret = (plot_energie_spektren())
    eval_compton(ret[0], ret[1])


if __name__ == "__main__":
    main()
