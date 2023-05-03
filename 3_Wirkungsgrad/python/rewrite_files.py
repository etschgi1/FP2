import csv
root = "3_Wirkungsgrad/data/Versuch 2"
filenames = [root+"/" + x for x in ["dunkel.csv", "400.csv", "1000.csv"]]

def reworkline(line):
    line = line[:-2]
    prev = ""
    for e,c in enumerate(line):
        try:
            if c == "," and prev.isnumeric() and line[e+1].isnumeric() and line[e+2].isnumeric():
                line = line[:e] + "." + line[e+1:]
        except IndexError:
            prev = c
            continue
        prev = c
    return line + "\n"

for name in filenames:
    with open(name, newline='') as f:
        lines = f.readlines()
        lines = [reworkline(x) for x in lines]
        mod_name = name[:-4] + "_mod.csv"
        with open(mod_name, "w") as f:
            f.writelines(lines)