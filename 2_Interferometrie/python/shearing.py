import labtool as lt


def calculate_radius_wavefront(l, d, theta, lambdA):
    return l * d / (lambdA * lt.unp.sin(theta))  # type: ignore


def main() -> None:

    lateral = lt.Student([10.0, 9.5, 10.0])  # mm
    distance = lt.Student([3.0, 3.5, 3.0])  # mm
    angle = lt.Student([22, 20, 25])  # deg

    print("l:", lateral.mean)
    print("d:", distance.mean)
    print("theta:", angle.mean)

    radius = calculate_radius_wavefront(
        lateral.mean * 1e-3, distance.mean * 1e-3, angle.mean *
        lt.np.pi / 180, lt.u.ufloat(537, 18) * 1e-9
    )
    print(f"{radius=}")


if __name__ == "__main__":
    main()
