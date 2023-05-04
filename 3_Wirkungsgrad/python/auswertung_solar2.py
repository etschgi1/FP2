import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from matplotlib.ticker import MaxNLocator
import scipy.optimize as opt
import lmfit 

import labtool as lt
lt.plt_latex()

dunkeldata = pd.read_csv("3_Wirkungsgrad/data/Versuch 2/dunkel_mod_final.csv", sep=",", decimal=".")
data400 =  pd.read_csv("3_Wirkungsgrad/data/Versuch 2/400_mod_final.csv", sep=",", decimal=".")
data1000 =  pd.read_csv("3_Wirkungsgrad/data/Versuch 2/1000_mod_final.csv", sep=",", decimal=".")

e = 1.602176634e-19
k_b =  1.380649e-23
T = 295 # K

def darkfit(u,I_s,f):
    return I_s * (np.exp(e*u/(f*k_b*T))-1) 
def hellfit(u,I_s,f,I_ph):
    return I_s * (np.exp(e*u/(f*k_b*T))-1) + I_ph
def residual(params, x, y,func):
    _,vals = params.valuesdict().keys(), params.valuesdict().values()
    return func(x, *vals) - y

def uncstr(val,unit=None):
    if unit:
        return "$({:L})".format(val)+ r"\,\unit{" + unit+r"}$"
    return "$({:L})$".format(val)

def plotkennlinie(data, name):
    fig, ax = plt.subplots()
    cutoffI = [x for x in data["I"] if round(x,3) < 1.0]
    ax.plot(data["V"][:len(cutoffI)], cutoffI, "x",label="Messwerte")
    ax.set_xlabel("U / V")
    ax.set_ylabel("I / A")
    ax.grid()
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    params = lmfit.Parameters()
    if name == "dunkel":
        params.add("I_s", value=1.41e-7, min=1e-8, max=1e-6)
        params.add("f", value=1.5, min=0.5, max=1.9)
        result = lmfit.minimize(residual, params, args=(data["V"][:len(cutoffI)], data["I"][:len(cutoffI)],darkfit)).params
        params = (result.valuesdict().values())
        ax.plot(data["V"][:len(cutoffI)], darkfit(data["V"][:len(cutoffI)], *params), label="Fit")
        I_S = lt.u.ufloat(result["I_s"].value, result["I_s"].stderr)
        f = lt.u.ufloat(result["f"].value, result["f"].stderr)
        ax.text(-0.8,0.1, r"$I_s = $" + uncstr(I_S, "A") + "\n" + r"$f = $" + uncstr(f),bbox=dict(facecolor='beige', alpha=0.5))
    else:
        params, error = opt.curve_fit(hellfit,data["V"][:len(cutoffI)],data["I"][:len(cutoffI)], p0=[1.41e-7,1.5,1e-7])
        I_S, I_ph, f = lt.u.ufloat(params[0], error[0][0]), lt.u.ufloat(params[1], error[1][1]), lt.u.ufloat(params[2], error[2][2])
        ax.text(-0.8,0.1, r"$I_s = $" + uncstr(I_S, "A") + "\n" +r"$I_{ph} = $" + uncstr(I_ph, "A") +"\n" + r"$f = $" + uncstr(f),bbox=dict(facecolor='beige', alpha=0.5))
        ax.plot(data["V"][:len(cutoffI)], hellfit(data["V"][:len(cutoffI)], *params), label="Fit")
    plt.savefig(f"3_Wirkungsgrad/latex/fig/plots/{name}_UI.png", bbox_inches="tight")
    plt.savefig(f"3_Wirkungsgrad/latex/fig/plots/{name}_UI.pdf", bbox_inches="tight")

def plotLeistung(data,name,P_zu):
    # plot Leistung
    cutoffI = [x for x in data["I"] if round(x,3) < 1.0]
    data["I"] = data["I"][:len(cutoffI)]
    data["V"] = data["V"][:len(cutoffI)]
    fig, ax = plt.subplots()
    ax.plot(data["V"], data["I"]*data["V"], label="Messwerte")
    ax.set_xlabel("U / V")
    ax.set_ylabel("P / W")
    #mark min
    minP = data["I"]*data["V"]
    minP = minP.idxmin()
    I_min, V_min = lt.u.ufloat(data["I"][minP], abs(data["I"][minP]*0.07)), lt.u.ufloat(data["V"][minP], abs(data["V"][minP]*0.07))
    minP_val = I_min * V_min
    ax.plot(data["V"][minP], data["I"][minP]*data["V"][minP], "x",label="Maximale Leistung")
    if P_zu != 0:
        eta = minP_val/P_zu
    else:
        eta = lt.u.ufloat(0,0)
        P_zu = lt.u.ufloat(0,0)
    ax.legend()
    ax.text(-0.8,0.1, r"$P_{max} = $" + uncstr(minP_val, "W") + "\n" +r"$U_{max} = $" + uncstr(V_min, "V") +"\n" + r"$I_{max} = $" + uncstr(I_min, "A")+"\n" + r"$P_{zu} = $" + uncstr(P_zu)+"\n" + r"$\eta = $" + uncstr(eta) ,bbox=dict(facecolor='beige', alpha=0.5))
    ax.grid()
    plt.savefig(f"3_Wirkungsgrad/latex/fig/plots/{name}_P.png", bbox_inches="tight")
    plt.savefig(f"3_Wirkungsgrad/latex/fig/plots/{name}_P.pdf", bbox_inches="tight")


solarcell_area = lt.u.ufloat(38e-3,1e-3)*lt.u.ufloat(17e-3,1e-3)
P_ein = [0,400*solarcell_area, 1000*solarcell_area] # W
for data,name,p_zu in zip([dunkeldata, data400, data1000], ["dunkel", "400", "1000"],P_ein):
    data.rename(columns={"Smu1.Time[1][1]":"t", "Smu1.V[1][1]":"V", "Smu1.I[1][1]":"I"}, inplace=True)
    # plotkennlinie(data, name)
    plotLeistung(data,name,p_zu)
    