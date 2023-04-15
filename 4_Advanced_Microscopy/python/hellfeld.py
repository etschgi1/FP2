# type: ignore

import labtool as lt


def main() -> None:
    f_obj = lt.u.ufloat(35, 0.4) * 1e-3
    f_oku = lt.u.ufloat(50, 0.4) * 1e-3
    d_obj_oku = lt.u.ufloat(170, 5) * 1e-3
    t_o = d_obj_oku - f_obj - f_oku
    print(f"t_o = {t_o*1e3} mm")

    V_MIK_th = -t_o / f_obj * 0.25 / f_oku
    print(f"V_MIK,th = {V_MIK_th}")

    d_unver = lt.u.ufloat(128, 7)
    d_ver = lt.u.ufloat(840, 50)
    V_MIK_ex = d_ver / d_unver
    print(f"V_MIK,ex = {V_MIK_ex}")

    G = 6
    E = lt.u.ufloat(5, 0.5)
    f_r = 2 ** (G + (E - 1) / 6)
    x_min = 1 / f_r
    print(f"f_r = {f_r} LP/mm")
    print(f"x_min = {x_min} mm")


if __name__ == "__main__":
    main()
