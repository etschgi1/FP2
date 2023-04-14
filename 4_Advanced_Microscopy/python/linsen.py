import labtool as lt

g = lt.unp.uarray([126, 44], [3, 2])
b = lt.unp.uarray([35, 54], [2, 2])

gbessel = lt.unp.uarray([23, 112], [2, 3])
bbessel = lt.unp.uarray([125, 36], [3, 3])
l = gbessel + bbessel
w = abs(gbessel - bbessel)


def f(g, b):
    return 1 / (1 / g + 1 / b)


def bessel(l, w):
    return (l**2 - w**2) / (4 * l)


print("------------Linsen---------")
print(f(g, b))
print(f(g, b).mean())
# print(lt.Student([x.n for x in f(g, b)], sigma=2))
print("------------Bessel---------")
print(bessel(l, w))
print(bessel(l, w).mean())

##############Leeuwenhoek##############


def M(f):
    return 250 / f


def f(n, d):
    return n * d / (4 * (n - 1))


n = lt.u.ufloat(1.518, 0.0005)  # laut angabe
d = lt.unp.uarray([2.5, 6.35], [0.05, 0.005])  # mm
print("------------Leeuwenhoek---------")
print(f(n, d))
print(M(f(n, d)))
