import labtool as lt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

lt.plt_latex() 

#daten von files einlesen
data_root = "3_Wirkungsgrad/data/Versuch 1"
plot_root = "3_Wirkungsgrad/latex/fig/plots"
Data = {"solar_parallel":None, "solar_seriell":None, "solar_solar_verdeckt":None}

def getuncertainty(x, voltage=True):
    if voltage:
        x = np.array(x)  # V
        x[x <= 0.6] = x[x <= 0.6] * 0.0015 + 2e-4
        x[x > 0.6] = x[x > 0.6] * 0.0015 + 2e-3
        return x
    else:
        x = np.array(x)  # mA
        x[x <= 60] = x[x <= 60] * 0.01 + 3e-2
        x[x > 60] = x[x > 60] * 0.01 + 3e-1
        return x

def fuellfaktor(I_max,U_max,I_kurz,U_kurz):
    return I_max*U_max/(I_kurz*U_kurz)

def printlatextable(x,y):
    print("\\begin{tabular}{|c|c|}")
    print("\\hline")
    print("x & y \\\\")
    print("\\hline")
    for i in range(len(x)):
        print(str(x[i]) + " & " + str(y[i]) + "\\\\")
    print("\\hline")
    print("\\end{tabular}")

for key in Data:
    #start from 7 row
    Data[key] = pd.read_csv(data_root + "/" + key + ".txt", sep=";", decimal=".", skiprows=5)
    Data[key] = Data[key].rename(columns={"I / mA":"I"," U / V":"U"})
    Data[key]["I"] = lt.unp.uarray(Data[key]["I"],getuncertainty(Data[key]["I"],voltage=False))
    Data[key]["U"] = lt.unp.uarray(Data[key]["U"],getuncertainty(Data[key]["U"]))
    printlatextable(Data[key]["U"],Data[key]["I"])

def plotUI(U,I,title):
    lt.plt_uplot(U,I, label="Messwerte")
    kurz_i = I[len(I)-1]
    plt.errorbar(0,kurz_i.n, xerr=kurz_i.s, fmt="o", label="Kurzschlussstrom")
    leer_u = U[0]
    plt.errorbar(leer_u.n,0, yerr=leer_u.s, fmt="o", label="Leerlaufspannung")
    max_p_pos =  np.argmax(U*I)
    plt.errorbar(U[max_p_pos].n,I[max_p_pos].n, xerr=U[max_p_pos].s, yerr=I[max_p_pos].s, fmt="o", label="Maximale Leistung")
    plt.xlabel("U / V")
    plt.ylabel("I / mA")
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.savefig(plot_root + "/" + title + "_UI_.png", bbox_inches="tight")
    plt.cla()

def uncstr(val,unit=None, round_ = 2):
    if unit:
        return "$("+str(round(val.n,round_)) + r"\pm" + str(round(val.s,round_)) +")"+ r"\,\unit{" + unit+r"}$"
    return "$("+str(round(val.n,round_)) + r"\pm" + str(round(val.s,round_))+")$"

def plotUP(I,U,P,title):
    lt.plt_uplot(U,P, label="Messwerte")
    max_p_pos = np.argmax(P)
    plt.errorbar(U[max_p_pos].n,P[max_p_pos].n, xerr=U[max_p_pos].s, yerr=P[max_p_pos].s, fmt="o", label="Maximale Leistung")
    max_p = P[max_p_pos]
    U_max_p = U[max_p_pos]
    I_max_p = I[max_p_pos]
    kurz_i = I[len(I)-1]
    leer_u = U[0]
    füllfaktor = fuellfaktor(I_max_p,U_max_p,kurz_i,leer_u)
    # textbox with max_p U_max_p, I_max_p, füllfaktor in light beige
    plt.text(np.max(U).n*0.3,np.max(P).n*0.05, r"$P_{MPP}=$ " +uncstr(max_p,r"\watt")+ "\n" + r"$U_{MPP}=$ " +uncstr((U_max_p),r"\volt") + "\n" + r"$I_{MPP}=$ " +uncstr(I_max_p,r"\milli\ampere") + "\n" + r"FF = " +uncstr(füllfaktor),  bbox=dict(facecolor='beige', alpha=0.5))
    plt.xlabel("U / V")
    plt.ylabel("P / mW")
    plt.title(title)
    plt.grid()
    plt.savefig(plot_root + "/" + title + "_UP_.png", bbox_inches="tight")
    plt.cla()


for key in Data:
    plotUI(Data[key]["U"],Data[key]["I"], key)
    plotUP(Data[key]["I"],Data[key]["U"],Data[key]["I"]*Data[key]["U"],key)