import labtool as lt


def get_wavelength(n, d):
    return 2 * d / n


def main() -> None:
    n = lt.u.ufloat(100, 1)
    d_sammel = lt.u.ufloat(26.4, 1) * 1e-6
    d_streu = lt.u.ufloat(26.6, 1) * 1e-6

    lambda_sammel = get_wavelength(n, d_sammel)
    lambda_streu = get_wavelength(n, d_streu)
    print(f"{lambda_sammel=}")
    print(f"{lambda_streu=}")


if __name__ == "__main__":
    main()
