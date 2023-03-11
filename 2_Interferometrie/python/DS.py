
def format_maxima(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    bins = {}
    start_ = ["Maxima" in line for line in lines].index(True)
    for line in lines[start_:]:
        if "Maxima" in line:
            add_ = float(
                line.split(":")[1].split("mm")[0])
            try:
                bins[line.split(".")[0]] += [add_]
            except KeyError:
                bins[line.split(".")[0]] = [add_]
    # printout latex table style
    for key in bins:
        print(key, end=" & ")
        for i, item in enumerate(bins[key]):
            if i == len(bins[key]) - 1:
                print(item, end="\\\\")
                print()
            else:
                print(item, end="& ")


if __name__ == "__main__":
    format_maxima("2_Interferometrie/data/gitter.txt")
