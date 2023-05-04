
import numpy as np
import matplotlib.pyplot as plt

with open('Wärmepumpe\Daten.csv') as infile:
    infile.readline()
    t = []
    T1 = []
    T2 = []
    for line in infile:
        string = line.replace(',', '.')
        l = string.split(';')
        t.append((float(l[0]) - 12.5317747222725)*3600)
        T1.append(float(l[1]))
        T2.append(float(l[2]))

t_array = np.asarray(t)
T1_array = np.asarray(T1)
T2_array = np.asarray(T2)
# fig = plt.figure(dpi=200)
# plt.plot(t_array/60, T1_array, label='$T_1$')
# plt.plot(t_array/60, T2_array, label='$T_2$')
# plt.xlabel('t / min')
# plt.ylabel('T / °C')
# plt.legend(loc='best')
# plt.title('Temperaturverläufe')
# plt.show()


# polynom
# coef_1 = np.polynomial.polynomial.polyfit(t_array[50:-1600], T1_array[50:-1600], 4)
# coef_2 = np.polynomial.polynomial.polyfit(t_array[50:-1600], T2_array[50:-1600], 5)
# def func(t, coef):
#     T = 0
#     DT = 0
#     for i, c in enumerate(coef):
#         if i == 0:
#             T += c*t**i
#         else:
#             DT += i*c*t**(i - 1)
#             T += c*t**i    
#     return DT, T


# T1 = []
# T2 = []
# T2_dot = []
# for t in t_array[50:-1600]:
#     T1.append(func(t, coef_1)[1])
#     T2_dot.append(func(t, coef_2)[0])
#     T2.append(func(t, coef_2)[1])

# x = t_array[50:-1600]

# plt.plot(x/60, T1)
# plt.plot(x/60, T2)

# c = 4.19*1e3
# m = 4
# P = 120
# q_point_pol = c*m*np.asarray(T2_dot)
# epsilon_pol = q_point_pol/P

# fig3 = plt.figure(dpi=200)
# plt.plot(np.asarray(T2) - np.asarray(T1), epsilon_pol)


# numerical
c = 4.19*1e3
m = 4
P = 120
dT2_dt = []
deltaT_list = []
timelist = []
epsilon_max = []
for i in range(2000):
    deltaT = T2_array[i + 800] - T2_array[i]
    deltat = t_array[i + 800] - t_array[i]
    dT2_dt.append(deltaT/deltat)
    deltaT_list.append(T2_array[i] - T1_array[i])
    timelist.append(t_array[i])
    epsilon_max.append(T2_array[i]/(T2_array[i] - T1_array[i]))
deltaT_array = np.asarray(deltaT_list)
dT2_dt_array = np.asarray(dT2_dt)
epsilon_max_array = np.asarray(epsilon_max)

q_point = c*m*dT2_dt_array
epsilon = q_point/P

deltaepsilon = 0.1*epsilon

# fig2 = plt.figure(dpi=200)
# markers, caps, bars = plt.errorbar(deltaT_array, epsilon, yerr=0.25, fmt='-', elinewidth=5, markersize=3, ecolor='r', label='$ε(ΔT)$')
# [bar.set_alpha(0.01) for bar in bars]
# plt.ylabel('$ε$ / 1')
# plt.xlabel('$ΔT$ / K')
# plt.title('Leistungszahl der Wärmepumpe')
# plt.legend()
# plt.show()

deltaeta = 1/epsilon_max_array*0.25 + epsilon/epsilon_max_array**2*0.2

fig3 = plt.figure(dpi=200)
markers, caps, bars = plt.errorbar(deltaT_array, epsilon/epsilon_max_array, yerr=0.2, fmt='-', elinewidth=5, markersize=3, ecolor='r', label='$η(ΔT)$')
[bar.set_alpha(0.01) for bar in bars]
plt.ylabel('$η$ / 1')
plt.xlabel('$ΔT$ / K')
plt.title('Gütegrad der Wärmepumpe')
plt.legend()
plt.show()








