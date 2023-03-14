import pandas as pd


def calcError(reading, full_scale, round_=0):
    res = round(reading * 0.03 + 0.005 * full_scale, round_)
    return res if res <= 10.0 else res // 10 * 10 + 10


def read_in_pol_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    start_ = [";" in line for line in lines].index(True)
    df = pd.read_csv(filename, sep=";", skiprows=start_ +
                     1, names=[x.strip() for x in lines[start_].split(";")])
    df["error 1"] = df.apply(lambda row: calcError(
        row["lux 1"], 2000), axis=1)
    df["error 2"] = df.apply(lambda row: calcError(row["lux 2"], 2000), axis=1)
    # round I1 and I2 to tens
    print(df.head())
    df["lux 1"] = df["lux 1"] // 10 * 10
    df["lux 2"] = df["lux 2"] // 10 * 10
    # first half
    print("I_1 \t& \Delta I_1 \t& I_2 \t& \Delta I_2")
    for index, row in df.iterrows():
        for key in ["deg", "lux 1", "error 1", "lux 2", "error 2"]:
            if "error 2" in key:
                print(int(row[key]), end="\t\\\\\n")
            else:
                print(int(row[key]), end=" \t& ")


if __name__ == "__main__":
    read_in_pol_data("2_Interferometrie/data/Polarisationsfilter_quant.txt")
