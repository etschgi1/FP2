import pandas as pd


def calcError(reading, full_scale, round_=2):
    return round(reading * 0.03 + 0.005 * full_scale, round_)


def read_in_pol_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    start_ = [";" in line for line in lines].index(True)
    df = pd.read_csv(filename, sep=";", skiprows=start_ +
                     1, names=[x.strip() for x in lines[start_].split(";")])
    df["error 1"] = df.apply(lambda row: calcError(
        row["lux 1"], 2000), axis=1)
    df["error 2"] = df.apply(lambda row: calcError(row["lux 2"], 2000), axis=1)
    # print(df.head())
    for index, row in df.iterrows():
        for key in row.keys():
            if "error 2" in key:
                print(row[key], end="\t\\\\\n")
            else:
                print(row[key], end=" \t& ")


if __name__ == "__main__":
    read_in_pol_data("2_Interferometrie/data/Polarisationsfilter_quant.txt")
