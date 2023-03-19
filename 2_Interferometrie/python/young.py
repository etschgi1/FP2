import labtool as lt

DISTANCE_DOUBLE_SLIT_SCREEN = lt.u.ufloat(252, 1) * 1e-2  # m # type: ignore
WAVELENGTH_LASER = 532e-9  # m
PIXEL_TO_DISTANCE_CONVERTERS = [
    lambda px: (px - 2748 + 1e-100) * 5e-3 / -(2748 - 3057),
    lambda px: (px - 1751 + 1e-100) * 5e-3 / -(1751 - 1859),
    lambda px: (px - 2337 + 1e-100) * 2.5e-3 / -(2337 - 2403),
    lambda px: (px - 3193 + 1e-100) * 1.5e-3 / -(3193 - 3248),
]  # px to m, added 1e-100 to avoid division by zero error
CALC_DOUBLE_SLITS = False


class DoubleSlit:
    width_D: float
    distance_d: float

    def __init__(self, width: float, distance: float) -> None:
        self.width_D = width
        self.distance_d = distance


def get_intensity_from_interference(x, d, lam=WAVELENGTH_LASER, z=DISTANCE_DOUBLE_SLIT_SCREEN) -> lt.np.ndarray:
    return 0.5 * (1 + lt.unp.cos(2 * lt.np.pi * x * d / (lam * z)))  # type: ignore


def get_intensity_from_diffraction(x, D, lam=WAVELENGTH_LASER, z=DISTANCE_DOUBLE_SLIT_SCREEN) -> lt.np.ndarray:
    term = lt.np.pi * D * x / (lam * z)
    return (lt.unp.sin(term) / term) ** 2  # type: ignore


def get_wavelength_from_nth_maximum(d, x, n):
    return d * x / (DISTANCE_DOUBLE_SLIT_SCREEN * n)


def get_grating_constant_from_nth_maximum(x, n):
    return n * WAVELENGTH_LASER * DISTANCE_DOUBLE_SLIT_SCREEN / x


