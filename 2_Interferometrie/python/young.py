import labtool as lt

DISTANCE_DOUBLE_SLIT_SCREEN = lt.u.ufloat(252, 1) * 1e-2  # m # type: ignore
WAVELENGTH_LASER = 532e-9  # m
I_0 = 1


class DoubleSlit:
    width: float
    distance: float

    def __init__(self, width: float, distance: float) -> None:
        self.width = width
        self.distance = distance


def intensity_interference(x, d, lam=WAVELENGTH_LASER, z=DISTANCE_DOUBLE_SLIT_SCREEN):
    return I_0 * (1 + lt.unp.cos(2 * lt.np.pi * x * d / (lam * z)))  # type: ignore


def intensity_diffraction(x, D, lam=WAVELENGTH_LASER, z=DISTANCE_DOUBLE_SLIT_SCREEN):
    return I_0 * lt.unp.sin(lt.np.pi * D * x / (lam * z)) ** 2 / (lt.np.pi * D * x / (lam * z)) ** 2  # type: ignore


def main() -> None:
    # lt.plt_latex()
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

    for i, (slit, data) in enumerate(zip(slits, experimental_data)):
        x = lt.np.linspace(-lt.np.max(data), +lt.np.max(data), 1000)
        interference = intensity_interference(x, slit.width)
        diffraction = intensity_diffraction(x, slit.distance)
        lt.plt.figure.figsize = (8, 2)
        lt.plt_uplot(x, interference, label=f"Interferenz")  # type: ignore
        lt.plt_uplot(x, diffraction, label=f"Beugung")  # type: ignore
        lt.plt_uplot(x, interference * diffraction, label=f"Überlagerug")  # type: ignore
        for point in data:
            lt.plt.axvline(point, color="grey", linestyle="--")
            lt.plt.axvspan(point - 5e-4, point + 5e-4, color="grey", alpha=0.2)
        # lt.plt.xticks(x, x * 1e2)
        lt.plt.xlabel("$x$ / cm")
        lt.plt.ylabel("$I$ / a.u.")
        lt.plt.title(
            f"Theoretischer Intensitätsverlauf und Messpunkte\ndes Doppelspalts $d={slit.width * 1e3:.2f}$ mm, $D={slit.distance * 1e3:.2f}$ mm"
        )
        lt.plt.legend()
        # lt.plt.savefig(f"./2_Interferometrie/python/plots/young_{slit.width * 1e3:.2f}_{slit.distance * 1e3:.2f}.pdf")
        lt.plt.savefig(f"./2_Interferometrie/python/plots/young_{slit.width * 1e3:.2f}_{slit.distance * 1e3:.2f}.png")
        lt.plt.clf()
        print(f"DS{i+1} done")


if __name__ == "__main__":
    main()
