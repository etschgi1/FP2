import labtool as lt


def main() -> None:
    I_0 = 1144
    data = lt.StudentArray(
        lt.np.array(
            [
                [1020, 1070],
                [990, 1050],
                [910, 960],
                [780, 820],
                [610, 640],
                [440, 450],
                [270, 280],
                [130, 140],
                [30, 30],
                [0, 0],
                [20, 20],
                [100, 110],
                [230, 250],
                [390, 410],
                [570, 600],
                [750, 790],
                [890, 940],
                [1000, 1040],
                [1040, 1090],
                [1020, 1070],
                [950, 990],
                [810, 840],
                [650, 670],
                [470, 490],
                [280, 300],
                [150, 150],
                [30, 40],
                [0, 0],
                [20, 20],
                [110, 120],
                [250, 260],
                [420, 440],
                [600, 630],
                [740, 810],
                [920, 970],
                [1020, 1070],
                [1060, 1100],
            ]
        ).T, sigma=2
    )

    angle_shifted = lt.np.arange(-30, 331, 10)
    angle_rad = lt.np.linspace(0, 2 * lt.np.pi, 37)

    lt.plt_latex()
    cm = 1 / 2.54  # conversion factor inch to cm
    fig, ax = lt.plt.subplots(figsize=(15 * cm, 8 * cm))

    lt.plt_uplot(angle_shifted, data, label="Messwerte")  # type: ignore
    ax.plot(angle_shifted, I_0 * lt.np.cos(angle_rad) ** 2, label="Theorie")
    ax.set_xticks(angle_shifted[::2], rotation=45)
    ax.set_xlabel(r"$\alpha$ / °")
    ax.set_ylabel(r"$I$ / lx")
    ax.set_title(
        "Intensitätsverlauf des Lasers beim Durchgang durch zwei\nPolarisationsfilter in Abhängigkeit von der Winkelverschiebung "
        + r"$\alpha$"
    )
    ax.legend()
    ax.grid()
    fig.savefig("./2_Interferometrie/python/plots/polarisation.pdf")


if __name__ == "__main__":
    main()
