import labtool as lt

DISTANCE_DOUBLE_SLIT_SCREEN = lt.u.ufloat(25200, 9) * 1e-4  # m  # type: ignore
WAVELENGTH_LASER = 532e-9  # m


class DoubleSlit:
    width: float
    distance: float

    def __init__(self, width: float, distance: float) -> None:
        self.width = width
        self.distance = distance


def intensity_interference(x, d, lam=WAVELENGTH_LASER, z=DISTANCE_DOUBLE_SLIT_SCREEN):
    return 0.5 * (1 + lt.unp.cos((2 * lt.np.pi * x * d) / (lam * z)))  # type: ignore


def intensity_diffraction(x, D, lam=WAVELENGTH_LASER, z=DISTANCE_DOUBLE_SLIT_SCREEN):
    return lt.unp.sin(lt.np.pi * x * D / (lam * z)) ** 2 / (lt.np.pi * x * D / (lam * z)) ** 2  # type: ignore


def main() -> None:
    slits = [
        DoubleSlit(0.2e-3, 0.25e-3),
        DoubleSlit(0.1e-3, 0.25e-3),
        DoubleSlit(0.1e-3, 0.5e-3),
        DoubleSlit(0.1e-3, 1e-3),
    ]
    experimental_data = [
        lt.np.array([0, 5, 11, 16, 21, 27, 33, 38, 43, 49, 55, 58]) * 1e-3,
        lt.np.array([0, 5, 11, 16, 22, 27, 32, 38, 43, 48, 54]) * 1e-3,
        lt.np.array([0, 2.5, 8, 10.5, 13, 16, 18.5, 21, 24, 26.5, 29]) * 1e-3,
        lt.np.array([0, 1.5, 2.5, 4, 5.5, 6.5, 8, 9.5, 10.5, 12, 13.5, 15]) * 1e-3,
    ]
    x = lt.np.linspace(-6e-2, 6e-2, 1000)

    for slit, data in zip(slits, experimental_data):
        interference = intensity_interference(x, slit.width)
        diffraction = intensity_diffraction(x, slit.distance)
        lt.plt_uplot(x, interference, label=f"Interferenz")  # type: ignore
        lt.plt_uplot(x, diffraction, label=f"Beugung")  # type: ignore
        lt.plt_uplot(x, interference * diffraction, label=f"Überlagerug")  # type: ignore
        for point in data:
            lt.plt.axvline(point, color="grey", linestyle="--")

        lt.plt.xlabel("$x$ / cm")
        lt.plt.ylabel("$I$ / a.u.")
        lt.plt.title(
            f"Theoretischer Intensitätsverlauf und Messpunkte des Doppelspalts $d={slit.width * 1e3:.2f}$ mm, $D={slit.distance * 1e3:.2f}$ mm"
        )
        lt.plt.legend()
        lt.plt.show()
        lt.plt.clf()


if __name__ == "__main__":
    main()
