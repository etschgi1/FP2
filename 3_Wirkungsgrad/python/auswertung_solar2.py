import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from matplotlib.ticker import MaxNLocator
# import labtool as lt
# lt.plt_latex()

dunkeldata = pd.read_csv("3_Wirkungsgrad/data/Versuch 2/dunkel_mod_final.csv", sep=",", decimal=".")
data400 =  pd.read_csv("3_Wirkungsgrad/data/Versuch 2/400_mod_final.csv", sep=",", decimal=".")
data1000 =  pd.read_csv("3_Wirkungsgrad/data/Versuch 2/1000_mod_final.csv", sep=",", decimal=".")

e = 1.602176634e-19
k_b =  1.380649e-23
T = 295 # K

def plotkennlinie(data, name):
    fig, ax = plt.subplots()
    cutoffI = [x for x in data["I"] if round(x,3) < 1.0]
    ax.plot(data["V"][:len(cutoffI)], cutoffI, "x",label="Messwerte")
    ax.set_xlabel("U / V")
    ax.set_ylabel("I / A")
    ax.grid()
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    plt.show()
    return
    plt.savefig(f"3_Wirkungsgrad/latex/fig/plots/{name}.png", bbox_inches="tight")

for data,name in zip([dunkeldata, data400, data1000], ["dunkel", "400", "1000"]):
    data.rename(columns={"Smu1.Time[1][1]":"t", "Smu1.V[1][1]":"V", "Smu1.I[1][1]":"I"}, inplace=True)
    plotkennlinie(data, name)
    