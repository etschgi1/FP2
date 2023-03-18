import labtool as lt
import scipy.signal

DISTANCE_DOUBLE_SLIT_SCREEN = lt.u.ufloat(252, 1) * 1e1  # mm # type: ignore
WAVELENGTH_LASER = 532e-6  # mm
PIXEL_TO_DISTANCE_IN_MM_CONVERTERS = [
    lambda px: (px - 2748 + 1e-100) * 5 / -(2748 - 3057),
    lambda px: (px - 1751 + 1e-100) * 5 / -(1751 - 1859),
    lambda px: (px - 2337 + 1e-100) * 2.5 / -(2337 - 2403),
    lambda px: (px - 3193 + 1e-100) * 1.5 / -(3193 - 3248),
]  # px to mm, added 1e-100 to avoid division by zero


class DoubleSlit:
    width: float
    distance: float

    def __init__(self, width: float, distance: float) -> None:
        self.width = width
        self.distance = distance


def intensity_interference(x, d, lam=WAVELENGTH_LASER, z=DISTANCE_DOUBLE_SLIT_SCREEN, I_0=1) -> lt.np.ndarray:
    return I_0 * 0.5 * (1 + lt.unp.cos(2 * lt.np.pi * x * d / (lam * z)))  # type: ignore


def intensity_diffraction(x, D, lam=WAVELENGTH_LASER, z=DISTANCE_DOUBLE_SLIT_SCREEN, I_0=1) -> lt.np.ndarray:
    term = lt.np.pi * D * x / (lam * z)
    return I_0 * (lt.unp.sin(term) / term) ** 2  # type: ignore


def main() -> None:
    # lt.plt_latex()
    slits = [
        DoubleSlit(0.2, 0.25),  # mm
        DoubleSlit(0.1, 0.25),  # mm
        DoubleSlit(0.1, 0.5),  # mm
        DoubleSlit(0.1, 1),  # mm
    ]
    experimental_data_ruler = [
        lt.np.array([0, 5, 11, 16, 21, 27, 33, 38, 43]),  # , 49, 55, 58]),  # mm
        lt.np.array([0, 5, 11, 16, 22, 27, 32, 38, 43, 48, 54]),  # mm
        lt.np.array([0, 2.5, 8, 10.5, 13, 16, 18.5, 21, 24, 26.5, 29]),  # mm
        lt.np.array([0, 1.5, 2.5, 4, 5.5, 6.5, 8, 9.5, 10.5, 12, 13.5, 15]),  # mm
    ]

    path = "./2_Interferometrie/data/double_slits/"
    experimental_data_imagej = [
        lt.pd.read_csv(f"{path}DS1.csv", names=["px", "I"], skiprows=1),
        lt.pd.read_csv(f"{path}DS2.csv", names=["px", "I"], skiprows=1),
        lt.pd.read_csv(f"{path}DS3.csv", names=["px", "I"], skiprows=1),
        lt.pd.read_csv(f"{path}DS4.csv", names=["px", "I"], skiprows=1),
    ]

    for i, (slit, data_ruler, data_imagej, converter) in enumerate(
        zip(slits, experimental_data_ruler, experimental_data_imagej, PIXEL_TO_DISTANCE_IN_MM_CONVERTERS)
    ):

        fig, ax = lt.plt.subplots(figsize=(8, 3))

        # plot imagej data
        data_imagej["mm"] = converter(data_imagej["px"])
        data_imagej["I"] = data_imagej["I"] / lt.np.max(data_imagej["I"])
        # ax.plot(data_imagej["mm"], data_imagej["I"], label="Messdaten")

        # # plot ruler data
        # for point in data_ruler:
        #     ax.axvline(point, color="grey", linestyle="--")
        #     ax.axvspan(point - 5e-4, point + 5e-4, color="grey", alpha=0.2)

        # plot theoretical data
        interference = intensity_interference(data_imagej["mm"], slit.width)
        diffraction = intensity_diffraction(data_imagej["mm"], slit.distance)
        # ax.plot(data_imagej["mm"], [x.n for x in interference], label=f"Interferenz")
        # ax.plot(data_imagej["mm"], [x.n for x in diffraction], label=f"Beugung")
        ax.plot(data_imagej["mm"], [x.n for x in interference * diffraction], label=f"Theoretischer Verlauf")  # type: ignore

        # configure plot
        ax.set_xlabel("$x$ / mm")
        ax.set_ylabel("$I$ / a.u.")
        ax.set_title(
            "Theoretischer Intensitätsverlauf und Messpunkte\ndes Doppelspalts "
            f"$d={slit.width:.2f}$ mm, $D={slit.distance:.2f}$ mm"
        )
        ax.grid()
        ax.legend()
        fig.tight_layout()
        fig.savefig(f"./2_Interferometrie/python/plots/young_{slit.width:.2f}_{slit.distance:.2f}.png")
        # lt.plt.show()
        print(f"DS{i+1} done")


if __name__ == "__main__":
    main()