def main() -> None:
    lt.plt_latex()
    path = "./2_Interferometrie/data/double_slits/"

    if CALC_DOUBLE_SLITS:
        slits = [
            DoubleSlit(0.2e-3, 0.25e-3),  # m
            DoubleSlit(0.1e-3, 0.25e-3),  # m
            DoubleSlit(0.1e-3, 0.5e-3),  # m
            DoubleSlit(0.1e-3, 1e-3),  # m
        ]
        experimental_data_ruler = [
            lt.np.array([0, 5, 11, 16, 21, 27, 33, 38, 43]) * 1e-3,  # , 49, 55, 58]),  # m
            lt.np.array([0, 5, 11, 16, 22, 27, 32, 38, 43, 48, 54]) * 1e-3,  # m
            lt.np.array([0, 2.5, 8, 10.5, 13, 16, 18.5, 21, 24, 26.5, 29]) * 1e-3,  # m
            lt.np.array([0, 1.5, 2.5, 4, 5.5, 6.5, 8, 9.5, 10.5, 12, 13.5, 15]) * 1e-3,  # m
        ]

        experimental_data_imagej = [
            lt.pd.read_csv(f"{path}DS1.csv", names=["px", "I"], skiprows=1),
            lt.pd.read_csv(f"{path}DS2.csv", names=["px", "I"], skiprows=1),
            lt.pd.read_csv(f"{path}DS3.csv", names=["px", "I"], skiprows=1),
            lt.pd.read_csv(f"{path}DS4.csv", names=["px", "I"], skiprows=1),
        ]

        for i, (slit, data_ruler, data_imagej, converter) in enumerate(
            zip(slits, experimental_data_ruler, experimental_data_imagej, PIXEL_TO_DISTANCE_CONVERTERS)
        ):
            # create figure
            fig, ax = lt.plt.subplots(figsize=(9, 3))

            # plot imagej data
            data_imagej["m"] = converter(data_imagej["px"])
            data_imagej["I"] /= lt.np.max(data_imagej["I"])
            ax.plot(data_imagej["m"], data_imagej["I"], label="Messdaten")

            # plot ruler data
            for point in data_ruler:
                ax.axvline(point, color="grey", linestyle="--")
                ax.axvspan(point - 5e-4, point + 5e-4, color="grey", alpha=0.2)

            # plot theoretical data
            interference = get_intensity_from_interference(data_imagej["m"], slit.distance_d)
            diffraction = get_intensity_from_diffraction(data_imagej["m"], slit.width_D)
            total = interference * diffraction

            # ax.plot(data_imagej["m"], total_n, label="Theoretischer Verlauf")
            lt.plt_uplot(data_imagej["m"], total, label="Theoretischer Verlauf")

            # configure plot
            ax.set_xlabel("$x$ / m")
            ax.set_ylabel("$I$ / a.u.")
            ax.set_title(
                "Theoretischer Intensitätsverlauf und Messkurve des Doppelspalts "
                f"$D={slit.width_D*1e3:.2f}$ mm, $d={slit.distance_d*1e3:.2f}$ mm"
            )
            ax.grid()
            ax.legend(loc="upper right")
            fig.tight_layout()
            path_plot = f"./2_Interferometrie/python/plots/young_{i+1}.p"
            fig.savefig(f"{path_plot}df")
            fig.savefig(f"{path_plot}ng")

            # calc wavelengths from maxima
            grating_constants = [
                get_wavelength_from_nth_maximum(slit.distance_d, data_ruler[n], n).n for n in range(1, 9)
            ]
            grating_constants_student = lt.Student(grating_constants)
            print(f"DS{i+1}:\n{grating_constants_student}")
            lt.plt.close(fig)
            print(f"-> DS{i+1} done\n")

    wavelength_total = lt.Student([531, 532, 630, 534])
    print(wavelength_total)

    ## difraction grating --------------------------------------------------------------------
    grating_data_imagej = lt.pd.read_csv(f"{path}grating.csv", names=["px", "I"], skiprows=1)
    grating_data_ruler = lt.np.array([0, 11, 21, 32, 43, 53, 64, 75, 86, 97, 108, 118, 128, 139, 151]) * 1e-3  # m

    # create figure
    fig, ax = lt.plt.subplots(figsize=(9, 3))

    # plot imagej data
    converter = lambda px: (px - 3726 + 1e-100) * 11e-3 / -(3726 - 3880)
    grating_data_imagej["m"] = converter(grating_data_imagej["px"])
    grating_data_imagej["I"] /= lt.np.max(grating_data_imagej["I"])
    ax.plot(grating_data_imagej["m"], grating_data_imagej["I"], label="Messdaten")

    # plot ruler data
    for point in grating_data_ruler:
        ax.axvline(point, color="grey", linestyle="--")
        ax.axvspan(point - 5e-4, point + 5e-4, color="grey", alpha=0.2)

    # configure plot
    ax.set_xlabel("$x$ / m")
    ax.set_ylabel("$I$ / a.u.")
    ax.set_title(r"Theoretischer Intensitätsverlauf und Messkurve des Gitters $\tilde{g}=8$ '/mm")
    ax.grid()
    ax.legend(loc="upper right")
    fig.tight_layout()
    path_plot = "./2_Interferometrie/python/plots/grating.p"
    fig.savefig(f"{path_plot}df")
    fig.savefig(f"{path_plot}ng")

    # calc wavelengths from maxima
    grating_constants = [
        get_grating_constant_from_nth_maximum(data, n).n for n, data in enumerate(grating_data_ruler[1:])
    ]
    grating_constants_student = lt.Student(grating_constants)
    print(f"Grating:\n{grating_constants_student}")
    lt.plt.close(fig)
    print("-> Grating done\n")

    lt.plt.show()


if __name__ == "__main__":
    main()
