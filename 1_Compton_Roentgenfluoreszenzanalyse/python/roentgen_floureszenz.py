import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
import scipy as sp
import labtool as lt


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


FILE_ROOT = "1_Compton_Roentgenfluoreszenzanalyse/data/roentgen"
# kalibrierung hat irgendwie scheiße ausgesehen
filenames = ["Ag", "Cu", "Fe",
             "Mo", "Ni", "Ti", "Zn", "Zr", "Probe1", "Probe2", "Ring"]
exp_data = [pd.read_csv(f"{FILE_ROOT}/{filename}.csv", sep=";")
            for filename in filenames]
print(exp_data[0].head())

# info peak-finder engine Elias :))
k_beta_peak_hints = {"Cu": 8.75, "Mo": 19.15,
                     "Ag": 24.1, "Zn": 9.4, "Zr": 17.5}


def find_highest_peak(counts):
    max_index, max_value = np.nanargmax(counts), counts.max()
    return max_index, max_value


def plot_all_counts_over_engergy(data):
    fig, ax = plt.subplots(3, 4, figsize=(18.5, 10.5))
    peaks_found = {}
    for i, d in enumerate(data):
        energy_numpy = np.array(d["Energie E_A / keV"])
        counts_numpy = np.array(d["Ereignisse N_A"])
        idx, val = find_highest_peak(counts_numpy)
        peaks_found[filenames[i]] = [
            energy_numpy[idx]]  # energy, counts
        ax[i // 4, i %
            4].plot(energy_numpy, counts_numpy)
        ax[i // 4, i % 4].set_title(filenames[i])
        ax[i // 4, i % 4].set_xlabel("Energie / keV")
        ax[i // 4, i % 4].set_ylabel("Ereignisse / 1")
        ax[i // 4, i % 4].grid()
        ax[i // 4, i % 4].axvline(energy_numpy[idx],
                                  color="black", linestyle="--")
        ax[i // 4, i % 4].text(energy_numpy[idx] * 1.08, max(counts_numpy) * 0.9,
                               f"K-alpha: {energy_numpy[idx]:.2f} keV")
        if filenames[i] in k_beta_peak_hints:
            peaks_found[filenames[i]] += [k_beta_peak_hints[filenames[i]]]
            ax[i // 4, i %
                4].axvline(k_beta_peak_hints[filenames[i]], color="gray", linestyle="--")
            ax[i // 4, i % 4].text(k_beta_peak_hints[filenames[i]] * 1.08, max(counts_numpy) * 0.7,
                                   f"K-beta: {k_beta_peak_hints[filenames[i]]:.2f} keV", color="gray")

    plt.tight_layout()
    # delete empty axes
    for a in ax.flat:
        # check if something was plotted
        if not bool(a.has_data()):
            fig.delaxes(a)  # delete if nothing is plotted in the axes obj
    print(peaks_found)
    plt.savefig("1_Compton_Roentgenfluoreszenzanalyse/plots/roentgen_data.pdf")
    plt.savefig("1_Compton_Roentgenfluoreszenzanalyse/plots/roentgen_data.png")
    # plt.show()
    plt.close()
    return peaks_found


def calculate_covariance_of_two_lists(list1, list2):
    #!maybe for the unknown materials maybe not
    if len(list1) != len(list2):
        raise ValueError("List must be of same length")
    mean1 = np.mean(list1)
    mean2 = np.mean(list2)
    cov = 0
    for i in range(len(list1)):
        cov += (list1[i] - mean1) * (list2[i] - mean2)
    cov /= len(list1)
    return cov


energy_peaks = plot_all_counts_over_engergy(exp_data)
Ordnungszahlen_der_Elemente = {
    "Ag": 47, "Cu": 29, "Fe": 26, "Mo": 42, "Ni": 28, "Ti": 22, "Zn": 30, "Zr": 40}
R_y = 13.6  # Rydberg constant in keV


def mod_energy(E):
    return np.sqrt(E * 1000 / R_y)


def fitfunc(x, k):
    return k * x


def moesley(mod_energy, Z, alpha=True):
    if alpha:  # alpha
        n1, n2 = 1, 2
    else:  # beta
        n1, n2 = 1, 3
    return -mod_energy * (1 / n1**2 - 1 / n2**2)**(-1 / 2) + Z


def plot_Ordnungszahl_against_mod_energy(energy_peaks):
    fig, ax = plt.subplots()
    scatter_alpha = []
    scatter_beta = []
    for key, element in energy_peaks.items():
        try:
            scatter_alpha.append((
                Ordnungszahlen_der_Elemente[key], mod_energy(element[0])))
            if len(element) == 2:
                scatter_beta.append(
                    (Ordnungszahlen_der_Elemente[key], mod_energy(element[1])))
        except KeyError:
            continue
    scatter_x_alpha, scatter_y_alpha = zip(*scatter_alpha)
    scatter_x_beta, scatter_y_beta = zip(*scatter_beta)
    # info a bissl an fehler drauf und passt schon
    scatter_y_alpha_err = lt.unp.uarray(scatter_y_alpha, 0.2)
    scatter_y_beta_err = lt.unp.uarray(scatter_y_beta, 0.2)
    ax.scatter(scatter_x_alpha, scatter_y_alpha, marker="x", label="K-alpha")
    ax.scatter(scatter_x_beta, scatter_y_beta, marker="x", label="K-beta")
    # fit both lines with scipy optimize
    fit_alpha, var_a = sp.optimize.curve_fit(
        fitfunc, scatter_x_alpha, scatter_y_alpha)
    fit_beta, var_b = sp.optimize.curve_fit(
        fitfunc, scatter_x_beta, scatter_y_beta)
    # plot both lines
    x = np.linspace(20, 50, 100)
    y_alpha = fitfunc(x, fit_alpha[0])
    y_beta = fitfunc(x, fit_beta[0])
    ax.plot(x, y_alpha, label="Fit K-alpha")
    ax.plot(x, y_beta, label="Fit K-beta")
    # print the fit parameters
    print(
        f"Fit K-alpha: {fit_alpha[0]:.6f} * Z - unvertainty: {var_a[0][0]:.6f} ")
    print(
        f"Fit K-beta: {fit_beta[0]:.6f} * Z - uncertainty: {var_b[0][0]:.6f} ")
    ax.set_ylabel(r"$\sqrt{\frac{E}{R_y}}$ / 1")
    ax.set_xlabel(r"$Z$ / 1")
    ax.legend()
    ax.grid()
    # plot 2-sigma uncertainty
    ax.fill_between(
        x, y_alpha - 2 * np.sqrt(var_a[0][0]), y_alpha + 2 * np.sqrt(var_a[0][0]), alpha=0.2)
    ax.fill_between(
        x, y_beta - 2 * np.sqrt(var_b[0][0]), y_beta + 2 * np.sqrt(var_b[0][0]), alpha=0.2)
    # calc Abschirmung
    const_alpha = np.mean([moesley(scatter_y_alpha_err[i], scatter_x_alpha[i])
                          for i in range(len(scatter_x_alpha))])
    const_beta = np.mean([moesley(scatter_y_beta_err[i], scatter_x_beta[i],
                         alpha=False) for i in range(len(scatter_x_beta))])
    print(f"Abschirmung alpha: {const_alpha:.6f}")
    print(f"Abschirmung beta: {const_beta:.6f}")
    lab_a, lab_b = r"$\sigma_{2,1,exp}=$" + str(round(const_alpha.n, 2)) + r"$\pm$" + str(round(const_alpha.s, 2)), r"$\sigma_{2,1,exp} = $" + \
        str(round(const_beta.n, 2)) + r"$\pm$" + str(round(const_beta.s, 2))
    ax.text(0.7, 0.1, lab_a,
            transform=ax.transAxes, va="top")
    ax.text(0.7, 0.05, lab_b,
            transform=ax.transAxes, va="top")
    plt.savefig(
        "1_Compton_Roentgenfluoreszenzanalyse/plots/roentgen_data_Z_vs_E.pdf")
    plt.savefig(
        "1_Compton_Roentgenfluoreszenzanalyse/plots/roentgen_data_Z_vs_E.png")
    # plt.show()


plot_Ordnungszahl_against_mod_energy(energy_peaks)
