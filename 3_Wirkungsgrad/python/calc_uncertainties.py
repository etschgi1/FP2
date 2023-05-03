import numpy as np
from numpy.typing import ArrayLike


def get_uncertainty_U(x: ArrayLike) -> ArrayLike:
    x = np.array(x)  # V
    x[x <= 0.6] = x[x <= 0.6] * 0.0015 + 2e-4
    x[x > 0.6] = x[x > 0.6] * 0.0015 + 2e-3
    return x


def get_uncertainty_I(x: ArrayLike) -> ArrayLike:
    x = np.array(x)  # mA
    x[x <= 60] = x[x <= 60] * 0.01 + 3e-2
    x[x > 60] = x[x > 60] * 0.01 + 3e-1
    return x


def main() -> None:
    def seriell():
        I = [
            0,
            11.70,
            15.19,
            19.79,
            24.17,
            26.60,
            28.92,
            30.93,
            34.05,
            38.52,
            43.50,
            48.40,
            52.01,
            54.51,
            55.58,
            56.56,
            57.06,
            57.20,
            57.30,
            57.30,
            57.25,
            57.30,
            57.80,
            58.20,
            58.70,
            59.50,
            61.20,
            63.30,
            65.50,
            65.40,
        ]  # mA
        U = [
            11.65,
            11.48,
            11.40,
            11.30,
            11.20,
            11.15,
            11.10,
            11.06,
            10.98,
            10.86,
            20.72,
            10.55,
            10.39,
            10.24,
            10.14,
            9.94,
            9.81,
            9.67,
            9.55,
            9.40,
            9.34,
            8.98,
            7.77,
            6.25,
            5.49,
            4.31,
            2.72,
            0.69,
            0.12,
            0,
        ]  # V


if __name__ == "__main__":
    main()
